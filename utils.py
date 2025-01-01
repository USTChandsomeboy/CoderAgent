import random
import torch
import numpy as np
import os
import subprocess
import pandas as pd
from evaluator.CodeBLEU import calc_code_bleu


def set_seed(seed: int, cudnn: bool = True) -> None:
    """
    Seed all relevant libraries to ensure reproducibility.

    Args:
        seed (int): The seed value to set.
        cudnn (bool): Whether to set CuDNN to deterministic mode.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    if cudnn and seed is not None:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def save_profile(profile_file: str, user_id: str, profile: str) -> None:
    """
    Save or update a user's profile in the profile CSV file.

    Args:
        profile_file (str): Path to the profile CSV file.
        user_id (str): The user's unique identifier.
        profile (str): The profile data to save.
    """
    if os.path.exists(profile_file):
        profile_data = pd.read_csv(profile_file)
        if user_id in list(profile_data['user_id'].values):
            profile_data.loc[profile_data['user_id'] == user_id, 'profile'] = str(profile)
        else:
            new_row = pd.DataFrame({'user_id': [str(user_id)], 'profile': [profile]})
            profile_data = pd.concat([profile_data, new_row], ignore_index=True)
    else:
        profile_data = pd.DataFrame({'user_id': [str(user_id)], 'profile': [profile]})

    profile_data.to_csv(profile_file, index=False)

def load_problems(problem_file: str) -> pd.DataFrame:
    """
    Load problem data from a CSV file.

    Args:
        problem_file (str): Path to the problem CSV file.

    Returns:
        pd.DataFrame: DataFrame containing problem data.
    """
    return pd.read_csv(problem_file)

def merge_codes(codes: list) -> str:
    """
    Merge multiple code submissions into a single string.

    Args:
        codes (list): List of code strings.

    Returns:
        str: Merged code string with submission order.
    """
    merged_code = ""
    for index, code in enumerate(codes, start=1):
        merged_code += f"The {index}-th submission code:\n{code}\n\n"
    return merged_code


def compile_code(code: str, language: str) -> str:
    """
    Compile the given code based on the specified programming language.

    Args:
        code (str): The source code to compile.
        language (str): The programming language of the code.

    Returns:
        str: Compilation result or error message.
    """
    if language.lower() == 'python':
        return code
    elif language.lower() == 'java':
        class_name = "Solution"
        wrapped_code = f"public class {class_name} {{\n{code}\n}}"
        java_file = f"{class_name}.java"
        with open(java_file, 'w') as file:
            file.write(wrapped_code + '\n')
        compile_process = subprocess.run(["javac", java_file], capture_output=True, text=True)
        if compile_process.returncode != 0:
            return compile_process.stderr
        return "There is no compilation error."
    elif language.lower() == 'cpp':
        # Assuming the code needs no wrapping for C++
        return code
    else:
        raise ValueError(f"Unsupported language: {language}")


def compute_code_bleu(
    ground_truth_codes: list,
    generated_codes: list,
    lang: str = 'java'
) -> tuple:
    """
    Compute the CodeBLEU score between ground truth and generated codes.

    Args:
        ground_truth_codes (list): List of ground truth code strings.
        generated_codes (list): List of generated code strings.
        lang (str): Programming language of the codes.

    Returns:
        tuple: CodeBLEU score and detailed CodeBLEU score.
    """
    params = '0.25,0.25,0.25,0.25'
    codebleu_score, detailed_codebleu_score = calc_code_bleu.get_codebleu(
        pre_references=[ground_truth_codes],
        hypothesis=generated_codes,
        lang=lang,
        params=params
    )
    return codebleu_score, detailed_codebleu_score