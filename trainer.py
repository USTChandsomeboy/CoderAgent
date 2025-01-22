import random
import json
import pickle
from tqdm import tqdm
import torch
import json
# import logging
import torch.nn.functional as F
from torch.optim import Adam
import numpy as np
from options import args
import os
import re
import pandas as pd
import numpy as np
from modules.adaptive_learner_modeling import *
from modules.learner_simulation import *
from modules.question_analysis import *
from modules.reflection_agent import *
from modules.ac_rate import *
from modules.evaluate_howwhat import *
from utils import save_profile, merge_codes, compile_code, compute_code_bleu
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(message)s',
#     handlers=[logging.StreamHandler(), logging.FileHandler('output.log')]
# )

def get_problem_info(problems: pd.DataFrame, problem_id: str) -> dict:
    """
    Retrieve problem information based on problem ID.

    Args:
        problems (pd.DataFrame): DataFrame containing problem data.
        problem_id (str): The ID of the problem.

    Returns:
        dict: Dictionary containing problem requirements and required skills.
    """
    problem_row = problems[problems['ProblemID'] == problem_id].iloc[0]
    return {
        'problem': problem_row['Requirement'],
        'problem_requireskill': problem_row['RequirementSkill']
    }

def handle_reflection(
    llm,
    profile,
    problem_info,
    all_records,
    code_record_updated,
    err_info
) -> str:
    """
    Handle the reflection process for code updates.

    Args:
        llm: The language model instance.
        profile (str): The user's profile.
        problem_info (dict): Information about the problem.
        all_records (list): List of all submission records.
        code_record_updated (str): The updated code record.
        err_info (str): Compilation error information.

    Returns:
        str: The final updated code after reflection.
    """
    reflection_information = analysis_question_with_llm(llm, profile, problem_info, all_records, code_record_updated)
    reflection_times = 0
    while reflection_information['judgment'] == 'No':
        if reflection_times > 3:
            break
        reflection_details = {
            'reflection_information': reflection_information['explanation'],
            'your_last_generated_code': code_record_updated
        }
        code_update = update_code_with_llm(llm, profile, problem_info, all_records, err_info, reflection_details)
        code_record_updated = code_record_updated.replace(code_update['code0'], code_update['code1'])
        reflection_information = analysis_question_with_llm(llm, profile, problem_info, all_records, code_record_updated)
        reflection_times += 1
    return code_record_updated

def process_training_data(
    metadata_folder: str,
    problems: pd.DataFrame,
    profiles: pd.DataFrame,
    profile_file: str,
    llm
) -> None:
    """
    Process the training dataset for all users.

    Args:
        metadata_folder (str): Path to the base training metadata folder containing user_id subfolders.
        problems (pd.DataFrame): DataFrame containing problem data.
        profiles (pd.DataFrame): DataFrame containing user profiles.
        profile_file (str): Path to the profile CSV file.
        llm: The language model instance.
    """
    # 获取所有用户ID文件夹
    user_folders = [d for d in os.listdir(metadata_folder) if os.path.isdir(os.path.join(metadata_folder, d))]

    for user_id in tqdm(user_folders, desc="Processing users"):
        print(f"Processing user: {user_id}", flush=True)
        user_folder_path = os.path.join(metadata_folder, user_id)
        for filename in os.listdir(user_folder_path):
            pattern = r"Problem_(p\d+)_records"
            match = re.search(pattern, filename)
            if match:
                problem_id = match.group(1)

            filepath = os.path.join(user_folder_path, filename)
            code_records = pd.read_csv(filepath)

            problem_info = get_problem_info(problems, problem_id)
            merged_code = merge_codes(code_records['Code'].tolist())

            if user_id in profiles['user_id'].values:
                profile = profiles.loc[profiles['user_id'] == user_id, 'profile'].values[0]
                profile = update_learner_profile_with_llm(llm, profile, merged_code)
            else:
                profile = initialize_learner_profile_with_llm(llm, merged_code)

            save_profile(profile_file, user_id, str(profile))
            
def process_test_data(
    metadata_folder: str,
    problems: pd.DataFrame,
    profiles: pd.DataFrame,
    language: str,
    profile_file: str,
    reflection: bool,
    llm,
    model_type: str
) -> None:
    """
    Process the test dataset.

    Args:
        metadata_folder (str): Path to the base training metadata folder containing user_id subfolders.
        problems (pd.DataFrame): DataFrame containing problem data.
        profiles (pd.DataFrame): DataFrame containing user profiles.
        profile_file (str): Path to the profile CSV file.
        llm: The language model instance.
    """
    user_folders = [d for d in os.listdir(metadata_folder) if os.path.isdir(os.path.join(metadata_folder, d))]
    ref_codes = []
    gen_codes = []
    pre_scores = []
    real_scores = []
    all_lengths = []
    ideas = []
    positions = []
    use_reflection = reflection
    i = 0
    for user_id in tqdm(user_folders, desc="Processing users"):
        print(f"Processing user: {user_id}", flush=True)
        profile = profiles.loc[profiles['user_id'] == user_id, 'profile'].values[0]
        exercise_records = []

        user_folder_path = os.path.join(metadata_folder, user_id)
        for filename in os.listdir(user_folder_path):
            try:
                pattern = r"Problem_(\d+)_records"
                match = re.search(pattern, filename)
                if match:
                    problem_id = int(match.group(1))
                print(f"Processing problem: {problem_id}", flush=True)
                filepath = os.path.join(user_folder_path, filename)
                code_records = pd.read_csv(filepath)
                problem_info = get_problem_info(problems, problem_id)
                first_code_gen = generate_first_code_with_llm(llm, profile, problem_info, language, exercise_records)
                code_record_updated = first_code_gen['code']
                pre_score = first_code_gen['score']
                pre_scores.append(int(pre_score))
                gen_codes.append(code_record_updated)
                ref_codes.append(code_records['Code'][0])
                all_records = [f"1-th submission code:\n{code_records['Code'][0]}"]
                err_info = compile_code(code_records['Code'][0], language)
                real_scores.append(code_records['Score'][0])
                for j in range(1, len(code_records['Code'])):
                    code_update = update_code_with_llm(
                        llm, profile, problem_info, all_records, err_info, ''
                    )
                    # print("pre_code: ",code_records['Code'][j - 1])
                    code_record_updated = code_records['Code'][j - 1].replace(code_update['code0'], code_update['code1'])
                    # print("update_code1: ",code_record_updated)
                    if code_records['Code'][j - 1] == code_record_updated:
                        # print("No update")
                        code_record_updated = code_update['code']
                    # print("update_code2: ",code_record_updated)
                    if use_reflection:
                        code_record_updated = handle_reflection(
                            llm, profile, problem_info, all_records, code_record_updated, err_info
                        )
                    if language == "java":
                        if compile_code(code_record_updated, language) != "There is no compilation error.":
                            pre_scores.append(0)
                        else:
                            pre_score = code_update['score']
                            pre_scores.append(int(pre_score))
                    else:
                        pre_score = code_update['score']
                        pre_scores.append(int(pre_score))
                    # result = evaluate_with_llm(llm, code_records['Code'][j - 1], code_record_updated, code_records['Code'][j])
                    # ideas.append(result['idea'])
                    # positions.append(result['position'])
                    real_scores.append(code_records['Score'][j])
                    ref_codes.append(code_records['Code'][j])
                    gen_codes.append(code_record_updated)
                    err_info = compile_code(code_records['Code'][j], language)
                    all_records.append(f"{j + 1}-th submission code:\n{code_records['Code'][j]}")
                all_lengths.append(len(code_records['Code']))
                # print(pre_scores,flush=True)
                # print(real_scores,flush=True)
                merged_code = merge_codes(code_records['Code'].tolist())
                last_record = f"Problem information: {problem_info}\nCode records:\n{merged_code}"
                
                # profile = update_learner_profile_with_llm(llm, profile, merged_code)

                # output_file = f'results/experiments/{user_id}/output_code_{problem_id}.txt'
                # os.makedirs(os.path.dirname(output_file), exist_ok=True)
                # with open(output_file, 'w') as f:
                #     for record in all_records:
                #         f.write(record + '\n')
                
                if exercise_records:
                    exercise_records.pop(0)
                exercise_records.append(last_record)
            except Exception as e:
                print("Failed to process problem: ", e)
                continue
        i+=1
        if i >= 30:
            break
    # Calculate accuracy
    accuracy = accuracy_score(real_scores, pre_scores)
    print(f"Accuracy: {accuracy}")

    # Calculate AUC
    auc = roc_auc_score(real_scores, pre_scores)
    print(f"AUC: {auc}")
    # Calculate F1-score
    f1 = f1_score(real_scores, pre_scores, average='weighted')
    print(f"F1 Score: {f1}")
    with open(f'code_bleu_results_{language}_{model_type}.json', 'w') as f:
        json.dump({
            'ground_truth_codes': ref_codes,
            'generated_codes': gen_codes
        }, f, indent=4)
    with open(f'length_{language}_{model_type}.json', 'w') as f:
        json.dump({
            'all_lengths': all_lengths
        }, f, indent=4)
    codebleu_score, detailed_codebleu_score = compute_code_bleu(ref_codes, gen_codes, lang=language)
    print(f"CodeBLEU Score: {codebleu_score}")
    print(f"Detailed CodeBLEU Score: {detailed_codebleu_score}")
    # print(f"idea acc: {sum(ideas)/len(ideas)}, position acc: {sum(positions)/len(positions)}")