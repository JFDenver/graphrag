# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""A module containing 'ResolvedEntity' and 'EntityResolutionResult' models."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from datashaper import VerbCallbacks

from graphrag.index.cache import PipelineCache

StrategyConfig = dict[str, Any]


@dataclass
class SummarizedDescriptionResult:
    """Entity summarization result class definition."""

    items: str | tuple[str, str]
    description: str


SummarizationStrategy = Callable[
    [
        str | tuple[str, str],
        list[str],
        VerbCallbacks,
        PipelineCache,
        StrategyConfig,
    ],
    Awaitable[SummarizedDescriptionResult],
]
