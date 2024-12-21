from enum import Enum
import urllib.request
from pathlib import Path
from functools import cached_property
from dataclasses import dataclass, field
from typing import List, Generator, Iterator, Optional, Any, Tuple, TypeVar, Type
from abc import ABC, abstractmethod
import pandas as pd
import importlib.resources as resources
from cocktail_database.database import Database, LocalFileDatabase, GoogleCSVDatabase

# think about how to handle whiespace and capitalization. want to display with those, but maybe not search? Can a df have more than one column name?

T = TypeVar('T')

@dataclass
class Ingredient:
    name: str
    volume: str

NOT_INGREDIENTS = ['Name', 'Garnish', 'Mix', 'Glass', 'Category', 'Notes']


@dataclass
class Cocktail:
    name: str
    ingredients: List[Ingredient]
    mix: str
    glass: str
    garnish: str
    notes: str

    @classmethod
    def from_series(cls: Type[T], series: pd.Series) -> T:
        name = series.name
        entries = series[series.notna()]
        columns_ingredients = [ind for ind in entries.index if ind not in NOT_INGREDIENTS]
        ingredients = [Ingredient(*item) for item in entries[columns_ingredients].items()]
        mix = entries.get('Mix')
        glass = entries.get('Glass')
        notes = entries.get('Notes', '')
        garnish = entries.get('Garnish', '')
        return cls(
            name=name,
            ingredients=ingredients,
            mix=mix,
            glass=glass,
            garnish=garnish,
            notes=notes,
        )

class Match(Enum):
    ALL = "all"
    ANY = "any"


class CocktailLoader:

    def __init__(self, database: Database):
        self._database = database

    def get_cocktails_matching(self, ingredients: Iterator[str], match: Match) -> Generator[Cocktail, None, None]:

        matcher = getattr(self._cocktail_df.loc[:, ingredients].notnull(), match.value)
        idx = matcher(axis='columns')
        for index, row in self._cocktail_df.loc[idx, :].iterrows():
            yield Cocktail.from_series(row)

    def get_cocktail_by_name(self, name: str) -> Cocktail:
        try:
            row = self._cocktail_df.loc[name]
        except KeyError:
            return None
        return Cocktail.from_series(row)

    def get_all_cocktails(self) -> Generator[Cocktail, None, None]:
        for index, row in self._cocktail_df.iterrows():
            yield Cocktail.from_series(row)

    @cached_property
    def ingredients(self) -> List[str]:
        return [ind for ind in self._cocktail_df.columns if ind not in NOT_INGREDIENTS]

    @cached_property
    def _cocktail_df(self) -> pd.DataFrame:
        return self._database.get_df()


        



if __name__ == "__main__":

    ingredients = ["Rye", "Dry Vermouth", "Campari"]
    match = Match.ALL
    # database = LocalFileDatabase()
    key = "1diaueSEOgMkL1mbNxtLawo0N9-OPlBK-cTdg_8KZlCA"
    database = GoogleCSVDatabase(key=key)
    loader = CocktailLoader(database=database)

    print(f"cocktials matching {match}")
    for cocktail in loader.get_cocktails_matching(ingredients, match):
        print(f"name: {cocktail.name}")
        print(f"ingredients: {cocktail.ingredients}")
        print(f"garnish: {cocktail.garnish}")
        print(f"mix: {cocktail.mix}")
        print(f"glass: {cocktail.glass}")
        print(f"notes: {cocktail.notes}")
        print("")

    match = Match.ANY
    print("")
    print(f"cocktials matching {match}")
    for cocktail in loader.get_cocktails_matching(ingredients, match):
        print(f"name: {cocktail.name}")
        print(f"ingredients: {cocktail.ingredients}")
        print(f"garnish: {cocktail.garnish}")
        print(f"mix: {cocktail.mix}")
        print(f"glass: {cocktail.glass}")
        print(f"notes: {cocktail.notes}")
        print("")

    print("="*50)
    name = "Old Pal"
    cocktail = loader.get_cocktail_by_name(name)
    print(cocktail)

    print("="*50)
    print(loader.ingredients)