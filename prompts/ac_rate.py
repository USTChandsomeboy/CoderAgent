from .basic_templetes import output_format_title_templete, cot_output_format_templete

ac_rate_output_format = """
{{
    "score": 0 ~ 1,
}}
"""
ac_rate_output_format_with_title = ac_rate_output_format + output_format_title_templete
cot_ac_rate_output_format_with_title = ac_rate_output_format + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", ac_rate_output_format_with_title)

ac_rate_system_prompt_base = """
You are the code educator in a programming learning platform. Your task is to predict whether the student will get correct (AC) or not."""

ac_rate_system_prompt_task_chain_of_thoughts = """
**Core Task**:

Task: Predict whether the student will get correct (AC) or not.

Chain of Thoughts for Task:
1. Analyze the code records and the problem statement.
2. You need to consider whether the student's problem-solving approach throughout the entire process is correct. If yes, the student will get AC; otherwise, the student will not get AC.


"""

ac_rate_system_prompt = ac_rate_system_prompt_base + ac_rate_system_prompt_task_chain_of_thoughts + """
**Requirements**:
- The result should between 0 and 1.
"""


ac_rate_task_prompt = """


Problem Stem: {question}
Student's Code Records: {code}


CODE_GENERATION_OUTPUT_FORMAT
"""

ac_rate_task_prompt = ac_rate_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_ac_rate_output_format_with_title)

from .basic_templetes import output_format_requirements_templete

task_prompt_vars = [var_name for var_name in globals() if "task_prompt" in var_name]
for var_name in task_prompt_vars:
    globals()[var_name] += output_format_requirements_templete