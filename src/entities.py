from typing_extensions import TypedDict

class CheckInput(TypedDict):

    ref_code: str
    candidate_code: str

class CheckResult(TypedDict):

    percent: str