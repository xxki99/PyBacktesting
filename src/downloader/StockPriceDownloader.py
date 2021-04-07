import yfinance as yf
from os.path import isdir
from os import mkdir
import pandas as pd

class PriceDownloader():
    def __init__(self, symbol, interval, start, end, save_path = "./data/"):
        self.symbol = symbol
        self.interval = interval
        self.start = start
        self.end = end
        self.save_path = save_path        

        self.data = pd.DataFrame()
        
        self.do_download()
        self.data_process()

    def data_process(self):
        self.data["Date"] = self.data.index


    def get_data(self):
        
        return self.data


    def do_download(self):
        data = yf.download(self.symbol, interval=self.interval, start = self.start, end = self.end)
        self.data = data

    def save_data(self):
        if not self.data.empty:
            if (not isdir(self.save_path)):
                mkdir(self.save_path)
            self.data.to_csv("%s%s_%s_%s.csv" %(self.save_path, self.symbol, self.start, self.end))
        else:
            raise RuntimeError("Symbol: %s | Data is empty" % self.symbol)
