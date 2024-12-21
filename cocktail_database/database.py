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

    def get_df(self) -> pd.DataFrame:
        pass

    @staticmethod
    def parse_csv(file: Union[IO | Path | str]):
        data = pd.read_csv(file, index_col='Name')
        data.columns = [column.strip() for column in data.columns]
        data.index = [ind.strip() for ind in data.index]
        return data


class GoogleCSVDatabase(Database):

    def __init__(self, key: str):
        self._url = f"https://docs.google.com/spreadsheets/d/{key}/export?exportFormat=csv"
        super().__init__()

    def get_df(self) -> pd.DataFrame: 
        with urllib.request.urlopen(self._url) as database_file:
            return self.parse_csv(database_file)


class LocalFileDatabase(Database):

    def __init__(self):
        resources_dir = resources.files('resources')
        with resources.as_file(resources_dir / 'cocktails.csv') as csv_filepath:
            self._csv_filepath = Path(csv_filepath)
        super().__init__()

    def get_df(self) -> pd.DataFrame:
        return self.parse_csv(self._csv_filepath)