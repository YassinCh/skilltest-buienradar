from typing import Type

import polars as pl
from sqlmodel import SQLModel, select

from .database import engine as default_engine


class DataFrameConvertor:
    @staticmethod
    def get_dataframe(model: Type[SQLModel]) -> pl.DataFrame:
        """Get Polars DataFrame from SQLModel table"""
        with default_engine.connect() as conn:
            return pl.read_database(select(model), connection=conn)

    @staticmethod
    def get_joined_dataframe(
        left_df: pl.DataFrame, right_df: pl.DataFrame, on: str
    ) -> pl.DataFrame:
        """Join DataFrames"""
        return left_df.join(right_df, on=on, how="inner")
