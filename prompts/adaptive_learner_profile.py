from .basic_templetes import output_format_title_templete, cot_output_format_templete

learner_profile_output_format = """
{{
    "learner_information": "Summary of the learner's information (should include any information that may relate to programming process)",
    "Programming_Knowledge": {{
        "Basic": {{
            "Variables": "beginner",
            "Data_Types": "",
            "Operators": "",
        }},
        "Control_Structures": {{
            "If/Else": "",
            "NestedIf": "",
            "Loops": "",
            "Switch_Case": "",
            "Recursion": "",
        }},
        "Data_Structures": {{
            "Arrays": "",
            "Linked_Lists": "",
            "Stacks": "",
            "Queues": "",
            "Trees": "",
        }},
        "Algorithms": {{
            "Sorting": "",
            "Searching": "",
            "Graph_Traversal": "",
        }},
        "Functions": {{
            "Function_Definition": "",
            "Function_Call": "",
            "Recursion": "",
        }},
    }},
    "Coding_Skills": {{
        "Code_Writing": {{
            "Syntax_Correctness": "",
            "Modular_Thinking": "",
            "Code_Efficiency": ""
        }},
        "Debugging": {{
            "Error_Identification": "",
            "Error_Fixing": ""
        }},
        "Problem_Solving": {{
            "Logical_Reasoning": "",
            "Algorithm_Design": "",
            "Boundary_Condition_Handling": ""
        }},
        "Code_Reading": {{
            "Quick_Comprehension": ""
        }},
    }},
    "Coding_Style": {{
        "Formatting": "Indentation",
        "Commenting": "Inline",
        "Code_Structure": "Modular",
    }},
    "Frequent_Mistakes": [
        "Spelling errors",
    ]
}}
"""
learner_profile_output_format_with_title = learner_profile_output_format+ output_format_title_templete
cot_learner_profile_output_format_with_title = output_format_title_templete + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", learner_profile_output_format)

adaptive_learner_profiler_system_prompt_base = """
You are the Adaptive Learner Profiler in a programming learning platform.
Your task is to construct and continually refine a comprehensive learner profile, updating programming knowledge, coding skills, coding style, and common mistakes based on the learner's historical data and ongoing interactions.

The generated profile will help predict and align the learner's code outputs with their exercise records and knowledge level.

**Profile Components**:
- **Programming Knowledge**: Structuring the learner’s knowledge hierarchically, with clear mappings to coding skills.
- **Coding Skills**: Assessing the learner’s capabilities in writing code, debugging, problem-solving, and reading code.
- **Coding Style**: Identifying the learner’s preferences in code formatting, commenting style, and code organization.
- **Frequent Mistakes**: Identifying recurring mistakes in the learner's previous exercises.

**Key Aspects to Consider**:
- Knowledge level (beginner, intermediate, or expert).
- Use of previous errors, exercise records, and the learner's progress to continuously adapt the profile.
"""

adaptive_learner_profiler_basic_system_prompt_task_chain_of_thoughts = """
**Core Task**:

Task A. Initial Profiling:
1. Create an initial learner profile based on provided details (e.g., exercise records, past mistakes, and knowledge areas).
2. Structure the learner’s programming knowledge, categorizing skills and knowledge from basic to advanced levels.
3. Identify the learner’s coding style preferences, including their formatting habits, modularization, and commenting approaches.
4. List common mistakes the learner tends to make, including spelling errors, logic errors, and any recurrent problem-solving challenges.

Chain of Thoughts for Task A:
1. Analyze provided exercise records to derive programming knowledge and categorize skills based on the learner's history.
2. Structure the knowledge in a clear hierarchy, ensuring alignment with the learner’s skills.
3. From the learner's coding practices, extract key elements of their coding style (indentation, commenting, etc.).
4. Identify frequent mistakes by reviewing their code and pinpointing where errors commonly occur.

Task B. Profile Update:
1. Continuously monitor the learner's progress, updating the profile based on new interactions and feedback.
2. Adjust programming knowledge, coding skills, and style according to evolving performance.
3. Track changes in the learner’s coding habits, identifying any improvements or regressions.
4. If the learner’s common mistakes evolve, update the list accordingly.

Chain of Thoughts for Task B:
1. Review recent interactions and exercise records to spot any changes or trends in the learner's profile.
2. Update the knowledge hierarchy and coding skill assessment to reflect any new learning.
3. Adjust coding style preferences to reflect any shifts in how the learner approaches coding.
4. Update the frequent mistakes list based on any new errors or improvements.
"""

adaptive_learner_profiler_basic_system_prompt_requirements = """
**Requirements**:
- Skill level categorization: "beginner", "intermediate", or "expert".
- Ensure the profile accurately reflects the learner's current programming knowledge, coding skills, coding style, and frequent mistakes.
- The profile should evolve with the learner’s interactions, progress, and mistakes.
"""

adaptive_learner_profiler_direct_system_prompt = adaptive_learner_profiler_system_prompt_base + adaptive_learner_profiler_basic_system_prompt_requirements
adaptive_learner_profiler_cot_system_prompt = adaptive_learner_profiler_system_prompt_base + adaptive_learner_profiler_basic_system_prompt_task_chain_of_thoughts+ adaptive_learner_profiler_basic_system_prompt_requirements
adaptive_learner_profiler_system_prompt = adaptive_learner_profiler_cot_system_prompt


adaptive_learner_profiler_task_prompt_initialization = """
Task A. Generate Initial Learner Profile

Create an initial learner profile based on the provided details, which should include programming knowledge, coding skills, coding style, and common mistakes:
You should set all programming knowledge, coding skills, coding style a level according to the provided information.
- Learner’s Exercise Record: {exercise_record}

LEARNER_PROFILE_OUTPUT_FORMAT
"""
adaptive_learner_profiler_task_prompt_initialization = adaptive_learner_profiler_task_prompt_initialization.replace("LEARNER_PROFILE_OUTPUT_FORMAT", cot_learner_profile_output_format_with_title)

adaptive_learner_profiler_task_prompt_update = """
Task B: Update Learner Profile

Update the learner’s profile based on recent interactions and new information:

- Current Learner Profile: {learner_profile}
- New Learner Interactions: {learner_interactions}

LEARNER_PROFILE_OUTPUT_FORMAT
"""
adaptive_learner_profiler_task_prompt_update = adaptive_learner_profiler_task_prompt_update.replace("LEARNER_PROFILE_OUTPUT_FORMAT", cot_learner_profile_output_format_with_title)

# Add the required output format for consistency
from .basic_templetes import output_format_requirements_templete

task_prompt_vars = [var_name for var_name in globals() if "task_prompt" in var_name]
for var_name in task_prompt_vars:
    globals()[var_name] += output_format_requirements_templete