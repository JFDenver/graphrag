# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""Parameterization settings for the default configuration."""

from pydantic import BaseModel, Field

from graphrag.index.config import PipelineReportingType


class ReportingConfigModel(BaseModel):
    """The default configuration section for Reporting."""

    type: PipelineReportingType | None = Field(
        description="The reporting type to use.", default=None
    )
    base_dir: str | None = Field(
        description="The base directory for reporting.", default=None
    )
    connection_string: str | None = Field(
        description="The reporting connection string to use.", default=None
    )
    container_name: str | None = Field(
        description="The reporting container name to use.", default=None
    )