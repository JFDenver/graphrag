# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""A module containing create_graph, _get_node_attributes, _get_edge_attributes and _get_attribute_column_mapping methods definition."""

import logging
from typing import cast

import pandas as pd
from datashaper import TableContainer, VerbInput, verb

import graphrag.index.graph.extractors.community_reports.schemas as schemas

log = logging.getLogger(__name__)


@verb(name="restore_community_hierarchy")
def restore_community_hierarchy(
    input: VerbInput,
    node_name_column: str = schemas.NODE_NAME,
    node_community_column: str = schemas.NODE_COMMUNITY,
    node_level_column: str = schemas.NODE_LEVEL,
    **_kwargs,
) -> TableContainer:
    """Restore the community hierarchy from the node data."""
    node_df: pd.DataFrame = cast(pd.DataFrame, input.get_input())
    community_df = (
        node_df.groupby([node_community_column, node_level_column])
        .agg({node_name_column: list})
        .reset_index()
    )
    community_levels = {}
    for _, row in community_df.iterrows():
        if community_levels.get(row[node_level_column]) is None:
            community_levels[row[node_level_column]] = {}
        community_levels[row[node_level_column]][row[node_community_column]] = row[
            node_name_column
        ]

    # get unique levels, sorted in ascending order
    levels = sorted(community_levels.keys())

    community_hierarchy = []

    for idx in range(len(levels) - 1):
        level = levels[idx]
        log.debug("Level: %s", level)
        next_level = levels[idx + 1]
        current_level_communities = community_levels[level]
        next_level_communities = community_levels[next_level]
        log.debug(
            "Number of communities at level %s: %s",
            level,
            len(current_level_communities),
        )

        for current_community in current_level_communities:
            current_entities = current_level_communities[current_community]

            # loop through next level's communities to find all the subcommunities
            entities_found = 0
            for next_level_community in next_level_communities:
                next_entities = next_level_communities[next_level_community]
                if set(next_entities).issubset(set(current_entities)):
                    community_hierarchy.append({
                        node_community_column: current_community,
                        schemas.COMMUNITY_LEVEL: level,
                        schemas.SUB_COMMUNITY: next_level_community,
                        schemas.SUB_COMMUNITY_SIZE: len(next_entities),
                    })

                    entities_found += len(next_entities)
                    if entities_found == len(current_entities):
                        break

    return TableContainer(table=pd.DataFrame(community_hierarchy))
