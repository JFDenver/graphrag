# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""Parameterization settings for the default configuration."""

from pydantic import BaseModel, Field

from graphrag.index.default_config.parameters.defaults import (
    DEFAULT_CHUNK_GROUP_BY_COLUMNS,
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
)
from graphrag.index.verbs.text.chunk import ChunkStrategyType


class ChunkingConfigModel(BaseModel):
    """Configuration section for chunking."""

    size: int = Field(description="The chunk size to use.", default=DEFAULT_CHUNK_SIZE)
    overlap: int = Field(
        description="The chunk overlap to use.", default=DEFAULT_CHUNK_OVERLAP
    )
    group_by_columns: list[str] = Field(
        description="The chunk by columns to use.",
        default=DEFAULT_CHUNK_GROUP_BY_COLUMNS,
    )
    strategy: dict | None = Field(
        description="The chunk strategy to use, overriding the default tokenization strategy",
        default=None,
    )

    def resolved_strategy(self) -> dict:
        """Get the resolved chunking strategy."""
        return self.strategy or {
            "type": ChunkStrategyType.tokens,
            "size": self.size,
            "overlap": self.overlap,
            "group_by_columns": self.group_by_columns,
        }
