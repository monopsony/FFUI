import pandas as pd
import os, importlib

customMetricsString = r"""
import pandas as pd

class Metrics:
    @staticmethod
    def bogusMetric(df):
        return 1234

ACTIVE_METRICS = {
    "INFO": {}, # {nameOfMetrics: Metrics.nameOfMethod, ...}
    "CRAFT": {},
    "FLIP": {},
}
"""

customMetricsPath = os.path.join("Client", "MetricsCustom.py")
if not os.path.exists(customMetricsPath):
    with open(customMetricsPath, "w+") as f:
        f.write(customMetricsString)

custom = importlib.import_module("Client.MetricsCustom")
ACTIVE_METRICS_CUSTOM = custom.ACTIVE_METRICS
customMetrics = custom.Metrics


class Metrics(customMetrics):
    @staticmethod
    def expectedCraftProfit(df):
        price = df[["averagePrice", "minPrice"]].min(axis=1)
        return price * 0.95 * 0.97 - df["craftPrice"]
        # 0.95 for buyers tax (prices in universalis are displayed with buyers tax in mind)
        # 0.97 for sellers tax (assuming retainers in crystarium/ishgard or whatever)

    @staticmethod
    def expectedCraftProfitPerDay(df):
        return df["expectedCraftProfit"] * df["salesPerDay"]


ACTIVE_METRICS = {
    "INFO": {},  # {nameOfMetrics: Metrics.nameOfMethod, ...}
    "CRAFT": {
        "expectedCraftProfit": Metrics.expectedCraftProfit,
        "expectedCraftProfitPerDay": Metrics.expectedCraftProfitPerDay,
    },
    "FLIP": {},
}


for typ in ["INFO", "CRAFT", "FLIP"]:
    d = ACTIVE_METRICS_CUSTOM[typ]
    for k, v in d.items():
        ACTIVE_METRICS[typ][k] = v
# why not just use the same dictionary from customMetrics
# --> to have the Metrics here be first in the ordering, mainly


# ACTIVE_METRICS["CRAFT"]["expectedCraftProfit"] = Metrics.expectedCraftProfit
# ACTIVE_METRICS["CRAFT"]["expectedCraftProfitPerDay"] = Metrics.expectedCraftProfitPerDay
