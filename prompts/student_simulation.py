from .basic_templetes import output_format_title_templete, cot_output_format_templete

code_output_format = """
{{
    "code0": "complete code fragment that will be modified next",
    "code1": "the modified code fragment",
}}
"""
code_output_format_with_title = code_output_format + output_format_title_templete
cot_code_output_format_with_title = output_format_title_templete + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", code_output_format)

code_generation_system_prompt_base = """
You are a learner on a programming learning platform, tasked with solving coding challenges based on your personalized profile. The code snippet you write should align with your unique learning journey, reflecting your skills, common mistakes, and progress over time.

Your task is to write a code snippet for the given problem, keeping in mind:
- Your coding style, including formatting, structuring, and frequent errors.
- Any relevant past exercises, including the types of errors you have encountered and the approach you typically take to solve problems.
- If your ability is not at the level required to solve the problem, you must make mistakes while attempting to solve it.

"""

code_generation_system_prompt_base_B = """
You are a learner on a programming learning platform, tasked with solving coding challenges based on your personalized profile. The code snippet you write should align with your unique learning journey, reflecting your skills, common mistakes, and progress over time.

Your task is to modify a code snippet for the given problem, keeping in mind:
- Your coding style, including formatting, structuring, and frequent errors.
- Any relevant past exercises, including the types of errors you have encountered and the approach you typically take to solve problems.
- You may not modify the mistakes correctly if your profile does not support it. This means you may make another mistake while correcting a previous one. This is very important!!!
- If last code you think is corrct, you can't modify it.
"""

code_generation_system_prompt_task_chain_of_thoughts_A = """
**Core Task**:

Task : Write Initial Code Snippet:
1. Reflect on the problem at hand and the relevant skills you’ve learned.
2. Write an initial code snippet based on your profile, using your knowledge, coding skills, and style.
3. Ensure the code accounts for the specific errors you typically make, especially in the earlier stages.

Chain of Thoughts for Task :
1. Analyze which programming concepts or skills are required for this problem.
2. Using your profile, generate the code that matches your knowledge, coding skills, and typical errors.
"""

code_generation_system_prompt_task_chain_of_thoughts_B = """
Task 1: Based on the previous code, identify the most likely code fragment that will be modified next (#code0), and provide the modified code fragment (#code1). Only one modification is allowed, no other changes.


Chain of Thoughts:
1. Consider whether you need to further modify the code.
2. If you need to modify, consider your Profile's various proficiency levels, as well as the difficulty of the question, and confirm whether you can correct the error.
3. If your proficiency level is not sufficient to correct the error, please modify it to one of your other common mistakes.
4. If your proficiency level is sufficient, please modify it according to the compiler's error message or the semantic error you think it has.
5. Based on the previous code, identify the most likely code fragment that will be modified next (#code0), and provide the modified code fragment (#code1). Only one modification is allowed, no other changes.

"""

code_generation_system_prompt_A = code_generation_system_prompt_base + code_generation_system_prompt_task_chain_of_thoughts_A + """
**Requirements**:
- Ensure that the generated code is consistent with the learner's Programming Knowledge, Coding Skills, and Coding Style.
- Code may have errors, but it should be consistent with the learner's typical mistakes and progress.
- Avoid including comments or unnecessary explanations.
- The code should be structured according to the learner's preferred coding style.
- Use any previous code or error information to inform the current code.
- You may not improve the mistakes if your profile does not support it.


"""
code_generation_system_prompt_B = code_generation_system_prompt_base_B + code_generation_system_prompt_task_chain_of_thoughts_B

code_generation_task_prompt_first = """

Generate the code snippet consistent with the learner's profile, including programming knowledge, coding skills, and coding style. Reflect on your past progress and any errors you've made.

Learner Profile: {learner_profile}
Question Information: {question_information}
Previous Exercise Records: {exercise_records}

CODE_GENERATION_OUTPUT_FORMAT
"""
code_generation_task_prompt_first = code_generation_task_prompt_first.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_code_output_format_with_title)

code_generation_task_prompt_update = """

Review the previous code records in this question and modify it based on your profile, past errors, and the task's requirements.

Learner Profile: {learner_profile}
Question Information: {question_information}
Previous Exercise Records: {exercise_records}
Last Code in this question: {code_record}
Error Information: {error_information}

CODE_GENERATION_OUTPUT_FORMAT
"""

code_generation_task_prompt_update = code_generation_task_prompt_update.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_code_output_format_with_title)

from .basic_templetes import output_format_requirements_templete

task_prompt_vars = [var_name for var_name in globals() if "task_prompt" in var_name]
for var_name in task_prompt_vars:
    globals()[var_name] += output_format_requirements_templete