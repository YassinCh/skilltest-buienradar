"""Tests for the core pipeline module using modern pytest features."""

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable, TypeVar, cast
from unittest.mock import Mock, patch

import pytest
from sqlmodel import Session

from src.skilltest.core.extract import AbstractSource, FetchItem
from src.skilltest.core.pipeline import Pipeline
from src.skilltest.core.transform import AbstractTransformer

T = TypeVar("T")


def create_typed_mock(cls: type[T], **kwargs) -> T:
    """Create a typed Mock"""
    return cast(T, Mock(spec=cls, **kwargs))


@dataclass
class MockModel:
    """Mock SQLModel for testing."""

    id: int
    name: str


class MockSource(AbstractSource):
    """Mock source implementation for testing."""

    def __init__(self, data: list[FetchItem]):
        self.data = data

    def fetch(self) -> Iterable[FetchItem]:
        return self.data


class MockTransformer(AbstractTransformer[FetchItem, MockModel]):
    """Mock transformer implementation for testing."""

    def __init__(self, transform_fn: Callable[[FetchItem], MockModel] | None = None):
        self._transform_fn = transform_fn or self._default_transform

    def _default_transform(self, item: FetchItem) -> MockModel:
        return MockModel(id=item.data.get("id", 1), name=item.data.get("name", "test"))

    def transform(self, input: Iterable[FetchItem]) -> Iterable[MockModel]:
        return [self._transform_fn(item) for item in input]


class MockModelTransformer(AbstractTransformer[MockModel, MockModel]):
    """Mock transformer that processes MockModel to MockModel for testing chaining."""

    def __init__(self, transform_fn: Callable[[MockModel], MockModel] | None = None):
        self._transform_fn = transform_fn or self._default_transform

    def _default_transform(self, item: MockModel) -> MockModel:
        return MockModel(id=item.id + 100, name=f"transformed_{item.name}")

    def transform(self, input: Iterable[MockModel]) -> Iterable[MockModel]:
        return [self._transform_fn(item) for item in input]


class TestPipeline:
    """Test suite for the Pipeline class using modern pytest features."""

    @pytest.fixture
    def mock_source(self) -> MockSource:
        """Fixture providing a mock source with test data."""
        test_data = [
            FetchItem(data={"id": 1, "name": "item1"}),
            FetchItem(data={"id": 2, "name": "item2"}),
        ]
        return MockSource(test_data)

    @pytest.fixture
    def mock_transformer(self) -> MockTransformer:
        """Fixture providing a mock transformer."""
        return MockTransformer()

    @pytest.fixture
    def pipeline(self, mock_source: MockSource) -> Pipeline[FetchItem]:
        """Fixture providing a basic pipeline instance."""
        return Pipeline(source=mock_source)

    def test_add_transformers(self, pipeline: Pipeline[FetchItem]):
        """Test adding multiple transformers sequentially."""
        transformer1 = MockTransformer()
        transformer2 = MockModelTransformer()

        pipeline_with_one = pipeline.add(transformer1)
        pipeline_with_two = pipeline_with_one.add(transformer2)

        assert len(pipeline_with_two.transformers) == 2
        assert pipeline_with_two.transformers[0] is transformer1
        assert pipeline_with_two.transformers[1] is transformer2

    @patch("src.skilltest.core.pipeline.Session")
    @patch("src.skilltest.core.pipeline.engine")
    def test_run_without_transformers(
        self, mock_engine: Mock, mock_session_class: Mock, mock_source: MockSource
    ) -> None:
        """Test pipeline run without any transformers."""
        mock_session: Mock = Mock(spec=Session)
        mock_session_class.return_value.__enter__.return_value = mock_session

        pipeline: Pipeline[FetchItem] = Pipeline(source=mock_source)
        pipeline.run()

        mock_session_class.assert_called_once_with(mock_engine)

        assert mock_session.merge.call_count == 2
        mock_session.commit.assert_called_once()

    @patch("src.skilltest.core.pipeline.Session")
    @patch("src.skilltest.core.pipeline.engine")
    def test_run_with_transformers(
        self, mock_engine: Mock, mock_session_class: Mock, mock_source: MockSource
    ):
        """Test pipeline run with transformers."""
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        transformer = MockTransformer()
        base_pipeline: Pipeline[FetchItem] = Pipeline(source=mock_source)
        pipeline = base_pipeline.add(transformer)
        pipeline.run()

        mock_session_class.assert_called_once_with(mock_engine)

        assert mock_session.merge.call_count == 2
        mock_session.commit.assert_called_once()

        merge_calls = mock_session.merge.call_args_list
        for call in merge_calls:
            merged_item = call[0][0]
            assert isinstance(merged_item, MockModel)

    @patch("src.skilltest.core.pipeline.Session")
    @patch("src.skilltest.core.pipeline.engine")
    def test_run_with_chained_transformers(
        self, mock_engine: Mock, mock_session_class: Mock, mock_source: MockSource
    ) -> None:
        """Test pipeline run with multiple chained transformers."""
        # Setup mocks
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Using the typed mock factory - cleaner approach
        transformer1 = create_typed_mock(MockTransformer)
        transformer1.transform.return_value = ["intermediate_data"]  # type: ignore

        transformer2 = create_typed_mock(MockModelTransformer)
        transformer2.transform.return_value = [MockModel(id=3, name="final")]  # type: ignore

        base_pipeline: Pipeline[FetchItem] = Pipeline(source=mock_source)
        pipeline = base_pipeline.add(transformer1).add(transformer2)
        pipeline.run()

        transformer1.transform.assert_called_once()  # type: ignore
        transformer2.transform.assert_called_once_with(["intermediate_data"])  # type: ignore

        mock_session.merge.assert_called_once_with(MockModel(id=3, name="final"))
        mock_session.commit.assert_called_once()

    def test_pipeline_type_safety(self, mock_source: MockSource):
        """Test that pipeline maintains type safety through transformations."""
        transformer = MockTransformer()

        base_pipeline: Pipeline[FetchItem] = Pipeline(source=mock_source)
        typed_pipeline = base_pipeline.add(transformer)
        assert len(typed_pipeline.transformers) == 1
        assert isinstance(typed_pipeline.transformers[0], MockTransformer)

    @patch("src.skilltest.core.pipeline.Session")
    @patch("src.skilltest.core.pipeline.engine")
    def test_run_handles_empty_data(self, mock_engine: Mock, mock_session_class: Mock):
        """Test pipeline run with empty source data."""
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        empty_source = MockSource([])
        pipeline: Pipeline[FetchItem] = Pipeline(source=empty_source)
        pipeline.run()

        mock_session_class.assert_called_once_with(mock_engine)
        mock_session.merge.assert_not_called()
        mock_session.commit.assert_called_once()

    @patch("src.skilltest.core.pipeline.Session")
    @patch("src.skilltest.core.pipeline.engine")
    def test_run_handles_session_exception(
        self, mock_engine: Mock, mock_session_class: Mock, mock_source: MockSource
    ):
        """Test pipeline behavior when session operations fail."""
        mock_session = Mock()
        mock_session.merge.side_effect = Exception("Database error")
        mock_session_class.return_value.__enter__.return_value = mock_session

        pipeline: Pipeline[FetchItem] = Pipeline(source=mock_source)

        with pytest.raises(Exception, match="Database error"):
            pipeline.run()

    @pytest.mark.parametrize("num_items", [1, 5, 10, 100])
    def test_run_with_varying_data_sizes(self, num_items: int, mock_source: MockSource):
        """Test pipeline with different data sizes."""
        test_data = [
            FetchItem(data={"id": i, "name": f"item{i}"}) for i in range(num_items)
        ]
        source = MockSource(test_data)
        with (
            patch("src.skilltest.core.pipeline.Session") as mock_session_class,
            patch("src.skilltest.core.pipeline.engine"),
        ):
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            pipeline: Pipeline[FetchItem] = Pipeline(source=source)
            pipeline.run()

            assert mock_session.merge.call_count == num_items
            mock_session.commit.assert_called_once()


class TestPipelineIntegration:
    """Integration tests for pipeline components."""

    def test_pipeline_with_real_transformer_chain(self) -> None:
        """Test pipeline with realistic transformer chain."""
        source_data = [
            FetchItem(data={"temperature": 20.5, "station": "Amsterdam"}),
            FetchItem(data={"temperature": 18.2, "station": "Rotterdam"}),
        ]
        source = MockSource(source_data)

        def temp_processor(item: FetchItem) -> MockModel:
            temp = item.data["temperature"]
            station = item.data["station"]
            return MockModel(
                id=hash(station) % 1000,
                name=f"{station}: {temp}°C",
            )

        transformer = MockTransformer(transform_fn=temp_processor)

        with (
            patch("src.skilltest.core.pipeline.Session") as mock_session_class,
            patch("src.skilltest.core.pipeline.engine"),
        ):
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session

            base_pipeline: Pipeline[FetchItem] = Pipeline(source=source)
            pipeline = base_pipeline.add(transformer)

            pipeline.run()

            assert mock_session.merge.call_count == 2
            merge_calls = mock_session.merge.call_args_list

            merged_items = [call[0][0] for call in merge_calls]
            assert all(isinstance(item, MockModel) for item in merged_items)
            assert any("Amsterdam: 20.5°C" in item.name for item in merged_items)
            assert any("Rotterdam: 18.2°C" in item.name for item in merged_items)
