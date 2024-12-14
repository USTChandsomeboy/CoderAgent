from base import Agent
from prompts import problem_information_system_prompt, \
                    problem_information_task_prompt
                    
class QuestionAnalysis(Agent):

    def __init__(self, llm):
        super().__init__('QuestionAnalysis', llm=llm, json_output=True, output_tracks=False)

    def analysis_question(self, input_dict):
        """
        - Problem Stem: {question}
        """
        self.set_prompts(problem_information_system_prompt, problem_information_task_prompt)
        output = self.act(input_dict)
        return output


def generate_first_code_with_llm(llm, question):
    question_analysiser= QuestionAnalysis(llm)
    try:
        first_code = question_analysiser.analysis_question({
            "question": question,
        })
        return first_code
    except Exception as e:
        raise Exception(str(e))
