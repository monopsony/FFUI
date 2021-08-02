from collections import Counter


class RecipeHandler:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

            for x in item:
                c += self.getRecipeComp(x, shallow=shallow)

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
