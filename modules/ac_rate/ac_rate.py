from base import Agent
from prompts import ac_rate_system_prompt, \
                    ac_rate_task_prompt
                    
class AcRate(Agent):

    def __init__(self, llm):
        super().__init__('AcRate', llm=llm, json_output=True, output_tracks=False)

    def analysis_ac_rate(self, input_dict):
        """
        - Problem Stem: {question}
        - Code: {code}
        """
        self.set_prompts(ac_rate_system_prompt, ac_rate_task_prompt)
        output = self.act(input_dict)
        return output


def analysis_ac_rate_with_llm(llm, question, code):
    ac_rate_analysiser= AcRate(llm)
    try:
        score = ac_rate_analysiser.analysis_ac_rate({
            "question": question,
            "code": code
        })
        return score
    except Exception as e:
        raise Exception(str(e))
