from base import Agent
from prompts import code_generation_system_prompt, \
                    code_generation_task_prompt_first, \
                    code_generation_task_prompt_update
                    
class CodeGeneration(Agent):

    def __init__(self, llm):
        super().__init__('CodeGeneration', llm=llm, json_output=True, output_tracks=False)

    def generate_first_code(self, input_dict):
        """
        - Learner Information: {learner_information}
        - Question Information: {question_information}
        """
        self.set_prompts(code_generation_system_prompt, code_generation_task_prompt_first)
        output = self.act(input_dict)
        return output

    def code_update(self, input_dict):
        """
        - Learner's Profile: {learner_profile}
        - Question Information: {question_information}
        - Previous Codes Records: {code_records}
        - Error Information: {error_information}
        """
        self.set_prompts(code_generation_system_prompt, code_generation_task_prompt_update)
        return self.act(input_dict)


def generate_first_code_with_llm(llm, learner_profile, question_information):
    code_generater= CodeGeneration(llm)
    try:
        first_code = code_generater.generate_first_code({
            "learner_profile": learner_profile,
            "question_information": question_information,
        })
        return first_code
    except Exception as e:
        raise Exception(str(e))

def update_code_with_llm(llm, learner_profile, question_information, code_records, error_information):
    code_generater = CodeGeneration(llm)
    try:
        update_code = code_generater.code_update({
            "learner_profile": learner_profile,
            "question_information": question_information,
            "code_records": code_records,
            "error_information": error_information,
        })
        return update_code
    except Exception as e:
        raise Exception(str(e))