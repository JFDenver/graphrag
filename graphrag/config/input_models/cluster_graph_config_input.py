# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""Parameterization settings for the default configuration."""

from typing_extensions import NotRequired, TypedDict


class ClusterGraphConfigInput(TypedDict):
    """Configuration section for clustering graphs."""

    max_cluster_size: NotRequired[int | None]
    strategy: NotRequired[dict | None]
