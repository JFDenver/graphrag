# Copyright (c) 2024 Microsoft Corporation. All rights reserved.
from graphrag.index import (
    default_config,
    default_config_parameters,
    run_pipeline,
    run_pipeline_with_config,
)


def test_exported_functions():
    assert callable(default_config)
    assert callable(run_pipeline_with_config)
    assert callable(run_pipeline)
    assert callable(default_config_parameters)
