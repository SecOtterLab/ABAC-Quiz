# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List

# from abac_helper import evaluate_rules

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# DATA_FILE = "healthcare-data/healthcare-attribute-data.txt"

# # ---------------- ACL DATA ---------------- #

# ACL1 = {
#     "oncNurse1, oncPat1HR, modify",
#     "carNurse1, carPat1HR, modify",
#     "oncNurse2, oncPat2HR, modify",
#     "oncPat2, oncPat1HR, modify",
#     "carPat2, carPat1HR, modify",
#     "carNurse2, carPat2HR, modify",
#     "oncPat2, oncPat2HR, modify",
#     "carPat1, carPat2HR, modify",
#     "carPat1, carPat1HR, modify",
#     "oncPat1, oncPat2HR, modify",
#     "carNurse2, carPat1HR, modify",
#     "carPat2, carPat2HR, modify",
#     "oncNurse1, oncPat2HR, modify",
#     "oncPat1, oncPat1HR, modify",
#     "carNurse1, carPat2HR, modify",
#     "oncNurse2, oncPat1HR, modify",
# }

# ACL2 = {
#     "anesDoc1, oncPat1HR, modify",
#     "oncDoc4, oncPat2HR, modify",
#     "anesDoc1, carPat1HR, modify",
#     "carDoc1, carPat1HR, modify",
#     "oncDoc3, oncPat2HR, modify",
#     "carDoc2, carPat2HR, modify",
#     "oncDoc1, oncPat1HR, modify",
#     "oncDoc1, oncPat2HR, modify",
#     "oncDoc2, oncPat1HR, modify",
# }

# ACL3 = {
#     "oncPat2, oncPat2HR, modify",
#     "carPat2, carPat2HR, modify",
#     "carPat1, carPat1HR, modify",
#     "oncPat1, oncPat1HR, modify",
# }

# ACL4 = {
#     "oncAgent2, oncPat2HR, modify",
#     "carAgent1, carPat2HR, modify",
#     "carAgent1, carPat2HR, read",
#     "oncAgent2, oncPat2HR, read",
#     "oncAgent1, oncPat2HR, read",
#     "carAgent2, carPat2HR, read",
#     "oncAgent1, oncPat2HR, modify",
#     "carAgent2, carPat2HR, modify",
# }

# ACL5 = {
#     "oncDoc2, oncPat1oncItem, modify",
#     "oncDoc4, oncPat2oncItem, modify",
#     "carDoc2, carPat2carItem, modify",
#     "oncDoc3, oncPat2oncItem, modify",
#     "oncDoc1, oncPat2oncItem, modify",
#     "oncDoc1, oncPat1oncItem, modify",
#     "carDoc1, carPat1carItem, modify",
# }

# ACL6 = {
#     "doc2, carPat2carItem, delete",
#     "oncNurse2, oncPat1nursingItem, delete",
#     "carAgent1, carPat2noteItem, read",
#     "oncNurse1, oncPat2nursingItem, read",
#     "carNurse2, carPat2nursingItem, delete",
#     "doc1, oncPat2oncItem, read",
#     "carNurse2, carPat2nursingItem, read",
#     "oncNurse1, oncPat2nursingItem, delete",
#     "carNurse1, carPat1nursingItem, read",
#     "carPat1, carPat1noteItem, delete",
#     "carDoc2, carPat1carItem, delete",
#     "doc2, carPat2carItem, read",
#     "oncAgent1, oncPat2noteItem, delete",
#     "carAgent1, carPat2noteItem, delete",
#     "carDoc2, carPat1carItem, read",
#     "oncPat1, oncPat1noteItem, delete",
#     "oncAgent1, oncPat2noteItem, read",
#     "oncDoc1, oncPat1oncItem, delete",
#     "carNurse1, carPat1nursingItem, delete",
#     "carPat1, carPat1noteItem, read",
#     "oncDoc1, oncPat1oncItem, read",
#     "doc1, oncPat2oncItem, delete",
#     "oncPat1, oncPat1noteItem, read",
#     "oncNurse2, oncPat1nursingItem, read",
# }

# GT_ACL_LIST = [ACL1, ACL2, ACL3, ACL4, ACL5, ACL6]

# # ---------------- MODELS ---------------- #

# class Question(BaseModel):
#     question_number: int
#     subject_condition: str
#     resource_condition: str
#     constraint: str
#     actions: str


# class QuestionsRequest(BaseModel):
#     questions: List[Question]


# class BuiltRule(BaseModel):
#     subject_condition: str
#     resource_condition: str
#     constraint: str
#     actions: List[str]
#     rule_string: str


# class TestedQuestion(BaseModel):
#     question_number: int
#     subject_condition: str
#     resource_condition: str
#     constraint: str
#     actions: str
#     rule: BuiltRule


# class QuestionFeedback(BaseModel):
#     question_number: int
#     feedback_message: str
#     rule: BuiltRule


# class QuestionsResponse(BaseModel):
#     tested_questions: List[TestedQuestion]
#     results: List[QuestionFeedback]

# # ---------------- CLEANING (FIXED) ---------------- #

# def clean(text: str) -> str:
#     """
#     Only:
#     - strip leading/trailing whitespace
#     - collapse multiple spaces into a single space
#     """
#     return " ".join(text.strip().split())

# def parse_actions(actions: str) -> List[str]:
#     actions = actions.strip()
#     if not actions:
#         return []

#     parts = actions.replace(",", " ").split()
#     return [a for a in parts if a]

# # ---------------- RULE BUILDER ---------------- #

# def build_rule(question: Question) -> BuiltRule:
#     subject = clean(question.subject_condition)
#     resource = clean(question.resource_condition)
#     constraint = clean(question.constraint)
#     actions = parse_actions(question.actions)

#     action_str = " ".join(actions) if actions else ""
#     rule_string = f"rule({subject}; {resource}; {constraint}; {action_str})"

#     return BuiltRule(
#         subject_condition=subject,
#         resource_condition=resource,
#         constraint=constraint,
#         actions=actions,
#         rule_string=rule_string
#     )

# # ---------------- API ---------------- #

# @app.get("/hello")
# def hello():
#     return {"message": "hello"}

# @app.post("/feedback", response_model=QuestionsResponse)
# def feedback(payload: QuestionsRequest):
#     built_rules = [build_rule(q) for q in payload.questions]
#     rule_list = [r.rule_string for r in built_rules]

#     gt_acl_list = []
#     for q in payload.questions:
#         idx = q.question_number - 1
#         gt_acl_list.append(GT_ACL_LIST[idx] if 0 <= idx < len(GT_ACL_LIST) else set())

#     feedback_list = evaluate_rules(rule_list, gt_acl_list, DATA_FILE)

#     print("payload:", [q.model_dump() for q in payload.questions])
#     print("rules:", rule_list)
#     print("feedback:", feedback_list)

#     tested_questions = []
#     results = []

#     for i, q in enumerate(payload.questions):
#         rule = built_rules[i]

#         tested_questions.append(
#             TestedQuestion(
#                 question_number=q.question_number,
#                 subject_condition=q.subject_condition,
#                 resource_condition=q.resource_condition,
#                 constraint=q.constraint,
#                 actions=q.actions,
#                 rule=rule
#             )
#         )

#         results.append(
#             QuestionFeedback(
#                 question_number=q.question_number,
#                 feedback_message=str(feedback_list[i]) if i < len(feedback_list) else "No feedback returned.",
#                 rule=rule
#             )
#         )

#     return QuestionsResponse(
#         tested_questions=tested_questions,
#         results=results
#     )

# # ---------------- RUN ---------------- #

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=4989)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List

from abac_helper import evaluate_rules
from atomic import compare_atomic_rule, format_atomic_feedback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "healthcare-data/healthcare-attribute-data.txt"

# ---------------- ACL DATA ---------------- #

ACL1 = {
    "oncNurse1, oncPat1HR, modify",
    "carNurse1, carPat1HR, modify",
    "oncNurse2, oncPat2HR, modify",
    "carNurse2, carPat2HR, modify",
    "carNurse2, carPat1HR, modify",
    "oncNurse1, oncPat2HR, modify",
    "carNurse1, carPat2HR, modify",
    "oncNurse2, oncPat1HR, modify",
}

ACL2 = {
    "anesDoc1, oncPat1HR, modify",
    "oncDoc4, oncPat2HR, modify",
    "anesDoc1, carPat1HR, modify",
    "carDoc1, carPat1HR, modify",
    "oncDoc3, oncPat2HR, modify",
    "carDoc2, carPat2HR, modify",
    "oncDoc1, oncPat1HR, modify",
    "oncDoc1, oncPat2HR, modify",
    "oncDoc2, oncPat1HR, modify",
}

ACL3 = {
    "oncPat2, oncPat2HR, modify",
    "carPat2, carPat2HR, modify",
    "carPat1, carPat1HR, modify",
    "oncPat1, oncPat1HR, modify",
}

ACL4 = {
    "oncAgent2, oncPat2HR, modify",
    "carAgent1, carPat2HR, modify",
    "carAgent1, carPat2HR, read",
    "oncAgent2, oncPat2HR, read",
    "oncAgent1, oncPat2HR, read",
    "carAgent2, carPat2HR, read",
    "oncAgent1, oncPat2HR, modify",
    "carAgent2, carPat2HR, modify",
}

ACL5 = {
    "oncDoc2, oncPat1oncItem, modify",
    "oncDoc4, oncPat2oncItem, modify",
    "carDoc2, carPat2carItem, modify",
    "oncDoc3, oncPat2oncItem, modify",
    "oncDoc1, oncPat2oncItem, modify",
    "oncDoc1, oncPat1oncItem, modify",
    "carDoc1, carPat1carItem, modify",
}

ACL6 = {
    "doc2, carPat2carItem, delete",
    "oncNurse2, oncPat1nursingItem, delete",
    "carAgent1, carPat2noteItem, read",
    "oncNurse1, oncPat2nursingItem, read",
    "carNurse2, carPat2nursingItem, delete",
    "doc1, oncPat2oncItem, read",
    "carNurse2, carPat2nursingItem, read",
    "oncNurse1, oncPat2nursingItem, delete",
    "carNurse1, carPat1nursingItem, read",
    "carPat1, carPat1noteItem, delete",
    "carDoc2, carPat1carItem, delete",
    "doc2, carPat2carItem, read",
    "oncAgent1, oncPat2noteItem, delete",
    "carAgent1, carPat2noteItem, delete",
    "carDoc2, carPat1carItem, read",
    "oncPat1, oncPat1noteItem, delete",
    "oncAgent1, oncPat2noteItem, read",
    "oncDoc1, oncPat1oncItem, delete",
    "carNurse1, carPat1nursingItem, delete",
    "carPat1, carPat1noteItem, read",
    "oncDoc1, oncPat1oncItem, read",
    "doc1, oncPat2oncItem, delete",
    "oncPat1, oncPat1noteItem, read",
    "oncNurse2, oncPat1nursingItem, read",
}

GT_ACL_LIST = [ACL1, ACL2, ACL3, ACL4, ACL5, ACL6]

# ---------------- ATOMIC GROUND TRUTH ---------------- #
# subject_condition always has TWO valid options.
# Put the two accepted subject answers in the list below for each rule.

GT_ATOMIC_RULES: List[Dict[str, Any]] = [
    {
        "subject_condition": ["", "position [ {nurse}"],
        "resource_condition": "type [ {HR}",
        "constraint": "ward = ward",
        "actions": "modify",
    },
    {
        "subject_condition": ["", "position [ {doctor}"],
        "resource_condition": "type [ {HR}",
        "constraint": "teams ] treatingTeam",
        "actions": "modify",
    },
    {
        "subject_condition": ["", "position [ {patient}"],
        "resource_condition": "type [ {HR}",
        "constraint": "uid = patient",
        "actions": "modify",
    },
    {
        "subject_condition": ["", "position [ {agent}"],
        "resource_condition": "type [ {HR}",
        "constraint": "agentFor ] patient",
        "actions": "read modify",
    },
    {
        "subject_condition": ["", "position [ {doctor}"],
        "resource_condition": "type [ {HRitem}",
        "constraint": "teams ] treatingTeam, specialties > topics",
        "actions": "modify",
    },
    {
        "subject_condition": ["", ""],
        "resource_condition": "type [ {HRitem}",
        "constraint": "uid = author",
        "actions": "read delete",
    },
]

# ---------------- MODELS ---------------- #

class Question(BaseModel):
    question_number: int
    subject_condition: str
    resource_condition: str
    constraint: str
    actions: str


class QuestionsRequest(BaseModel):
    questions: List[Question]


class BuiltRule(BaseModel):
    subject_condition: str
    resource_condition: str
    constraint: str
    actions: List[str]
    rule_string: str


class AtomicSectionFeedback(BaseModel):
    is_correct: bool
    student_items: List[str]
    ground_truth_items: List[str]
    all_ground_truth_options: List[List[str]]
    correct_items: List[str]
    incorrect_items: List[str]
    missing_items: List[str]


class AtomicRuleFeedback(BaseModel):
    is_correct: bool
    sections: Dict[str, AtomicSectionFeedback]


class TestedQuestion(BaseModel):
    question_number: int
    subject_condition: str
    resource_condition: str
    constraint: str
    actions: str
    rule: BuiltRule
    atomic_feedback: AtomicRuleFeedback


class QuestionFeedback(BaseModel):
    question_number: int
    feedback_message: str
    atomic_feedback_message: str
    atomic_feedback: AtomicRuleFeedback
    rule: BuiltRule


class QuestionsResponse(BaseModel):
    tested_questions: List[TestedQuestion]
    results: List[QuestionFeedback]

# ---------------- CLEANING ---------------- #

def clean(text: str) -> str:
    """
    Only:
    - strip leading/trailing whitespace
    - collapse multiple spaces into a single space
    """
    return " ".join((text or "").strip().split())


def normalize_action_token(token: str) -> str:
    token = clean(token)
    token = token.strip("  ").strip()
    return token


def parse_actions(actions: str) -> List[str]:
    actions = clean(actions)
    if not actions:
        return []

    parts = actions.replace(",", " ").split()
    cleaned_parts = [normalize_action_token(part) for part in parts]
    return [part for part in cleaned_parts if part]

# ---------------- RULE BUILDER ---------------- #

def build_rule(question: Question) -> BuiltRule:
    subject = clean(question.subject_condition)
    resource = clean(question.resource_condition)
    constraint = clean(question.constraint)
    actions = parse_actions(question.actions)

    action_str = " ".join(actions) if actions else ""
    rule_string = f"rule({subject}; {resource}; {constraint}; {action_str})"

    return BuiltRule(
        subject_condition=subject,
        resource_condition=resource,
        constraint=constraint,
        actions=actions,
        rule_string=rule_string
    )


def build_student_atomic_rule(question: Question) -> Dict[str, str]:
    return {
        "subject_condition": clean(question.subject_condition),
        "resource_condition": clean(question.resource_condition),
        "constraint": clean(question.constraint),
        "actions": clean(question.actions),
    }


def get_gt_acl(question_number: int):
    idx = question_number - 1
    return GT_ACL_LIST[idx] if 0 <= idx < len(GT_ACL_LIST) else set()


def get_gt_atomic_rule(question_number: int) -> Dict[str, Any]:
    idx = question_number - 1
    if 0 <= idx < len(GT_ATOMIC_RULES):
        return GT_ATOMIC_RULES[idx]

    return {
        "subject_condition": ["", ""],
        "resource_condition": "",
        "constraint": "",
        "actions": "",
    }

# ---------------- API ---------------- #

@app.get("/hello")
def hello():
    return {"message": "hello"}


@app.post("/feedback", response_model=QuestionsResponse)
def feedback(payload: QuestionsRequest):
    built_rules = [build_rule(q) for q in payload.questions]
    rule_list = [r.rule_string for r in built_rules]

    gt_acl_list = []
    for q in payload.questions:
        idx = q.question_number - 1
        gt_acl_list.append(GT_ACL_LIST[idx] if 0 <= idx < len(GT_ACL_LIST) else set())

    feedback_list = evaluate_rules(rule_list, gt_acl_list, DATA_FILE)

    print("payload:", [q.model_dump() for q in payload.questions])
    print("rules:", rule_list)
    print("feedback:", feedback_list)

    tested_questions = []
    results = []

    for i, q in enumerate(payload.questions):
        rule = built_rules[i]

        student_atomic_rule = build_student_atomic_rule(q)
        gt_atomic_rule = get_gt_atomic_rule(q.question_number)

        atomic_raw = compare_atomic_rule(student_atomic_rule, gt_atomic_rule)
        atomic_feedback = AtomicRuleFeedback(
            is_correct=atomic_raw["is_correct"],
            sections={
                section_name: AtomicSectionFeedback(**section_data)
                for section_name, section_data in atomic_raw["sections"].items()
            }
        )
        atomic_feedback_message = format_atomic_feedback(atomic_raw)

        tested_questions.append(
            TestedQuestion(
                question_number=q.question_number,
                subject_condition=q.subject_condition,
                resource_condition=q.resource_condition,
                constraint=q.constraint,
                actions=q.actions,
                rule=rule,
                atomic_feedback=atomic_feedback
            )
        )

        results.append(
            QuestionFeedback(
                question_number=q.question_number,
                feedback_message=str(feedback_list[i]) if i < len(feedback_list) else "No feedback returned.",
                atomic_feedback_message=atomic_feedback_message,
                atomic_feedback=atomic_feedback,
                rule=rule
            )
        )

    return QuestionsResponse(
        tested_questions=tested_questions,
        results=results
    )

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4989)