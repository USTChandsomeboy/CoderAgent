import random
import json
import pickle
from tqdm import tqdm
import numpy as np
from options import args
import os
import re
import subprocess
import pandas as pd
import numpy as np
from base.llms import create_llm
from utils import set_seed, load_problems
from trainer import process_training_data, process_test_data

def main():
    """
    Main execution function to handle training and testing datasets.
    """
    # Initialize
    seed_list = [1024, 3145, 123, 321, 1513]
    set_seed(seed_list[0])

    
    llm = create_llm(backbone="gpt4o", deployment='gpt-4o-mini')
    dataset = args.dataset
    REFLECTION = args.reflection
    metadata_folder_base = f'dataset/{dataset}'
    problems = load_problems(f'dataset/{dataset}/problem_with_skills.csv')
    profile_file = f'dataset/{dataset}/profile.csv'
    profiles = pd.read_csv(profile_file)

    if args.test == False:
        metadata_folder = os.path.join(metadata_folder_base, 'train')
        process_training_data(metadata_folder, problems, profiles, profile_file, llm)

    elif args.test == True:
        metadata_folder = os.path.join(metadata_folder_base, 'test')
        process_test_data(metadata_folder, problems, profiles, profile_file, REFLECTION, llm)

    else:
        raise ValueError(f"Unsupported")


if __name__ == "__main__":
    main()