from enum import Enum
import urllib.request
from pathlib import Path
from functools import cached_property
from dataclasses import dataclass, field
from typing import List, Generator, Iterator, Optional, Any, Tuple, TypeVar, Type, IO, Union
from abc import ABC, abstractmethod
import pandas as pd
import importlib.resources as resources

# think about how to handle whiespace and capitalization. want to display with those, but maybe not search? Can a df have more than one column name?

T = TypeVar('T')

@dataclass
class Ingredient:
    name: str
    volume: str

NOT_INGREDIENTS = ['Name', 'Garnish', 'Mix', 'Glass', 'Category', 'Notes']



class Database(ABC):

    def get_data(self) -> pd.DataFrame:
        pass

    @staticmethod
    def load_data(file: Union[IO | Path | str]) -> Tuple[pd.DataFrame, pd.Series]:
        data = pd.read_csv(file, index_col='Name')
        data.index = [ind.strip() for ind in data.index]
        data.columns = [column.strip() for column in data.columns]
        ingredient_groups = data.loc['ingredient group']
        data.drop(labels='ingredient group', axis=0, inplace=True)
        return data, ingredient_groups


class GoogleCSVDatabase(Database):

    def __init__(self, key: str):
        self._url = f"https://docs.google.com/spreadsheets/d/{key}/export?exportFormat=csv"
        super().__init__()

    def get_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        with urllib.request.urlopen(self._url) as database_file:
            return self.load_data(database_file)


class LocalFileDatabase(Database):

    def __init__(self, filepath: Union[str, Path]):
        self._csv_filepath = Path(filepath)
        super().__init__()

    def get_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        return self.load_data(self._csv_filepath)


if __name__ == "__main__":

    database = LocalFileDatabase("/Users/dicaprio/Downloads/Cocktailsv2 - Sheet1.csv")
    print(database.get_data())
    print(type(database.get_data()[0]))
    print(type(database.get_data()[1]))