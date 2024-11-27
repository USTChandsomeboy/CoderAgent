
from pydantic import BaseModel
from fastapi import File, UploadFile, Form


class ChatWithAutorRequest(BaseModel):

    messages: dict
    learner_profile: dict = {}
    llm_type: str = "gpt4o"


class LearningGoalRefinementRequest(BaseModel):

    learning_goal: str
    learner_information: str = ""
    llm_type: str = "gpt4o"


class Goal2KnowledgePredictionRequest(BaseModel):

    learning_goal: str = Form(...),
    cv: UploadFile = File(...)
    llm_type: str = "gpt4o"


class SkillGapIdentificationRequest(BaseModel):

    learning_goal: str
    learner_information: str
    skill_requirements: list = None
    llm_type: str = "gpt4o"


class LearnerProfileInitializationWithInfoRequest(BaseModel):

    learning_goal: str
    learner_information: str
    skill_gap: list
    llm_type: str = "gpt4o"


class LearnerProfileInitializationRequest(BaseModel):

    learning_goal: str
    skill_requirements: list
    skill_gap: list
    cv_path: str
    llm_type: str = "gpt4o"


class LearnerProfileUpdateRequest(BaseModel):

    learner_profile: dict
    learner_interactions: dict
    learner_information: str = ""
    llm_type: str = "gpt4o"


class LearningPathSchedulingRequest(BaseModel):

    learner_profile: dict
    session_count: int = -1
    llm_type: str = "gpt4o"


class LearningPathReschedulingRequest(BaseModel):
    
    learner_profile: dict
    learning_path: dict
    session_count: int = -1
    other_feedback: str = ""
    llm_type: str = "gpt4o"


class TailoredContentGenerationRequest(BaseModel):

    learner_profile: dict
    learning_path: dict
    knowledge_point: dict
    llm_type: str = "gpt4o"


class KnowledgePerspectiveExplorationRequest(BaseModel):

    learner_profile: dict
    learning_path: dict
    knowledge_point: dict
    llm_type: str = "gpt4o"


class KnowledgePerspectiveDraftingRequest(BaseModel):

    learner_profile: dict
    learning_path: dict
    knowledge_point: dict
    perspectives_of_knowledge_point: dict
    knowledge_perspective: str
    use_search: bool = True
    llm_type: str = "gpt4o"


class KnowledgeDocumentIntegrationRequest(BaseModel):

    learner_profile: dict
    learning_path: dict
    knowledge_point: dict
    perspectives_of_knowledge_point: dict
    drafts_of_perspectives: str
    llm_type: str = "gpt4o"

class PointPerspectivesDraftingRequest(BaseModel):

    learner_profile: dict
    learning_path: dict
    knowledge_point: dict
    perspectives_of_knowledge_point: dict
    use_search: bool
    allow_parallel: bool
    llm_type: str = "gpt4o"
 

class KnowledgeQuizGenerationRequest(BaseModel):

    learner_profile: dict
    knowledge_document: str
    single_choice_count: int = 3
    multiple_choice_count: int = 0
    true_false_count: int = 0
    short_answer_count: int = 0
    llm_type: str = "gpt4o"


class TailoredContentGenerationRequest(BaseModel):

    learner_profile: dict
    learning_path: dict
    knowledge_point: dict
    use_search: bool = True
    allow_parallel: bool = True
    with_quiz: bool = True
    llm_type: str = "gpt4o"


class KnowledgePointExplorationRequest:
    
    llm_type: str
    learner_profile: dict
    learning_path: list
    knowledge_point: dict

class KnowledgePointDraftingRequest:

    llm_type: str
    learner_profile: dict
    learning_path: list
    learning_session: list
    knowledge_points: list
    knowledge_point: dict
    use_search: bool

class KnowledgePointsDraftingRequest:

    llm_type: str
    learner_profile: dict
    learning_path: list
    learning_session: list
    knowledge_points: list
    use_search: bool
    allow_parallel: bool

class LearningDocumentIntegrationRequest:

    llm_type: str
    learner_profile: dict
    learning_path: list
    learning_session: list
    knowledge_points: list
    knowledge_drafts: list
