# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""A module containing create_community_reports and load_strategy methods definition."""

import logging
from enum import Enum
from typing import cast

import pandas as pd
from datashaper import (
    AsyncType,
    NoopVerbCallbacks,
    TableContainer,
    VerbCallbacks,
    VerbInput,
    derive_from_rows,
    progress_ticker,
    verb,
)

import graphrag.config.defaults as defaults
import graphrag.index.graph.extractors.community_reports.schemas as schemas
from graphrag.index.cache import PipelineCache
from graphrag.index.graph.extractors.community_reports import (
    prep_community_report_context,
)

from .strategies.typing import CommunityReport, CommunityReportsStrategy

log = logging.getLogger(__name__)

_NAMED_INPUTS_REQUIRED = "Named inputs are required"


class CommunityReportsStrategyType(str, Enum):
    """CommunityReportsStrategyType class definition."""

    graph_intelligence = "graph_intelligence"


@verb(name="create_community_reports")
async def create_community_reports(
    input: VerbInput,
    callbacks: VerbCallbacks,
    cache: PipelineCache,
    strategy: dict,
    async_mode: AsyncType = AsyncType.AsyncIO,
    num_threads: int = 4,
    **_kwargs,
) -> TableContainer:
    """Generate entities for each row, and optionally a graph of those entities."""
    log.debug("create_community_reports strategy=%s", strategy)
    named_inputs = input.named
    if named_inputs is None:
        raise ValueError(_NAMED_INPUTS_REQUIRED)

    def get_table(name: str) -> pd.DataFrame:
        container = named_inputs.get(name)
        if container is None:
            msg = f"Missing input: {name}"
            raise ValueError(msg)
        return cast(pd.DataFrame, container.table)

    nodes = get_table("nodes")
    community_hierarchy = get_table("community_hierarchy")
    local_contexts = cast(pd.DataFrame, input.get_input())
    levels = sorted(nodes[schemas.NODE_LEVEL].unique(), reverse=True)

    reports: list[CommunityReport | None] = []
    tick = progress_ticker(callbacks.progress, len(local_contexts))

    runner = load_strategy(strategy["type"])

    for level in levels:
        level_contexts = prep_community_report_context(
            local_context_df=local_contexts,
            community_hierarchy_df=community_hierarchy,
            level=level,
            max_tokens=strategy.get(
                "max_input_tokens", defaults.COMMUNITY_REPORT_MAX_INPUT_LENGTH
            ),
        )

        async def run_generate(record):
            result = await _generate_report(
                runner,
                community_id=record[schemas.NODE_COMMUNITY],
                community_level=record[schemas.COMMUNITY_LEVEL],
                community_context=record[schemas.CONTEXT_STRING],
                cache=cache,
                callbacks=callbacks,
                strategy=strategy,
            )
            tick()
            return result

        local_reports = await derive_from_rows(
            level_contexts,
            run_generate,
            callbacks=NoopVerbCallbacks(),
            num_threads=num_threads,
            scheduling_type=async_mode,
        )
        reports.extend(local_reports)

    return TableContainer(
        table=pd.DataFrame([
            report.__dict__ for report in reports if report is not None
        ])
    )


async def _generate_report(
    runner: CommunityReportsStrategy,
    cache: PipelineCache,
    callbacks: VerbCallbacks,
    strategy: dict,
    community_id: int | str,
    community_level: int | str,
    community_context: str,
) -> CommunityReport | None:
    """Generate a report for a single community."""
    return await runner(
        community_id, community_context, community_level, callbacks, cache, strategy
    )


def load_strategy(
    strategy: CommunityReportsStrategyType,
) -> CommunityReportsStrategy:
    """Load strategy method definition."""
    match strategy:
        case CommunityReportsStrategyType.graph_intelligence:
            from .strategies.graph_intelligence import run

            return run
        case _:
            msg = f"Unknown strategy: {strategy}"
            raise ValueError(msg)
