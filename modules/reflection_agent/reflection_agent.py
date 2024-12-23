from base import Agent
from prompts import reflection_system_prompt, \
                    reflection_task_prompt
                    
class ReflectionAgent(Agent):

    def __init__(self, llm):
        super().__init__('ReflectionAgent', llm=llm, json_output=True, output_tracks=False)

    def reflection_codes(self, input_dict):
        """
        - Student's Profile : {profile}
        - Problem Stem: {question}
        - Previous code: {previous_code}
        - Modified code: {modified_code}
        """
        self.set_prompts(reflection_system_prompt, reflection_task_prompt)
        output = self.act(input_dict)
        return output


def analysis_question_with_llm(llm, profile, question, previous_code, modified_code):
    reflectionAgent= ReflectionAgent(llm)
    try:
        reflection = reflectionAgent.reflection_codes({
            "profile": profile,
            "question": question,
            "previous_code": previous_code,
            "modified_code": modified_code,
        })
        return reflection
    except Exception as e:
        raise Exception(str(e))
