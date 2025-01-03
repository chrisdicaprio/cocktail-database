import streamlit as st
import os

from typing import TYPE_CHECKING
from cocktail_database.cocktails import Match, CocktailLoader
from cocktail_database.database import GoogleCSVDatabase, LocalFileDatabase

if TYPE_CHECKING:
     from cocktail_database.cocktails import Cocktail

def write_cocktail(cocktail: 'Cocktail') -> None:
    st.divider()
    ingredeints_md = ""
    for ingredient in cocktail.ingredients:
        ingredeints_md += f"- {ingredient.name}: {ingredient.volume}\n"
    ingredeints_md = ingredeints_md[:-1]
    st.markdown(ingredeints_md)
    st.write(f"{cocktail.mix}, {cocktail.glass}")
    if cocktail.garnish:
        st.write(f"Garnish with {cocktail.garnish.lower()}")
    if cocktail.notes:
        st.write(f"Notes: {cocktail.notes}")

key = st.secrets["GOOGLE_CSV_KEY"]
database = GoogleCSVDatabase(key=key)
# database = LocalFileDatabase("/Users/dicaprio/Downloads/Cocktailsv2 - Sheet1.csv")
# database = LocalFileDatabase("/Users/dicaprio/Downloads/Cocktailsv2 - Sheet1.csv")
loader = CocktailLoader(database=database)

ingredients = []
ncols = 3
cols = st.columns(ncols)
for i, ingredient_group in enumerate(loader.ingredient_groups()):
    if ingredient_group.name == 'Bitters':
        continue
    with cols[i % ncols]:
        ingredients += st.multiselect(
            ingredient_group.name,
            ingredient_group.ingredients,
            default=None,
            placeholder="Choose your ingredients"
        )
match = Match(st.radio("match", ["Any", "All"]).lower())

if ingredients:
    for cocktail in loader.get_cocktails_matching(ingredients, match):
        with st.expander(label=f"**{cocktail.name}**"):
            write_cocktail(cocktail)
elif match is Match.ANY:
    for cocktail in loader.get_all_cocktails():
        with st.expander(label=f"**{cocktail.name}**"):
            write_cocktail(cocktail)
