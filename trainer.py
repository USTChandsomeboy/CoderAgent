import random
import json
import pickle
from tqdm import tqdm
import torch
import torch.nn.functional as F
from torch.optim import Adam
import numpy as np
from options import args
import os
import re
import subprocess
import pandas as pd
import numpy as np
from modules.adaptive_learner_modeling import *
from modules.learner_simulation import *
from modules.question_analysis import *
from modules.reflection_agent import *
from modules.ac_rate import *
from base.llms import create_llm
from utils import save_profile, merge_codes, compile_code, compute_code_bleu



def get_problem_info(problems: pd.DataFrame, problem_id: int) -> dict:
    """
    Retrieve problem information based on problem ID.

    Args:
        problems (pd.DataFrame): DataFrame containing problem data.
        problem_id (int): The ID of the problem.

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
        print(reflection_times)
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
    Process the training dataset.

    Args:
        metadata_folder (str): Path to the training metadata folder.
        problems (pd.DataFrame): DataFrame containing problem data.
        profiles (pd.DataFrame): DataFrame containing user profiles.
        profile_file (str): Path to the profile CSV file.
        llm: The language model instance.
    """
    user_id = '1'
    for filename in tqdm(os.listdir(metadata_folder), desc="Processing training data"):
        match = re.search(r'(\d+)', filename)
        problem_id = int(match.group(1)) if match else 1

        filepath = os.path.join(metadata_folder, filename)
        code_records = pd.read_csv(filepath)

        problem_info = get_problem_info(problems, problem_id)
        merged_code = merge_codes(code_records['Code'].tolist())

        if user_id in profiles['user_id'].values:
            profile = profiles.loc[profiles['user_id'] == user_id, 'profile'].values[0]
            profile = update_learner_profile_with_llm(llm, profile, merged_code)
        else:
            profile = initialize_learner_profile_with_llm(llm, merged_code)

        save_profile(profile_file, user_id, profile)
        
def process_test_data(
    metadata_folder: str,
    problems: pd.DataFrame,
    profiles: pd.DataFrame,
    profile_file: str,
    llm
) -> None:
    """
    Process the test dataset.

    Args:
        metadata_folder (str): Path to the test metadata folder.
        problems (pd.DataFrame): DataFrame containing problem data.
        profiles (pd.DataFrame): DataFrame containing user profiles.
        profile_file (str): Path to the profile CSV file.
        llm: The language model instance.
    """
    user_id = '1'
    profile = profiles.loc[profiles['user_id'] == user_id, 'profile'].values[0]
    print(profile)

    exercise_records = []
    ref_codes = []
    gen_codes = []
    pre_scores = []
    use_reflection = False

    for filename in tqdm(os.listdir(metadata_folder), desc="Processing test data"):
        match = re.search(r'(\d+)', filename)
        problem_id = int(match.group(1)) if match else 1

        filepath = os.path.join(metadata_folder, filename)
        code_records = pd.read_csv(filepath)

        problem_info = get_problem_info(problems, problem_id)
        merged_code = merge_codes(code_records['Code'].tolist())
        last_record = f"Problem information: {problem_info}\nCode records:\n{merged_code}"

        all_records = [f"1-th submission code:\n{code_records['Code'][0]}"]
        err_info = compile_code(code_records['Code'][0], 'java')

        for j in range(1, len(code_records['Code'])):
            ref_codes.append(code_records['Code'][j])
            code_update = update_code_with_llm(
                llm, profile, problem_info, all_records, err_info, ''
            )
            code_record_updated = code_records['Code'][j - 1].replace(code_update['code0'], code_update['code1'])

            if use_reflection:
                code_record_updated = handle_reflection(
                    llm, profile, problem_info, all_records, code_record_updated, err_info
                )

            gen_codes.append(code_record_updated)
            err_info = compile_code(code_record_updated, 'java')
            all_records.append(f"{j + 1}-th submission code:\n{code_record_updated}")

        pre_score = analysis_ac_rate_with_llm(llm, problem_info['problem'], code_record_updated)
        pre_scores.append(pre_score)
        profile = update_learner_profile_with_llm(llm, profile, merged_code)

        output_file = f'results/experiments/output_code_{problem_id}.txt'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            for record in all_records:
                f.write(record + '\n')

        if exercise_records:
            exercise_records.pop(0)
        exercise_records.append(last_record)

    codebleu_score, detailed_codebleu_score = compute_code_bleu(ref_codes, gen_codes, lang='java')
    print(f"CodeBLEU Score: {codebleu_score}")
    print(f"Detailed CodeBLEU Score: {detailed_codebleu_score}")