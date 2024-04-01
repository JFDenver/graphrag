#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project.
#

"""Parameterization settings for the default configuration, loaded from environment variables."""
from enum import Enum
from pathlib import Path

from datashaper import AsyncType
from environs import Env

from graphrag.index.config import (
    PipelineCacheType,
    PipelineInputStorageType,
    PipelineInputType,
    PipelineReportingType,
    PipelineStorageType,
)
from graphrag.index.default_config.parameters.models import TextEmbeddingTarget
from graphrag.index.default_config.parameters.read_dotenv import read_dotenv

from .default_config_parameters import DefaultConfigParametersDict
from .default_config_parameters_model import DefaultConfigParametersModel
from .models import (
    CacheConfigModel,
    ChunkingConfigModel,
    ClaimExtractionConfigModel,
    ClusterGraphConfigModel,
    CommunityReportsConfigModel,
    EmbedGraphConfigModel,
    EntityExtractionConfigModel,
    InputConfigModel,
    LLMParametersModel,
    ParallelizationParametersModel,
    ReportingConfigModel,
    SnapshotsConfigModel,
    StorageConfigModel,
    SummarizeDescriptionsConfigModel,
    TextEmbeddingConfigModel,
    UmapConfigModel,
)


def default_config_parameters(
    values: DefaultConfigParametersModel,
    root_dir: str | None,
    resume_from: str | None = None,
):
    """Load Configuration Parameters from a dictionary."""
    root_dir = root_dir or str(Path.cwd())
    env = _make_env(root_dir)
    return DefaultConfigParametersDict(values, env, root_dir, resume_from)


class Fragment(str, Enum):
    """Configuration Fragments."""

    api_base = "API_BASE"
    api_key = "API_KEY"
    api_version = "API_VERSION"
    async_mode = "ASYNC_MODE"
    concurrent_requests = "CONCURRENT_REQUESTS"
    conn_string = "CONNECTION_STRING"
    container_name = "CONTAINER_NAME"
    deployment_name = "DEPLOYMENT_NAME"
    description = "DESCRIPTION"
    enabled = "ENABLED"
    encoding = "ENCODING"
    encoding_model = "ENCODING_MODEL"
    max_gleanings = "MAX_GLEANINGS"
    max_length = "MAX_LENGTH"
    max_retries = "MAX_RETRIES"
    max_retry_wait = "MAX_RETRY_WAIT"
    max_tokens = "MAX_TOKENS"
    model = "MODEL"
    model_supports_json = "MODEL_SUPPORTS_JSON"
    organization = "ORGANIZATION"
    prompt_file = "PROMPT_FILE"
    proxy = "PROXY"
    request_timeout = "REQUEST_TIMEOUT"
    rpm = "RPM"
    sleep_recommendation = "SLEEP_ON_RATE_LIMIT_RECOMMENDATION"
    thread_count = "THREAD_COUNT"
    thread_stagger = "THREAD_STAGGER"
    tpm = "TPM"
    type = "TYPE"
    base_dir = "BASE_DIR"


class Section(str, Enum):
    """Configuration Sections."""

    cache = "CACHE"
    chunk = "CHUNK"
    claim_extraction = "CLAIM_EXTRACTION"
    community_report = "COMMUNITY_REPORT"
    embedding = "EMBEDDING"
    entity_extraction = "ENTITY_EXTRACTION"
    graphrag = "GRAPHRAG"
    input = "INPUT"
    llm = "LLM"
    node2vec = "NODE2VEC"
    reporting = "REPORTING"
    snapshot = "SNAPSHOT"
    storage = "STORAGE"
    summarize_descriptions = "SUMMARIZE_DESCRIPTIONS"
    umap = "UMAP"


def default_config_parameters_from_env_vars(
    root_dir: str | None, resume_from: str | None = None
):
    """Load Configuration Parameters from environment variables."""
    root_dir = root_dir or str(Path.cwd())
    env = _make_env(root_dir)

    def _str(key: str, default_value: str | None = None) -> str | None:
        return env(key, default_value)

    def _int(key: str, default_value: int | None = None) -> int | None:
        return env.int(key, default_value)

    def _bool(key: str, default_value: bool | None = None) -> bool | None:
        return env.bool(key, default_value)

    def _float(key: str, default_value: float | None = None) -> float | None:
        return env.float(key, default_value)

    def section(key: str):
        return env.prefixed(f"{key}_")

    fallback_oai_key = _str("OPENAI_API_KEY", _str("AZURE_OPENAI_API_KEY"))
    fallback_oai_org = _str("OPENAI_ORG_ID")
    fallback_oai_url = _str("OPENAI_BASE_URL")
    fallback_oai_version = _str("OPENAI_API_VERSION")

    with section(Section.graphrag):
        _api_key = _str(Fragment.api_key, fallback_oai_key)
        _api_base = _str(Fragment.api_base, fallback_oai_url)
        _api_version = _str(Fragment.api_version, fallback_oai_version)
        _organization = _str(Fragment.organization, fallback_oai_org)
        _proxy = _str(Fragment.proxy)
        _tpm = _int(Fragment.tpm)
        _rpm = _int(Fragment.rpm)
        _request_timeout = _float(Fragment.request_timeout)
        _max_retries = _int(Fragment.max_retries)
        _max_retry_wait = _float(Fragment.max_retry_wait)
        _sleep_recommendation = _bool(Fragment.sleep_recommendation)
        _concurrent_requests = _int(Fragment.concurrent_requests)
        _async_mode = _str(Fragment.async_mode)
        _stagger = _float(Fragment.thread_stagger)
        _thread_count = _int(Fragment.thread_count)

        with section(Section.llm):
            api_key = _str(Fragment.api_key, _api_key or fallback_oai_key)
            if api_key is None:
                msg = "API Key is required for Completion API. Please set either the OPENAI_API_KEY, GRAPHRAG_API_KEY or GRAPHRAG_LLM_API_KEY environment variable."
                raise ValueError(msg)
            llm_parameters = LLMParametersModel(
                api_key=api_key,
                type=_str(Fragment.type),
                model=_str(Fragment.model),
                max_tokens=_int(Fragment.max_tokens),
                model_supports_json=_bool(Fragment.model_supports_json),
                request_timeout=_float(Fragment.request_timeout, _request_timeout),
                api_base=_str(Fragment.api_base, _api_base),
                api_version=_str(Fragment.api_version, _api_version),
                organization=_str(Fragment.organization, _organization),
                proxy=_str(Fragment.proxy, _proxy),
                deployment_name=_str(Fragment.deployment_name),
                tokens_per_minute=_int(Fragment.tpm, _tpm),
                requests_per_minute=_int(Fragment.rpm, _rpm),
                max_retries=_int(Fragment.max_retries, _max_retries),
                max_retry_wait=_float(Fragment.max_retry_wait, _max_retry_wait),
                sleep_on_rate_limit_recommendation=_bool(
                    Fragment.sleep_recommendation, _sleep_recommendation
                ),
                concurrent_requests=_int(
                    Fragment.concurrent_requests, _concurrent_requests
                ),
            )
            llm_parallelization = ParallelizationParametersModel(
                stagger=_float(Fragment.thread_stagger, _stagger),
                num_threads=_int(Fragment.thread_count, _thread_count),
            )

        with section(Section.embedding):
            api_key = _str(Fragment.api_key, _api_key)
            if api_key is None:
                msg = "API Key is required for Embedding API. Please set either the OPENAI_API_KEY, GRAPHRAG_API_KEY or GRAPHRAG_EMBEDDING_API_KEY environment variable."
                raise ValueError(msg)

            embedding_target = _str("TARGET")
            embedding_target = (
                TextEmbeddingTarget(embedding_target) if embedding_target else None
            )
            async_mode = _str(Fragment.async_mode, _async_mode)
            async_mode_enum = AsyncType(async_mode) if async_mode else None

            text_embeddings = TextEmbeddingConfigModel(
                parallelization=ParallelizationParametersModel(
                    stagger=_float(Fragment.thread_stagger, _stagger),
                    num_threads=_int(Fragment.thread_count, _thread_count),
                ),
                async_mode=async_mode_enum,
                target=embedding_target,
                batch_size=_int("BATCH_SIZE"),
                batch_max_tokens=_int("BATCH_MAX_TOKENS"),
                skip=_array_string("SKIP"),
                llm=LLMParametersModel(
                    api_key=_str(Fragment.api_key, _api_key),
                    type=_str(Fragment.type),
                    model=_str(Fragment.model),
                    request_timeout=_float(Fragment.request_timeout, _request_timeout),
                    api_base=_str(Fragment.api_base, _api_base),
                    api_version=_str(Fragment.api_version, _api_version),
                    organization=_str(Fragment.organization, _organization),
                    proxy=_str(Fragment.proxy, _proxy),
                    deployment_name=_str(Fragment.deployment_name),
                    tokens_per_minute=_int(Fragment.tpm, _tpm),
                    requests_per_minute=_int(Fragment.rpm, _rpm),
                    max_retries=_int(Fragment.max_retries, _max_retries),
                    max_retry_wait=_float(Fragment.max_retry_wait, _max_retry_wait),
                    sleep_on_rate_limit_recommendation=_bool(
                        Fragment.sleep_recommendation, _sleep_recommendation
                    ),
                    concurrent_requests=_int(
                        Fragment.concurrent_requests, _concurrent_requests
                    ),
                ),
            )

        with section(Section.node2vec):
            embed_graph = EmbedGraphConfigModel(
                is_enabled=_bool(Fragment.enabled),
                num_walks=_int("NUM_WALKS"),
                walk_length=_int("WALK_LENGTH"),
                window_size=_int("WINDOW_SIZE"),
                iterations=_int("ITERATIONS"),
                random_seed=_int("RANDOM_SEED"),
            )
        with section(Section.reporting):
            reporting_type = _str(Fragment.type)
            reporting_type = (
                PipelineReportingType(reporting_type) if reporting_type else None
            )
            reporting = ReportingConfigModel(
                type=reporting_type,
                connection_string=_str(Fragment.conn_string),
                container_name=_str(Fragment.container_name),
                base_dir=_str(Fragment.base_dir),
            )
        with section(Section.storage):
            storage_type = _str(Fragment.type)
            storage_type = PipelineStorageType(storage_type) if storage_type else None
            storage = StorageConfigModel(
                type=storage_type,
                connection_string=_str(Fragment.conn_string),
                container_name=_str(Fragment.container_name),
                base_dir=_str(Fragment.base_dir),
            )
        with section(Section.cache):
            cache_type = _str(Fragment.type)
            cache_type = PipelineCacheType(cache_type) if cache_type else None
            cache = CacheConfigModel(
                type=cache_type,
                connection_string=_str(Fragment.conn_string),
                container_name=_str(Fragment.container_name),
                base_dir=_str(Fragment.base_dir),
            )
        with section(Section.input):
            input_type = _str(Fragment.type)
            input_type = PipelineInputType(input_type) if input_type else None
            storage_type = _str("STORAGE_TYPE")
            storage_type = (
                PipelineInputStorageType(storage_type) if storage_type else None
            )
            input = InputConfigModel(
                type=input_type,
                storage_type=storage_type,
                file_encoding=_str(Fragment.encoding),
                base_dir=_str(Fragment.base_dir),
                file_pattern=_str("FILE_PATTERN"),
                source_column=_str("SOURCE_COLUMN"),
                timestamp_column=_str("TIMESTAMP_COLUMN"),
                timestamp_format=_str("TIMESTAMP_FORMAT"),
                text_column=_str("TEXT_COLUMN"),
                title_column=_str("TITLE_COLUMN"),
                document_attribute_columns=_array_string(
                    _str("DOCUMENT_ATTRIBUTE_COLUMNS"),
                ),
            )
        with section(Section.chunk):
            chunks = ChunkingConfigModel(
                size=_int("SIZE"),
                overlap=_int("OVERLAP"),
                group_by_columns=_array_string(_str("BY_COLUMNS")),
            )
        with section(Section.snapshot):
            snapshots = SnapshotsConfigModel(
                graphml=_bool("GRAPHML"),
                raw_entities=_bool("RAW_ENTITIES"),
                top_level_nodes=_bool("TOP_LEVEL_NODES"),
            )
        with section(Section.entity_extraction):
            entity_extraction = EntityExtractionConfigModel(
                entity_types=_array_string(_str("ENTITY_TYPES")),
                max_gleanings=_int(Fragment.max_gleanings),
                prompt=_str(Fragment.prompt_file),
            )
        with section(Section.claim_extraction):
            claim_extraction = ClaimExtractionConfigModel(
                description=_str(Fragment.description),
                prompt=_str(Fragment.prompt_file),
                max_gleanings=_int(Fragment.max_gleanings),
            )
        with section(Section.community_report):
            community_reports = CommunityReportsConfigModel(
                prompt=_str(Fragment.prompt_file),
                max_length=_int(Fragment.max_length),
                max_input_length=_int("MAX_INPUT_LENGTH"),
            )
        with section(Section.summarize_descriptions):
            summarize_descriptions = SummarizeDescriptionsConfigModel(
                prompt=_str(Fragment.prompt_file),
                max_length=_int(Fragment.max_length),
            )
        with section(Section.umap):
            umap = UmapConfigModel(
                enabled=_bool(Fragment.enabled),
            )

        async_mode_enum = AsyncType(async_mode) if async_mode else None
        return DefaultConfigParametersDict(
            DefaultConfigParametersModel(
                llm=llm_parameters,
                parallelization=llm_parallelization,
                embeddings=text_embeddings,
                embed_graph=embed_graph,
                reporting=reporting,
                storage=storage,
                cache=cache,
                input=input,
                chunks=chunks,
                snapshots=snapshots,
                entity_extraction=entity_extraction,
                claim_extraction=claim_extraction,
                community_reports=community_reports,
                summarize_descriptions=summarize_descriptions,
                umap=umap,
                async_mode=async_mode_enum,
                cluster_graph=ClusterGraphConfigModel(
                    max_cluster_size=_int("MAX_CLUSTER_SIZE"),
                ),
                encoding_model=_str(Fragment.encoding_model),
                skip_workflows=_array_string(_str("SKIP_WORKFLOWS")),
            ),
            env,
            root_dir,
            resume_from,
        )


def _make_env(root_dir: str) -> Env:
    read_dotenv(root_dir)
    env = Env()
    env.read_env()
    return env


def _array_string(
    raw: str | None, default_value: list[str] | None = None
) -> list[str] | None:
    """Filter the array entries."""
    if raw is None:
        return default_value

    result = [r.strip() for r in raw.split(",")]
    return [r for r in result if r != ""]