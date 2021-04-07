import pandas as pd
import numpy as np

class Trader():

    def __init__(self, principal = 1000, col_price = "price", col_date = "date", col_isBuy = "isBuy"):
        self.principal = principal
        self.profit = principal
        self.holding = False
        self.buyPrice = None
        self.buyDate = None
        self.col_price = col_price
        self.col_date = col_date
        self.col_isBuy = col_isBuy

        self.record = pd.DataFrame()

    def do_dailyOperation(self, info):
        if np.isnan(info[self.col_isBuy]):
            return
        if info[self.col_isBuy]:
            self.do_buy(info)
        else:
            self.do_sell(info)
    

    def do_sell(self, info):
        if self.holding:
            # perform sell
            holding_period_return = info[self.col_price] / self.buyPrice - 1

            # change profit to reflect sell
            self.profit *= (1 + holding_period_return)


            # preform save record

            date_start = self.buyDate
            date_end = info[self.col_date]
            buyPrice = self.buyPrice
            sellPrice = info[self.col_price]
            endProfit = self.profit

            self.save_record(date_start, date_end, buyPrice, sellPrice, holding_period_return, endProfit)


            
            # reset trader state
            self.holding = False
            self.buyDate = None
            self.buyPrice = None

        else:
            pass

    def do_buy(self, info):
        if self.record.empty:
            date_start = self.buyDate
            date_end = info[self.col_date]
            buyPrice = self.buyPrice
            sellPrice = info[self.col_price]
            endProfit = self.profit
            self.save_record(date_start, date_end, buyPrice, sellPrice, 0, endProfit)

        if self.holding:
            pass
        else:
            # perform buy operation

            # setting trader state
            self.holding = True
            self.buyDate = info[self.col_date]
            self.buyPrice = info[self.col_price]

    
    def save_record(self, start, end, buyPrice, sellPrice, holding_period_return, endProfit):
        row = {
            "date_start": start, 
            "date_end": end, 
            "buyPrice": buyPrice, 
            "sellPrice": sellPrice, 
            "return": holding_period_return, 
            "endProfit": endProfit
        }
        row = pd.DataFrame(row, index = [0])
        if self.record.empty:
            self.record = row
        else:
            self.record = self.record.append(row, ignore_index=True)

    def get_record(self):
        return self.record
        


