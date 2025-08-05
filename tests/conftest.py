"""Pytest configuration and shared fixtures for the test suite."""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest


@pytest.fixture(scope="session")
def temp_database():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        db_path = tmp_file.name

    yield db_path

    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def mock_engine():
    """Mock SQLModel engine for testing."""
    with patch("skilltest.core.pipeline.engine") as mock:
        yield mock


@pytest.fixture
def mock_session():
    """Mock SQLModel session for testing."""
    with patch("skilltest.core.pipeline.Session") as mock_session_class:
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        yield mock_session
