from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class EmbeddingConfig(BaseSettings):
    model: str = Field(..., alias="EMBEDDING_MODEL")
    device: Optional[Literal["cpu", "cuda"]] = Field(default=None, alias="EMBEDDING_DEVICE")
    batch_size: Optional[int] = Field(default=8, alias="EMBEDDING_BATCH_SIZE")
    threshold: Optional[float] = Field(default=None, alias="EMBEDDING_THRESHOLD", ge=0.0, le=1.0)


