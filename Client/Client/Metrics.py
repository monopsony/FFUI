import pandas as pd


class Metrics:
    @staticmethod
    def expectedCraftProfit(df):
        price = df[["averagePrice", "minPrice"]].min(axis=1)
        return price - df["craftPrice"]

    @staticmethod
    def expectedCraftProfitPerDay(df):
        return df["expectedCraftProfit"] * df["regularSaleVelocity"]


ACTIVE_METRICS = {
    "INFO": {},
    "CRAFT": {
        "expectedCraftProfit": Metrics.expectedCraftProfit,
        "expectedCraftProfitPerDay": Metrics.expectedCraftProfitPerDay,
    },
    "FLIP": {},
}
