import os

output_data_dir = './data/output'
exp_results_dir = './results/experiments'
fig_save_dir = './results/figs'
vectorstore_dir = './data/vectorstore'

os.makedirs(output_data_dir, exist_ok=True)
os.makedirs(exp_results_dir, exist_ok=True)
os.makedirs(fig_save_dir, exist_ok=True)
os.makedirs(vectorstore_dir, exist_ok=True)
os.system(f'chmod -R 777 {vectorstore_dir}')
