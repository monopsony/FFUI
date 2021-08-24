from collections import Counter
import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def colsRemoveSpecialChars(df):
    df.columns = df.columns.str.replace("#", "ItemId")
    df.columns = df.columns.str.replace("[#,@,&,{,},\[,\], ,:]", "", regex=True)
    return df


RECIPES_FILE = "Recipe.csv"


class RecipeHandler:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def secretRecipeBookToMastery(self, n):
        if n == 0:
            return 0
        elif n <= 8:
            return 1
        elif n <= 23:
            return 1.5
        else:
            return (n - 8) // 8

    def loadRecipes(self):
        if not os.path.exists(RECIPES_FILE):
            logger.error(
                f'No file found under {RECIPES_FILE}. Fetch them using "recipe update"'
            )
            return

        r = pd.read_csv(RECIPES_FILE)
        r = colsRemoveSpecialChars(r)

        # add mastery level
        r["MasteryLevel"] = r["SecretRecipeBook"].map(self.secretRecipeBookToMastery)
        self.recipes = r

        # self.recipes.sort_values("Name", inplace=True, ignore_index=True)
        logger.info(f"Loaded a total of {len(self.recipes)} RECIPES")
        self.eventPush("CLIENT_RECIPES_LOADED")

    def getRecipe(self, item):
        df = self.recipes
        recipe = df.loc[df["ItemResult"] == item["ItemId"]]

        if len(recipe) == 0:
            return None
        else:  # len(recipe) == 1:
            return recipe.iloc[0]

    def getRecipeComp(self, item, asItem=False, shallow=False):
        if type(item) == list:
            c = Counter()

            self.setProgress(
                currentProgress=0,
                currentMax=len(item),
                progressText=f"Gathering recipe components",
            )

            i = 0
            for x in item:
                c += self.getRecipeComp(x, shallow=shallow)
                self.setProgress(currentProgress=i)
                i += 1

            if asItem:
                return [self.getItem(id=x) for x in c]
            else:
                return c

        c = Counter()
        rec = self.getRecipe(item)

        if rec is None:
            if asItem:
                return []
            else:
                return c

        for i in range(10):
            ingId = int(rec[f"ItemIngredient{i}"])
            if (ingId == 0) or (ingId == -1):
                continue

            ingAmount = int(rec[f"AmountIngredient{i}"])

            c[ingId] += ingAmount
            ingItem = self.getItem(id=ingId)
            if ingItem is None:
                logger.error(
                    f"Found None item component while gathering comps, id: {ingId}"
                )
                continue
            ingRec = self.getRecipe(ingItem)

            if (ingRec is None) or shallow:
                continue

            ingRecYield = int(ingRec["AmountResult"])
            comp = self.getRecipeComp(ingItem)
            for k in comp:
                comp[k] = comp[k] * ingAmount / ingRecYield

            c += comp

        if asItem:
            return [self.getItem(id=x) for x in c]
        else:
            return c


if __name__ == "__main__":
    r = RecipeHandler()
    for i in range(80):
        print(r.secretRecipeBookToMastery(i))
