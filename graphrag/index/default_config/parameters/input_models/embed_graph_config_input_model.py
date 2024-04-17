# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""Parameterization settings for the default configuration."""

from typing_extensions import NotRequired, TypedDict


class EmbedGraphConfigInputModel(TypedDict):
    """The default configuration section for Node2Vec."""

    is_enabled: NotRequired[bool | str | None]
    num_walks: NotRequired[int | str | None]
    walk_length: NotRequired[int | str | None]
    window_size: NotRequired[int | str | None]
    iterations: NotRequired[int | str | None]
    random_seed: NotRequired[int | str | None]
    strategy: NotRequired[dict | None]
