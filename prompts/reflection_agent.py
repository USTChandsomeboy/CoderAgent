from .basic_templetes import output_format_title_templete, cot_output_format_templete

reflection_output_format = """
{{
    "reasonable": "Yes or No"
    "reason": ""
}}
"""
reflection_output_format_with_title = reflection_output_format + output_format_title_templete
cot_reflection_output_format_with_title = reflection_output_format_with_title + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", reflection_output_format_with_title)

reflection_system_prompt_base = """
You are an expert in coding education. There is a coding agent. The agent can generate next modified code based on student’s profile and last submitted code. Your task is to judge whether the student has the ability to modify the code in this way and whether the code modification aligns with the student's profile. 
If the modified code are reasonable, you should say ”Yes”. Otherwise, you should tell the agent: ”No” and and explain how the student should modify the code.

"""

reflection_system_prompt_task_chain_of_thoughts = """

Task 1. Think about whether the student has the ability to modify the code in this way
Task 2. Think about whether the code modification aligns with the student's profile

Chain of Thoughts for Task:
1. Assess the difficulty of the problem.
2. Analyze the agent's knowledge and ability.
3. Evaluate if the student has the required skills and knowledge to make the modification.
4. Consider if the modification is consistent with the student's profile and previous submissions.


"""

reflection_system_prompt = reflection_system_prompt_base + reflection_system_prompt_task_chain_of_thoughts + """
**Requirements**:
- Provide a detailed reasoning for your judgment.
- If the answer is "No", offer concrete suggestions for how the student can modify the code.
"""


reflection_task_prompt = """

Student's Profile : {profile}
Problem Stem: {question}
Previous code: {previous_code}
Modified code: {modified_code}


CODE_GENERATION_OUTPUT_FORMAT
"""

problem_information_task_prompt = reflection_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_reflection_output_format_with_title)

from .basic_templetes import output_format_requirements_templete

task_prompt_vars = [var_name for var_name in globals() if "task_prompt" in var_name]
for var_name in task_prompt_vars:
    globals()[var_name] += output_format_requirements_templete