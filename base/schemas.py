
from pydantic import BaseModel
from fastapi import File, UploadFile, Form


"""
:TODO: Restrict the input data types to the required ones

messages: dict
learner_profile: dict
llm_type: str

learning_goal: str
learner_information: dict

cv: file

skill_requirements: list
skill_gap: list

session_count: int
other_feedback: str

knowledge_point: dict
perspectives_of_knowledge_point: list
knowledge_perspective: list

drafts_of_perspectives: list

single_choice_count: int
multiple_choice_count: int
true_false_count: int
short_answer_count: int

use_search: bool
allow_parallel: bool
with_quiz: bool

learning_session: dict
knowledge_points: list

learning_document: dict
learning_path: list
"""




class ChatWithAutorRequest(BaseModel):

    messages: str
    learner_profile: str = ""
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class LearningGoalRefinementRequest(BaseModel):

    learning_goal: str
    learner_information: str = ""
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class Goal2KnowledgePrestrionRequest(BaseModel):

    learning_goal: str = Form(...),
    cv: UploadFile = File(...)
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class SkillGapIdentificationRequest(BaseModel):

    learning_goal: str
    learner_information: str
    skill_requirements: str = None
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class LearnerProfileInitializationWithInfoRequest(BaseModel):

    learning_goal: str
    learner_information: str
    skill_gap: str
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class LearnerProfileInitializationRequest(BaseModel):

    learning_goal: str
    skill_requirements: str
    skill_gap: str
    cv_path: str
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class LearnerProfileUpdateRequest(BaseModel):

    learner_profile: str
    learner_interactions: str
    learner_information: str = ""
    session_information: str = ""
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class LearningPathSchedulingRequest(BaseModel):

    learner_profile: str
    session_count: int
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class LearningPathReschedulingRequest(BaseModel):
    
    learner_profile: str
    learning_path: str
    session_count: int = -1
    other_feedback: str = ""
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class TailoredContentGenerationRequest(BaseModel):

    learner_profile: str
    learning_path: str
    knowledge_point: str
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class KnowledgePerspectiveExplorationRequest(BaseModel):

    learner_profile: str
    learning_path: str
    knowledge_point: str
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class KnowledgePerspectiveDraftingRequest(BaseModel):

    learner_profile: str
    learning_path: str
    knowledge_point: str
    perspectives_of_knowledge_point: str
    knowledge_perspective: str
    use_search: bool = True
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class KnowledgeDocumentIntegrationRequest(BaseModel):

    learner_profile: str
    learning_path: str
    knowledge_point: str
    perspectives_of_knowledge_point: str
    drafts_of_perspectives: str
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class PointPerspectivesDraftingRequest(BaseModel):

    learner_profile: str
    learning_path: str
    knowledge_point: str
    perspectives_of_knowledge_point: str
    use_search: bool
    allow_parallel: bool
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"
 

class KnowledgeQuizGenerationRequest(BaseModel):

    learner_profile: str
    learning_document: str
    single_choice_count: int = 3
    multiple_choice_count: int = 0
    true_false_count: int = 0
    short_answer_count: int = 0
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class TailoredContentGenerationRequest(BaseModel):

    learner_profile: str
    learning_path: str
    learning_session: str
    use_search: bool = True
    allow_parallel: bool = True
    with_quiz: bool = True
    llm_type: str = "gpt4o"
    method_name: str = "genmentor"


class KnowledgePointExplorationRequest(BaseModel):
    
    llm_type: str = "gpt4o"
    learner_profile: str
    learning_path: str
    learning_session: str
    method_name: str = "genmentor"

class KnowledgePointDraftingRequest(BaseModel):

    llm_type: str = "gpt4o"
    learner_profile: str
    learning_path: str
    learning_session: str
    knowledge_points: str
    knowledge_point: str
    use_search: bool
    method_name: str = "genmentor"

class KnowledgePointsDraftingRequest(BaseModel):

    llm_type: str = "gpt4o"
    learner_profile: str
    learning_path: str
    learning_session: str
    knowledge_points: str
    use_search: bool
    allow_parallel: bool
    method_name: str = "genmentor"

class LearningDocumentIntegrationRequest(BaseModel):

    llm_type: str = "gpt4o"
    learner_profile: str
    learning_path: str
    learning_session: str
    knowledge_points: str
    knowledge_drafts: str
    output_markdown: bool = False
    method_name: str = "genmentor"
    
