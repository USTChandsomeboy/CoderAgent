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
    metadata_folder_base = 'dataset/CSEDM/SingleRecords/'
    problems = load_problems('dataset/CSEDM/problem_with_skills.csv')

    profile_file = 'dataset/CSEDM/profile.csv'
    profiles = pd.read_csv(profile_file)

    if args.dataset == 'train':
        metadata_folder = os.path.join(metadata_folder_base, '1', 'train')
        process_training_data(metadata_folder, problems, profiles, profile_file, llm)

    elif args.dataset == 'test':
        metadata_folder = os.path.join(metadata_folder_base, '1', 'test')
        process_test_data(metadata_folder, problems, profiles, profile_file, llm)

    else:
        raise ValueError(f"Unsupported dataset type: {args.dataset}")


if __name__ == "__main__":
    main()