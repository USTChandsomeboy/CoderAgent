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
from base.llms import create_llm
from evaluator.CodeBLEU import calc_code_bleu
def set_seed(seed, cudnn=True):
    """
    Seed everything we can!
    Note that gym environments might need additional seeding (env.seed(seed)),
    and num_workers needs to be set to 1.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.random.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    # note: the below slows down the code but makes it reproducible
    if (seed is not None) and cudnn:
        torch.backends.cudnn.deterministic = True



def save_profile(profile_file, user_id, profile):
    if os.path.exists(profile_file):
        profile_data = pd.read_csv(profile_file)

        if user_id in profile_data['user_id'].values:
            profile_data.loc[profile_data['user_id'] == user_id, 'profile'] = profile
        else:
            new_row = pd.DataFrame({'user_id': [user_id], 'profile': [profile]})
            profile_data = pd.concat([profile_data, new_row], ignore_index=True)
    else:
        profile_data = pd.DataFrame({'user_id': [user_id], 'profile': [profile]})

    profile_data.to_csv(profile_file, index=False)
    
def code_merge(codes):
    merged_code = ''
    for i,code in enumerate(codes):
        merged_code += f"The {i+1}-th submission code: {code}   \n"
    return merged_code

def compile_code(code, language):
    if language == 'python':
        return code
    elif language == 'java':
        start = "public class Solution {\n"
        end = "\n}"
        code = start + code + end
        with open(f'Solution.java', 'w') as f:
                f.write(code + '\n')
        com_response = subprocess.run(["javac", "Solution.java"], capture_output=True, text=True)
        if com_response.returncode != 0:
            return com_response.stderr  
        else:
            return 'There is no compilation error'
    elif language == 'cpp':
        code = code.replace('int main', 'int main')
        return code

def compute_code_bleu(ground_truth_codes, generated_codes):
    print(f"ground_truth_codes: {ground_truth_codes}")
    print(f"generated_codes: {generated_codes}")
    params='0.25,0.25,0.25,0.25'
    lang='java'
    codebleu_score, detailed_codebleu_score = calc_code_bleu.get_codebleu(
                        pre_references=[ground_truth_codes], hypothesis=generated_codes, lang=lang, params=params)
    return codebleu_score, detailed_codebleu_score

seed_list = [1024, 3145, 123, 321, 1513]
set_seed(seed_list[0])
gpt4o_llm = create_llm(backbone="gpt4o", deployment='gpt-4o-mini')
metadata_folder = 'dataset/CSEDM/SingleRecords/1/'
problems = pd.read_csv('dataset/CSEDM/problem_with_skills.csv')

if args.dataset == 'train':
    user_id = '1'
    metadata_folder = f'dataset/CSEDM/SingleRecords/{user_id}/train'
    profile_file = 'dataset/CSEDM/profile.csv'
    profiles = pd.read_csv(profile_file)
    for i, filename in enumerate(os.listdir(metadata_folder)):
        match = match = re.search(r'(\d+)', filename)
        problem_id = '1'
        if match:
            problem_id = match.group(1)
        problem_id = int(problem_id)
        filepath = os.path.join(metadata_folder, filename)
        code_records = pd.read_csv(filepath)
        problem = problems[problems['ProblemID'] == problem_id]['Requirement'].values[0]
        problem_requireskill = problems[problems['ProblemID'] == problem_id]['RequirementSkill'].values[0]
        problem_info={
            'problem': problem,
            'problem_requireskill': problem_requireskill
        }
        merged_code = code_merge(code_records['Code'])
        
        if user_id in profiles['user_id']:
            profile = profiles[profiles[user_id] == user_id ]['profile'].values[0]
            profile = update_learner_profile_with_llm(gpt4o_llm, profile, merged_code)
        else:
            profile = initialize_learner_profile_with_llm(gpt4o_llm, merged_code)
        save_profile(profile_file, user_id, profile)

elif args.dataset == 'test':
    user_id = 1
    metadata_folder = f'dataset/CSEDM/SingleRecords/{user_id}/test'
    profile_file = 'dataset/CSEDM/profile.csv'
    profiles = pd.read_csv(profile_file)
    profile = profiles[profiles['user_id'] == user_id ]['profile'].values[0]
    print(profile)
    exercise_records = []
    ref_codes = []
    gen_codes = []
    for i, filename in enumerate(os.listdir(metadata_folder)):
        match = re.search(r'(\d+)', filename)
        result = '1'
        if match:
            result = match.group(1)
        problem_id = int(result)
        filepath = os.path.join(metadata_folder, filename)
        code_records = pd.read_csv(filepath)
        problem = problems[problems['ProblemID'] == problem_id]['Requirement'].values[0]
        problem_requireskill = problems[problems['ProblemID'] == problem_id]['RequirementSkill'].values[0]
        problem_info={
            'problem': problem,
            'problem_requireskill': problem_requireskill
        }
        merged_code = code_merge(code_records['Code'])
        last_record = f"problem information: {problem_info}   \n code records: {merged_code}"

        all_records = []
        code_record_current = code_records['Code'][0]
        all_records.append(f"1-th submission code: {code_records['Code'][0]}")
        err_info = compile_code(code_records['Code'][0], 'java')
        # code = generate_first_code_with_llm(gpt4o_llm, profile, problem, exercise_records)
        # code_records_current.append(code)
        for j in range(len(code_records['Code'])-1):
            ref_codes.append(code_records['Code'][j+1])
            code = update_code_with_llm(gpt4o_llm, profile, problem_info, exercise_records, code_record_current, err_info)
            code_record_current = code_record_current.replace(code['code0'], code['code1'])
            gen_codes.append(code_record_current)
            err_info = compile_code(code_record_current, 'java')
            all_records.append(f"{j+2}-th submission code: {code_record_current}")
            code_record_current = code_records['Code'][j+1]

        with open(f'results/experiments/output_code_{problem_id}.txt', 'w') as f:
            for record in all_records:
                f.write(record + '\n')
        if len(exercise_records) < 1:
            exercise_records.append(last_record)
        else:
            exercise_records.pop(0)
            exercise_records.append(last_record)        

    codebleu_score, de_codebleu_score = compute_code_bleu(ref_codes,gen_codes)
    print(f"codebleu_score: {codebleu_score}")
    print(f"de_codebleu_score: {de_codebleu_score}")