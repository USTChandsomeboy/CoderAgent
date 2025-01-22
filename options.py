import argparse

parser = argparse.ArgumentParser([])
parser.add_argument("--dataset", choices=['CSEDM', 'CodeNet'], default='CSEDM')
parser.add_argument("--model", choices=['gpt4o', 'llama'], default='gpt4o')
parser.add_argument("--device", default='cuda:0')
parser.add_argument("--reflection", action="store_true", default=False)
parser.add_argument("--test", action="store_true", default=False)


args = parser.parse_args()
