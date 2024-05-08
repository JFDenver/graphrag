# Copyright (c) 2024 Microsoft Corporation.

"""Parameterization settings for the default configuration."""

from typing_extensions import NotRequired

from .llm_config_input import LLMConfigInput


class ClaimExtractionConfigInput(LLMConfigInput):
    """Configuration section for claim extraction."""

    enabled: NotRequired[bool | None]
    prompt: NotRequired[str | None]
    description: NotRequired[str | None]
    max_gleanings: NotRequired[int | str | None]
    strategy: NotRequired[dict | None]
