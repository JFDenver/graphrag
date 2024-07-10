"""Persona, entity type, relationships and domain generation prompts module."""

# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from .community_report_rating import GENERATE_REPORT_RATING_PROMPT
from .community_reporter_role import GENERATE_COMMUNITY_REPORTER_ROLE_PROMPT
from .domain import GENERATE_DOMAIN_PROMPT
from .entity_relationship import (
    ENTITY_RELATIONSHIPS_GENERATION_JSON_PROMPT,
    ENTITY_RELATIONSHIPS_GENERATION_PROMPT,
    UNTYPED_ENTITY_RELATIONSHIPS_GENERATION_PROMPT,
)
from .entity_types import (
    ENTITY_TYPE_GENERATION_JSON_PROMPT,
    ENTITY_TYPE_GENERATION_PROMPT,
)
from .persona import GENERATE_PERSONA_PROMPT

__all__ = [
    "ENTITY_RELATIONSHIPS_GENERATION_JSON_PROMPT",
    "ENTITY_RELATIONSHIPS_GENERATION_PROMPT",
    "ENTITY_TYPE_GENERATION_JSON_PROMPT",
    "ENTITY_TYPE_GENERATION_PROMPT",
    "GENERATE_COMMUNITY_REPORTER_ROLE_PROMPT",
    "GENERATE_DOMAIN_PROMPT",
    "GENERATE_PERSONA_PROMPT",
    "GENERATE_REPORT_RATING_PROMPT",
    "UNTYPED_ENTITY_RELATIONSHIPS_GENERATION_PROMPT",
]