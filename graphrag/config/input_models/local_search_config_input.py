# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""Parameterization settings for the default configuration."""

from typing_extensions import NotRequired, TypedDict


class LocalSearchConfigInput(TypedDict):
    """The default configuration section for Cache."""

    text_unit_prop: NotRequired[float | str | None]
    community_prop: NotRequired[float | str | None]
    conversation_history_max_turns: NotRequired[int | str | None]
    top_k_mapped_entities: NotRequired[int | str | None]
    top_k_mapped_relationships: NotRequired[int | str | None]
    max_tokens: NotRequired[int | str | None]
