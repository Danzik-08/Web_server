from pydantic import BaseModel
from typing import List, Optional


class MLConfig(BaseModel):
    model: str
    task: str
    name: str  # name for file model
    params: Optional[dict]


class BodyFit(BaseModel):
    X: List[List[float]]
    y: List[float]
    config: MLConfig


class BodyPredict(BaseModel):
    X: List[List[float]]
    config: MLConfig


