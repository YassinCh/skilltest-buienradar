from typing import Type

import polars as pl
from sqlmodel import SQLModel

from ...database import engine as default_engine


class DataFrameConvertor:
    # TODO: Improve this class
    @staticmethod
    def get_dataframe(model: Type[SQLModel]) -> pl.DataFrame:
        """Get Polars DataFrame from SQLModel table"""
        table_name = model.__tablename__
        query = f"SELECT * FROM {table_name}"
        with default_engine.connect() as conn:
            df = pl.read_database(query, connection=conn)
        return df

    @staticmethod
    def get_joined_dataframe(
        left_df: pl.DataFrame, right_df: pl.DataFrame, on: str
    ) -> pl.DataFrame:
        """Join DataFrames"""
        return left_df.join(right_df, on=on, how="inner")
