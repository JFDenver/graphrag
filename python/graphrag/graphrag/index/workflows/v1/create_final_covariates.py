#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project.
#

"""A module containing build_steps method definition."""
from datashaper import AsyncType

from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

workflow_name = "create_final_covariates"


def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    Create the final covariates table.

    ## Dependencies
    * `workflow:create_base_text_units`
    * `workflow:create_base_extracted_entities`
    """
    claim_extract_config = config.get("claim_extract", {})

    input = {"source": "workflow:create_base_text_units"}

    return [
        {
            "id": "extract_claims",
            "verb": "extract_claims",
            "args": {
                "column": config.get("chunk_column", "chunk"),
                "id_column": config.get("chunk_id_column", "chunk_id"),
                "resolved_entities_column": "resolved_entities",
                "async_mode": config.get("async_mode", AsyncType.AsyncIO),
                **claim_extract_config,
            },
            "input": input,
        },
        {
            "verb": "impute",
            "args": {
                "column": "covariate_type",
                "value": "claim",
            },
        },
        {
            "verb": "window",
            "args": {"to": "id", "operation": "uuid", "column": "covariate_type"},
        },
        {
            "verb": "rename",
            "args": {
                "columns": {
                    "chunk_id": "text_unit_id",
                }
            },
        },
        {
            "verb": "select",
            "args": {
                "columns": [
                    "id",
                    "covariate_type",
                    "type",
                    "description",
                    "subject_id",
                    "subject_type",
                    "object_id",
                    "object_type",
                    "status",
                    "start_date",
                    "end_date",
                    "source_text",
                    "text_unit_id",
                    "document_ids",
                    "n_tokens",
                ]
            },
        },
    ]