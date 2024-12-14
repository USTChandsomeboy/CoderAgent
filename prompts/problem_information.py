from .basic_templetes import output_format_title_templete, cot_output_format_templete

problem_information_output_format = """
{{
    "Knowledge skill": {{
        "Variables": "beginner",
        ...
    }},
}}
"""
problem_information_output_format_with_title = problem_information_output_format + output_format_title_templete
cot_problem_information_output_format_with_title = problem_information_output_format + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", problem_information_output_format_with_title)

problem_information_system_prompt_base = """
You are the Problem Information Generator in a programming learning platform. Your task is to generate the knowledge and skills required for a given programming problem.
"""

problem_information_system_prompt_task_chain_of_thoughts = """
**Core Task**:

Task: generate the knowledge and skills required for a given programming problem.


Chain of Thoughts for Task:
1. Thinking about the diffculty of the problem.
2. Analyze which programming concepts or skills are required for this problem.


"""

problem_information_system_prompt = problem_information_system_prompt_base + problem_information_system_prompt_task_chain_of_thoughts + """
**Requirements**:
- Ensure that the generated knowledge and skills are consistent with the programming problem.

"""


problem_information_task_prompt = """


Problem Stem: {question}

CODE_GENERATION_OUTPUT_FORMAT
"""

problem_information_task_prompt = problem_information_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_problem_information_output_format_with_title)

from .basic_templetes import output_format_requirements_templete

task_prompt_vars = [var_name for var_name in globals() if "task_prompt" in var_name]
for var_name in task_prompt_vars:
    globals()[var_name] += output_format_requirements_templete