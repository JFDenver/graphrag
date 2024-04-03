# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""A module containing load method definition."""

import logging
import re
from pathlib import Path
from typing import Any

import pandas as pd

from graphrag.index.config import PipelineInputConfig
from graphrag.index.progress import ProgressReporter
from graphrag.index.storage import PipelineStorage
from graphrag.index.utils import gen_md5_hash

DEFAULT_FILE_PATTERN = re.compile(
    r".*[\\/](?P<source>[^\\/]+)[\\/](?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})_(?P<author>[^_]+)_\d+\.txt"
)
input_type = "text"
log = logging.getLogger(__name__)


async def load(
    config: PipelineInputConfig,
    progress: ProgressReporter | None,
    storage: PipelineStorage,
) -> pd.DataFrame:
    """Load text inputs from a directory."""

    async def load_file(
        path: str, group: dict | None = None, _encoding: str = "utf-8"
    ) -> dict[str, Any]:
        if group is None:
            group = {}
        text = await storage.get(path, encoding="utf-8")
        new_item = {**group, "text": text}
        new_item["id"] = gen_md5_hash(new_item, new_item.keys())
        new_item["title"] = str(Path(path).name)
        return new_item

    files = list(
        storage.find(
            re.compile(config.file_pattern),
            progress=progress,
            file_filter=config.file_filter,
        )
    )
    if len(files) == 0:
        msg = "No text files found in %s" % config.base_dir
        raise ValueError(msg)
    log.info("found text files from %s, found %s", config.base_dir, files)
    return pd.DataFrame([await load_file(file, group) for file, group in files])
