from base import Agent
from prompts import adaptive_learner_profiler_system_prompt, \
                    adaptive_learner_profiler_task_prompt_initialization, \
                    adaptive_learner_profiler_task_prompt_update


class AdaptiveLearnerProfiler(Agent):

    def __init__(self, llm):
        super().__init__('AdaptiveLearnerProfiler', llm=llm, json_output=True, output_tracks=False)

    def initialize_profile(self, input_dict):
        """
        - Exercise Record: {exercise_record}
        - Learner Information: {learner_information}
        """
        self.set_prompts(adaptive_learner_profiler_system_prompt, adaptive_learner_profiler_task_prompt_initialization)
        output = self.act(input_dict)
        return output

    def update_profile(self, input_dict):
        """
        - Learner's Initial Profile: {learner_profile}
        - New Learner Interactions: {learner_interactions}
        """
        self.set_prompts(adaptive_learner_profiler_system_prompt, adaptive_learner_profiler_task_prompt_update)
        return self.act(input_dict)


def initialize_learner_profile_with_llm(llm, exercise_record, learner_information):
    learner_profiler = AdaptiveLearnerProfiler(llm)
    try:
        learner_profile = learner_profiler.initialize_profile({
            "exercise_record": exercise_record,
            "learner_information": learner_information,
        })
        return learner_profile
    except Exception as e:
        raise Exception(str(e))

def update_learner_profile_with_llm(llm, learner_profile, learner_interactions):
    learner_profiler = AdaptiveLearnerProfiler(llm)
    try:
        learner_profile = learner_profiler.update_profile({
            "learner_profile": learner_profile,
            "learner_interactions": learner_interactions,
        })
        return learner_profile
    except Exception as e:
        raise Exception(str(e))