from .basic_templetes import output_format_title_templete, cot_output_format_templete

reflection_output_format = """
{{
    "judgment": "Yes or No"
    "explanation": ""
}}
"""
reflection_output_format_with_title = reflection_output_format + output_format_title_templete
cot_reflection_output_format_with_title = reflection_output_format_with_title + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", reflection_output_format_with_title)

reflection_system_prompt_base = """
You are an expert in coding education. There is a coding agent. The agent can generate next modified code based on student’s profile and last submitted code. Your task is to judge whether the agent has the ability to modify the code in this way and whether the code modification aligns with the student's profile. 
If the modified code aligns with the student's abilities and habits, you should say ”Yes”. Otherwise, you should tell the agent: ”No” and and explain how the student should modify the code.

"""

reflection_system_prompt_task_chain_of_thoughts = """

Task 1: Evaluate whether the agent has the ability to modify the code in this way
- Consider the student's known strengths and weaknesses.
- Compare the complexity of the modification with their previous work and current skill level.

Task 2: Assess whether the code modification is consistent with the student's profile
- Reflect on the student's coding habits and common mistakes.
- Determine whether the change made reflects their typical approach or if it’s an unlikely shift in behavior.

Chain of Thoughts for Task:
1. Evaluate the difficulty of the task in comparison to the student's capabilities.
2. Assess the modification in terms of the student's existing knowledge and skills.

"""

reflection_system_prompt = reflection_system_prompt_base + reflection_system_prompt_task_chain_of_thoughts + """
**Requirements**:
- Provide a detailed, thoughtful reasoning for your judgment.
- If the answer is "No", offer specific guidance for how the student could realistically approach the modification.
"""


reflection_task_prompt = """

Student's Profile : {profile}
Problem Stem: {question}
Previous code: {previous_code}
Modified code: {modified_code}


CODE_GENERATION_OUTPUT_FORMAT
"""

reflection_task_prompt = reflection_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_reflection_output_format_with_title)

from .basic_templetes import output_format_requirements_templete

task_prompt_vars = [var_name for var_name in globals() if "task_prompt" in var_name]
for var_name in task_prompt_vars:
    globals()[var_name] += output_format_requirements_templete