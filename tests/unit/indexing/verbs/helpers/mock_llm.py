# Copyright (c) 2024 Microsoft Corporation. All rights reserved.
from graphrag.llm import CompletionLLM, MockChatLLM


def create_mock_llm(
    responses: list[str],
) -> CompletionLLM:
    """Creates a mock LLM that returns the given responses."""
    return MockChatLLM(responses)
