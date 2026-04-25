"""Unit tests for the correlation ID module."""

import asyncio
import uuid

import pytest

from reqtrace.correlation import (
    generate_correlation_id,
    get_correlation_id,
    get_or_create_correlation_id,
    set_correlation_id,
    correlation_id_var,
)


def test_generate_correlation_id_is_valid_uuid():
    cid = generate_correlation_id()
    parsed = uuid.UUID(cid)
    assert str(parsed) == cid


def test_generate_correlation_id_is_unique():
    ids = {generate_correlation_id() for _ in range(100)}
    assert len(ids) == 100


def test_set_and_get_correlation_id():
    cid = generate_correlation_id()
    set_correlation_id(cid)
    assert get_correlation_id() == cid


def test_get_correlation_id_returns_none_when_not_set():
    # Reset the context variable for this test
    token = correlation_id_var.set(None)
    try:
        assert get_correlation_id() is None
    finally:
        correlation_id_var.reset(token)


def test_get_or_create_uses_provided_header():
    custom_id = "my-custom-id-123"
    result = get_or_create_correlation_id(header_value=custom_id)
    assert result == custom_id
    assert get_correlation_id() == custom_id


def test_get_or_create_generates_id_when_no_header():
    token = correlation_id_var.set(None)
    try:
        result = get_or_create_correlation_id()
        assert result is not None
        assert get_correlation_id() == result
        uuid.UUID(result)  # should not raise
    finally:
        correlation_id_var.reset(token)


def test_correlation_id_is_context_isolated():
    """Each asyncio task should have its own correlation ID context."""
    results = {}

    async def set_and_read(name: str, cid: str):
        set_correlation_id(cid)
        await asyncio.sleep(0)  # yield to event loop
        results[name] = get_correlation_id()

    async def run():
        await asyncio.gather(
            set_and_read("task_a", "id-aaa"),
            set_and_read("task_b", "id-bbb"),
        )

    asyncio.run(run())
    assert results["task_a"] == "id-aaa"
    assert results["task_b"] == "id-bbb"
