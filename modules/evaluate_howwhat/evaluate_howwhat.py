from base import Agent
from prompts import evaluate_system_prompt, \
                    evaluate_task_prompt
                    
class Evaluate_howwhat(Agent):

    def __init__(self, llm):
        super().__init__('Evaluate_howwhat', llm=llm, json_output=True, output_tracks=False)

    def evaluate_howwhat(self, input_dict):

        self.set_prompts(evaluate_system_prompt, evaluate_task_prompt)
        output = self.act(input_dict)
        return output


def evaluate_with_llm(llm, previous_code, simulated_modified_code, real_modified_code):
    evaluater= Evaluate_howwhat(llm)
    try:
        result = evaluater.evaluate_howwhat({
            "previous_code": previous_code,
            "simulated_modified_code": simulated_modified_code,
            "real_modified_code": real_modified_code
        })
        return result
    except Exception as e:
        raise Exception(str(e))
