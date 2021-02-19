import trand as td
import data_get as dg
from interval import Interval as itv
import time
import socket


td.login()





class Peak_Business(dg.Peak):
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, "_instance"):
    #         cls._instance = super().__new__(cls, *args, **kwargs)
    #         return cls._instance

    def __init__(self, cy="m1", k=100):
        self.res_buy = self.peak_buy(cy, k)
        self.res_sell = self.peak_sell(cy, k)
        self.res_close_buy = self.peak_close_buy()
        self.res_close_sell = self.peak_close_sell()

    def peak_buy(self, cy='m1', k=100):
        """买入条件函数"""
        peak_result = super().peak_process(cy, k)
        b_buy = peak_result['res_low']
        print('b_buy', b_buy)
        if len(b_buy) == 1:
            if dg.bid() in itv(b_buy[0]+0.8, b_buy[0]-0.2):
                return 1
        if len(b_buy) > 1:
            if dg.bid() in itv(min(b_buy), max(b_buy)):
                return 1  # 买
        else:
            return 0

    def peak_sell(self, cy='m1', k=100):
        """卖出条件函数"""
        peak_result = super().peak_process(cy, k)
        s_sell = peak_result['res_high']
        print('s_sell', s_sell)
        if len(s_sell) == 1:
            if dg.bid() in itv(s_sell[0]+1.2, s_sell[0]-0.3):
                return 1
        if len(s_sell) > 1:
            if dg.bid() in itv(min(s_sell), max(s_sell)):
                return 1  # 卖
        else:
            return 0

    def peak_close_buy(self):
        """止盈买单条件函数"""
        if self.peak_sell() == 1:
            return 1
        else:
            return 0

    def peak_close_sell(self):
        """止盈空单条件函数"""
        if self.peak_buy() == 1:
            return 1
        else:
            return 0

    def innovation_low(self, cy='h4', k=80):
        """是否创新低函数"""
        min_value = dg.low_data(dg.cycle_judge_price(cy, k))
        low = list(dg.cycle_judge_price(cy, k).low.tail(2))[-2]
        if low < min_value:
            return 1  # 创新低了
        else:
            return 0

    def innovation_high(self, cy='h4', k=80):
        """是否创新高函数"""
        max_value = dg.high_data(dg.cycle_judge_price(cy, k))
        high = list(dg.cycle_judge_price(cy, k).high.tail(2))[-2]
        if high > max_value:
            return 1  # 创新高了
        else:
            return 0
# peak = Peak()
# peak_result = peak.peak_process('m5', k=80)
# b_buy = True if bid() in itv(min(peak_result["low_list"]), max(peak_result["low_list"])) else False
# s_sell = True if bid() in itv(min(peak_result["high_list"]), max(peak_result["high_list"])) else False


def extrusion_trend(lot=0.01, tp=1, sl=-3.8):
    """顺势策略"""
    while True:
        a = td.Ticket_Comment()
        for i in range(a.lens()):
            if a.tb[i].profit >= 1:
                a.close_tickets(a.tb[i].volume, a.tb[i].type, a.tb[i].ticket)
            print('i', i)
            if a.lens() in itv(1, 1.9):
                print('进入')
                # td.buy(volume=0.01)
                if 1 < 2:
                    print('买入.........')
        print("*************")
        time.sleep(3)






















td.shutdown()




