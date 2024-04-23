# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""A module containing build_steps method definition."""

from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

workflow_name = "create_final_community_reports"


def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    Create the final community reports table.

    ## Dependencies
    * `workflow:create_base_entity_graph`
    """
    create_community_reports_config = config.get("create_community_reports", {})
    base_text_embed = config.get("text_embed", {})
    community_report_full_content_embed_config = config.get(
        "community_report_full_content_embed", base_text_embed
    )
    community_report_summary_embed_config = config.get(
        "community_report_summary_embed", base_text_embed
    )
    community_report_title_embed_config = config.get(
        "community_report_title_embed", base_text_embed
    )
    skip_title_embedding = config.get("skip_title_embedding", False)
    skip_summary_embedding = config.get("skip_summary_embedding", False)
    skip_full_content_embedding = config.get("skip_full_content_embedding", False)

    return [
        #
        # Subworkflow: Augment Edges
        #
        {
            "verb": "compute_edge_combined_degree",
            "input": {
                "source": "workflow:create_final_relationships",
                "nodes": "nodes",
            },
        },
        {"id": "edges", "verb": "prepare_community_reports_edges"},
        #
        # Subworkflow: Prepare Claims Table
        #
        {
            "id": "claims",
            "verb": "prepare_community_reports_claims",
            "input": {
                "source": "workflow:create_final_covariates",
            },
        },
        #
        # Subworkflow: Get Community Hierarchy
        #
        {
            "id": "community_hierarchy",
            "verb": "restore_community_hierarchy",
            "input": {"source": "workflow:create_final_entities"},
        },
        #
        # Main Workflow: Create Community Reports
        #
        {
            "id": "local_contexts",
            "verb": "build_community_local_contexts",
            "input": {
                "source": "workflow:create_final_entities",
                "nodes": "workflow:create_final_entities",
                "edges": "edges",
                "claims": "claims",
            },
        },
        {
            "verb": "create_community_reports",
            "args": {
                **create_community_reports_config,
            },
            "input": {
                "source": "local_contexts",
                "community_hierarchy": "community_hierarchy",
                "nodes": "nodes",
            },
        },
        {
            # Generate a unique ID for each community report distinct from the community ID
            "verb": "window",
            "args": {"to": "id", "operation": "uuid", "column": "community_id"},
        },
        {
            "verb": "text_embed",
            "enabled": not skip_full_content_embedding,
            "args": {
                "embedding_name": "community_report_full_content",
                "column": "full_content",
                "to": "full_content_embedding",
                **community_report_full_content_embed_config,
            },
        },
        {
            "verb": "text_embed",
            "enabled": not skip_summary_embedding,
            "args": {
                "embedding_name": "community_report_summary",
                "column": "summary",
                "to": "summary_embedding",
                **community_report_summary_embed_config,
            },
        },
        {
            "verb": "text_embed",
            "enabled": not skip_title_embedding,
            "args": {
                "embedding_name": "community_report_title",
                "column": "title",
                "to": "title_embedding",
                **community_report_title_embed_config,
            },
        },
    ]
