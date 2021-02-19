import trand as td
import data_get as dg
from math import floor
import think_tank as tt
import pandas as pd
from collections import Counter
import time
from interval import Interval as itv
td.login()


class Peak(object):
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, "_instance"):
    #         cls._instance = super().__new__(cls, *args, **kwargs)
    #     return "_instance"

    def __init__(self):
        pass

    @staticmethod
    def peak(cy='m1', k=100):
        """历史极值点获取"""
        high = dg.cycle_judge_price(cy, k).high
        low = dg.cycle_judge_price(cy, k).low
        high_time = dg.cycle_judge_price(cy, k).time
        low_time = dg.cycle_judge_price(cy, k).time
        peak_high = pd.DataFrame(columns=['time', 'high'])
        peak_low = pd.DataFrame(columns=["time", "low"])
        i, h, l = 0, 0, 0  # i 循环遍历获取的K线数据， h统计high满足极值点的数目， l统计low满足极值点的数目

        while i < len(high)-6:
            middle_high = high[i+3]  # 第三根K线数据，最高值
            middle_low = low[i+3]
            middle_high_time = high_time[i+3]
            middle_low_time = low_time[i+3]

            if high[i+0] < middle_high and high[i+1] < middle_high and high[i+2] < middle_high:
                if high[i+4] < middle_high and high[i+5] < middle_high and high[i+6] < middle_high:
                    peak_high.loc[h] = middle_high_time, middle_high  # 满足条件，更新数据
                    h += 1

            if low[i+0] > middle_low and low[i+1] > middle_low and low[i+2] > middle_low:
                if low[i+4] > middle_low and low[i+5] > middle_low and low[i+6] > middle_low:
                    peak_low.loc[l] = middle_low_time, middle_low
                    l += 1
            i += 1
        print(peak_high, '\n')
        print(peak_low, '\n')
        return peak_high, peak_low

    def peak_process(self, cy='m1', k=100):
        high, low = self.peak(cy, k)
        high_list = []  # 去除小数后的存放high仓库
        low_list = []
        res_high = []  # 存放次数相同， 不同的点位仓库
        res_low = []

        for h in high.high:  # 清除小数，保存仓库
            high_list.append(floor(h))
        h_cont = dict(Counter(high_list))
        one_max_high_value = max(h_cont.values())  # 第一压力位出现的次数

        try:
            for key, value in h_cont.items():
                if value == max(h_cont.values()):
                    res_high.append(key)
            print('{}: high 各值次数统计----> {}'"\n"'{}---> {}次'.format(cy, h_cont, res_high, max(h_cont.values())), '\n')
        except ValueError:
            print('high数据为空')

        for lo in low.low:
            low_list.append(floor(lo))
        l_cont = dict(Counter(low_list))
        one_max_low_value = max(l_cont.values())  # 第一支撑位出现的次数

        try:
            for key, value in l_cont.items():
                if value == max(l_cont.values()):
                    res_low.append(key)
            print('{}: low 各值次数统计-----> {}'"\n"'{}---> {}次'.format(cy, l_cont, res_low, max(l_cont.values())), '\n')
        except ValueError:
            print('low 数据为空')

        result = {
            'high_list': h_cont,  # {1871: 1, 1873: 3, 1875: 2, 1874: 1, 1876: 1}
            'low_list': l_cont,  # {1869: 1, 1870: 3, 1871: 3, 1872: 4}
            'high': res_high,  # [1873]---> 3次
            'low': res_low,  # [1872]---> 4次
            'one_max_high_value': one_max_high_value,  # 3
            'one_max_low_value': one_max_low_value  # 4
        }
        return result


peak = Peak()
p = peak.peak_process('m15', 100)


td.shutdown()


















