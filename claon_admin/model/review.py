from typing import List, Optional

from pydantic import BaseModel, validator


class ReviewAnswerRequestDto(BaseModel):
    answer_content: str

    @validator('answer_content')
    def validate_name(cls, value):
        if len(value) > 500:
            raise ValueError('답글은 500자 이하로 입력해 주세요.')
        return value


class ReviewAnswerResponseDto(BaseModel):
    review_answer_id: str
    content: str
    created_at: str
    review_id: str


class ReviewBriefResponseDto(BaseModel):
    review_id: str
    content: str
    created_at: str
    answer: Optional[ReviewAnswerResponseDto]
    user_id: str
    user_nickname: str
    user_profile_image: str
    user_visit_count: int
    tags: List[str]


class ReviewTagDto(BaseModel):
    tag: str
    count: int


class ReviewSummaryResponseDto(BaseModel):
    center_id: str
    center_name: str
    count_total: int
    count_not_answered: int
    count_answered: int
    review_count_by_tag_list: List[ReviewTagDto]
