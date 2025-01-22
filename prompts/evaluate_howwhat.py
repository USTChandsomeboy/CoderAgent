from .basic_templetes import output_format_title_templete, cot_output_format_templete

evaluate_output_format = """
{{
    "idea": 0~1,
    "position": 0~1
}}
"""
evaluate_output_format_with_title = evaluate_output_format + output_format_title_templete
cot_evaluate_output_format_with_title = evaluate_output_format + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", evaluate_output_format_with_title)

evaluate_system_prompt_base = """
You are an expert in programming. Your task is to determine whether the modification ideas of the simulated generated code are consistent with the students' real modification ideas, as well as whether the modification positions are the same.
"""

evaluate_system_prompt_task_chain_of_thoughts = """


Chain of Thoughts for Task:
1. Consider the modification ideas and positions of real students.
2. Consider the modification ideas and positions of simulated code modifications.
3. Determine whether the modification ideas of the simulated generated code are consistent with the students' real modification ideas.
4. Determine whether the modification positions are the same.


"""

evaluate_system_prompt = evaluate_system_prompt_base + evaluate_system_prompt_task_chain_of_thoughts 


evaluate_task_prompt = """

Previous Code: {previous_code}
Simulated Modified Code: {simulated_modified_code}
Real Modified Code: {real_modified_code}

CODE_GENERATION_OUTPUT_FORMAT
"""

evaluate_task_prompt = evaluate_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_evaluate_output_format_with_title)

from .basic_templetes import output_format_requirements_templete

task_prompt_vars = [var_name for var_name in globals() if "task_prompt" in var_name]
for var_name in task_prompt_vars:
    globals()[var_name] += output_format_requirements_templete