# %%

%load_ext autoreload
%autoreload 2

from random import randint


from src.backTester.BackTester import BackTester
from src.utils.MathUtils import *


# %%
class RandomTrading(BackTester):

    def generateBuySignal(self):
        nrow = len(self.data)
        buySignal = [randint(0, 1) == 1 for i in range(nrow)]
        self.data["isBuy"] = buySignal

class Momentum_SMA(BackTester):

    def __init__(self, symbol, interval, start, end, sma_short, sma_long, strategy_name):
        self.sma_short = sma_short
        self.sma_long = sma_long
        super().__init__(symbol, interval, start, end, strategy_name)

    def generateBuySignal(self):
        price_ls = self.data["Adj Close"].tolist()
        sma_short = cal_sma(price_ls, self.sma_short)
        sma_long = cal_sma(price_ls, self.sma_long)
        self.data["sma_short"] = sma_short
        self.data["sma_long"] = sma_long
        isBuy = self.data["sma_long"] <= self.data["sma_short"]
        self.data["compare"] = isBuy
        isBuy = self.data["compare"].tolist()
        isBuy = [np.nan] + isBuy
        isBuy = isBuy[:-1]
        self.data["isBuy"] = isBuy
        self.data.dropna(subset=["sma_short", "sma_long"], axis = 0, inplace = True)

def test_sma_strategy(symbol, short, long):
    sma = Momentum_SMA(symbol, interval="1d", 
        start = "2000-01-01", end = "2020-12-01", 
        sma_short = short, sma_long = long, 
        strategy_name="SMA_%s_%s" %(short, long))
    sma.run()
    sma.report_result()
    filename = "./tradingRecord/%s_%s_%s.csv" %(symbol, short, long)
    sma.get_record.to_csv(filename, index = False)

stockls = ["^HSI"]
for i in range(1000):
    tmp = str(i + 1)
    rep = 4 - len(tmp)
    stockls.append("0" * rep + tmp + ".HK")
for s in stockls:
    try:
        test_sma_strategy(s, short = 15, long = 90)
    except:
        print("Error: %s" % s)
        continue

# %%
from src.downloader.StockPriceDownloader import PriceDownloader

dler = PriceDownloader("AAPL", interval="1d", start = "2000-01-01", end = "2020-12-01")

# %%
