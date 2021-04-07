import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from src.downloader.StockPriceDownloader import PriceDownloader
from src.trader.Trader import Trader

class BackTester(object):

    def __init__(self, symbol, interval, start, end, strategy_name, save_path = "./data/", ):
        self.symbol = symbol
        self.interval = interval
        self.start = start
        self.end = end
        self.save_path = save_path
        
        self.strategy_name = strategy_name
        

        self.data = None
        self.trader = None
    
    def generateBuySignal(self):
        raise Exception("generateBuySignal has to be overridden")
    
    def run(self):
        # download data
        dler = PriceDownloader(symbol = self.symbol, interval = self.interval, start = self.start, end = self.end, save_path = self.save_path)
        self.data = dler.get_data()

        # call override method generateBuySignal
        self.generateBuySignal()

        self.trader = Trader(col_price = "Adj Close", col_date = "Date")

        # start simulation
        for i in range(len(self.data)):
            info = self.data.iloc[i]
            self.trader.do_dailyOperation(info)
        
        self.trader.do_sell(self.data.iloc[-1])

    def get_record(self):
        return self.trader.get_record()

    def report_result(self):
        breakLine = "-" * 300
        print(breakLine)
        self.plot_record()
        recordDatels = self.get_record()["date_end"].tolist()
        print("%s | start: %s, end: %s, principal: %s, endProfit: %s" 
            %(self.strategy_name, recordDatels[0], recordDatels[-1], self.trader.principal, self.get_record()["endProfit"].tolist()[-1]))

        print(breakLine)

    
    def plot_record(self):
        record = self.get_record()
        date_end_list = record["date_end"].tolist()
        sub_index_list =  [i in date_end_list for i in self.data["Date"]]
        sub_df = self.data[sub_index_list]
        sub_df = sub_df.sort_index()
        x0 = sub_df["Adj Close"].tolist()[0]
        plt.plot(record["date_end"], record["endProfit"], "r--")
        plt.plot(sub_df["Date"], (sub_df["Adj Close"] / x0) * self.trader.principal)
        
        plt.title("%s | %s" %(self.symbol, self.strategy_name))
        plt.show()

