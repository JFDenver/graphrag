# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""Parameterization settings for the default configuration."""

from pydantic import Field

from .llm_config_model import LLMConfigModel


class SummarizeDescriptionsConfigModel(LLMConfigModel):
    """Configuration section for description summarization."""

    prompt: str | None = Field(
        description="The description summarization prompt to use.", default=None
    )
    max_length: int | None = Field(
        description="The description summarization maximum length.", default=500
    )
    strategy: dict | None = Field(
        description="The override strategy to use.", default=None
    )
