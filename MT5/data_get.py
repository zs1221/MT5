from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pytz import timezone
import re
import trand as td
from interval import Interval as itv
from math import floor
from collections import Counter

KC = 500  # 表示300根K线计算指标

first = False  # 判断数据是否首次传入
cache = None  # 数据中转站

pd.set_option('display.float_format', lambda x: '%.3f' % x)  # 保留3位小数
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1500)
timezone = timezone("Etc/UTC")

symbol = "XAUUSD"
K = 30  # 默认最近30根K线显示
date = (datetime.now()+timedelta(days=1)).strftime("%Y %m %d").split(" ")
date = [int(i) for i in date]  # [2020, 9, 11]  # 当前时间+1


# 获取开始日期
def get_date(k=0, cy="m1"):
    data = cycle_judge_price(cycle=cy, k=k)  # 调用周期判断
    # st, et = data.loc[[0], ["time"]], data.loc[[k-1], ["time"]]
    st = data.loc[[0], ["time"]]
    st = [int(i) for i in re.findall(r"\d+", pd.Series.to_string(st["time"]))][1:-1]  # 获取第K根K线时间
    # et = [int(i) for i in re.findall(r"\d+", pd.Series.to_string(et["time"]))][1:-1]
    print(st)
    return st


# 获取第K根k线实时报价数据
def quote_data(cycle="m1", k=0, sb=symbol):
    """获取k线实时报价数据 k=0 当前， k=1上根"""
    st = get_date(cy=cycle, k=k+1)  # 获取周期数据
    st_y, st_m, st_d, st_h, st_f = st  # 年，月，日，时，分，
    st_date = datetime(st_y, st_m, st_d, st_h, st_f, 0, tzinfo=timezone)
    # ed_date = datetime(et_y, et_m, et_d, et_h, et_f, 0, tzinfo=timezone)
    # ed_date = ed_date + timedelta(minutes=1)
    t = time_judge(cy=cycle)   # 时间周期判断，返回时间数字
    ed_date = (st_date + timedelta(minutes=t))  # 表示返回第K根K线时间结束时间

    rates = mt5.copy_ticks_range(sb, st_date, ed_date, mt5.COPY_TICKS_INFO)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


# 时间周期判断
def time_judge(cy=None):
    if cy == "m1":
        return 1
    if cy == "m5":
        return 5
    if cy == "m15":
        return 15
    if cy == "m30":
        return 30
    if cy == "h1":
        return 60
    if cy == "h4":
        return 240
    if cy == "d1":
        return 1440
    if cy == "w1":
        return 10080


def m1(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M1, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def m2(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M2, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def m3(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M3, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def m4(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M4, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def m5(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M5, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def m6(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M6, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def m10(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M10, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def m12(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M12, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def m15(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M15, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def m20(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M20, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def m30(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_M30, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def h1(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_H1, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def h2(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_H2, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def h3(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_H3, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def h4(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_H4, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def h6(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_H6, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def h8(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_H8, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def h12(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_H12, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def d1(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_D1, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def w1(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_W1, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def mn1(sb=symbol, k=K, t=date):
    """获取数据，周期，日期+1， K线数量"""
    y, m, d = t
    rates = mt5.copy_rates_from(sb, mt5.TIMEFRAME_MN1, datetime(y, m, d, tzinfo=timezone), k)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame


def yang_line(data):
    """阳线长度"""
    da = data['close'] - data['open']
    return da


def yin_line(data):
    """阴线长度"""
    da = data["open"] - data['close']
    return da


def up_line(data):
    """K线上沿线"""
    if yang_line(data)[1]:
        return data["close"]  # 阳  收
    else:
        return data["open"]   # 阴  开


def dw_line(data):
    """K线下沿线"""
    if yang_line(data)[1]:
        return data["open"]   # 阳 开
    else:
        return data["close"]  # 阴 收


def high_data(data):
    """K线的最大值"""
    return data['high'].max()


def low_data(data):
    """K线的最小值"""
    return data["low"].min()


def tk_volume(data):
    """获取成交量"""
    return data["tick_volume"]


def ask(sb=symbol):
    """实时  买价  """
    return mt5.symbol_info_tick(symbol).ask


def bid(sb=symbol):
    """实时  卖价  """
    return mt5.symbol_info_tick(symbol).bid


def cycle_judge(cycle=None):
    if cycle == "m1":
        return m1(k=KC)
    if cycle == "m5":
        return m5(k=KC)
    if cycle == "m15":
        return m15(k=KC)
    if cycle == "m30":
        return m30(k=KC)
    if cycle == "h1":
        return h1(k=KC)
    if cycle == "h4":
        return h4(k=KC)
    if cycle == "d1":
        return d1(k=KC)
    if cycle == "w1":
        return w1(k=KC)
    if cycle == "mn1":
        return mn1(k=KC)
    else:
        print("输入周期错误")


def cycle_judge_price(cycle=None, k=0):
    if cycle == "m1":
        return m1(k=k)
    if cycle == "m5":
        return m5(k=k)
    if cycle == "m15":
        return m15(k=k)
    if cycle == "m30":
        return m30(k=k)
    if cycle == "h1":
        return h1(k=k)
    if cycle == "h4":
        return h4(k=k)
    if cycle == "d1":
        return d1(k=k)
    if cycle == "w1":
        return w1(k=k)
    if cycle == "mn1":
        return mn1(k=k)
    else:
        print("输入周期错误")


def ema(cycle="m1", n=5, k=0, al=True, data=None, bach=None):
    """ n:12日均线
        k：当前K线,价格定位
        al:默认取所有数据
        data:判断是否传入数据
        bach：用于定位策略ema均线数据
    """
    loc = KC + k
    if data is None:
        cy = cycle_judge_price(cycle=cycle, k=loc)
        cy.rename(columns={"spread": "ema", "real_volume": "dif"}, inplace=True)
        cy.loc[[0], ["ema"]] = cy["close"][0]
        y1 = cy["close"][0]
        for i in range(1, loc):
            y1 = y1 * (n-1)/(n+1) + cy["close"][i]*2/(n+1)
            cy.loc[[i], ["ema"]] = y1
        tail = pd.Series.to_list(cy.loc[[loc-k-2], ["ema"]])
        return cy if al is True else round(tail[0][0], 3)
    else:
        global first, cache
        qd = data
        lens = len(qd)
        qd.rename(columns={"last": "ema"}, inplace=True)

        if not first:
            a = ema(cycle=cycle, n=5)
            y1 = a["ema"][len(a)-bach]
            for i in range(len(qd)):
                x1 = y1 * (n - 1) / (n + 1) + qd["bid"][i] * 2 / (n + 1)
                qd.loc[[i], ["ema"]] = x1
            cache = (qd["ema"][lens-1])

            first = True
            # 返回全部或最后一条数据
            return qd if al is True else round(qd["ema"][lens-1], 3)

        else:
            y1 = cache

            for i in range(lens):
                x1 = y1 * (n - 1) / (n + 1) + qd["bid"][i] * 2 / (n + 1)
                qd.loc[[i], ["ema"]] = x1
            cache = (qd["ema"][lens-1])

            return qd if al is True else round(qd["ema"][lens-1], 3)


def macd(cycle="h4", short=12, long=26, m=9, k=0, data=None):
    dea = 0
    st = ema(cycle=cycle, n=short) if data is None else data
    lg = ema(cycle=cycle, n=long) if data is None else data

    dif = st["ema"] - lg["ema"]
    st["dif"] = dif
    st.rename(columns={"ema": "dea"}, inplace=True)
    for i in range(KC):
        dea = dea * (m-1) / (m+1) + st["dif"][i] * 2.0 / (m + 1)
        st.loc[[i], ["dea"]] = dea
    return st


# def ema(cy, n=5):
#     cy.rename(columns={"spread": "ema", "real_volume": "dif"}, inplace=True)
#     cy.loc[[0], ["ema"]] = cy["close"][0]
#     y1 = cy["close"][0]
#     for i in range(1, len(cy["close"])):
#         y1 = y1 * (n - 1) / (n + 1) + cy["close"][i] * 2 / (n + 1)
#         cy.loc[[i], ["ema"]] = y1
#     return cy["ema"]


def main_capital_activity(cy="m1", k=0, sb=symbol):
    """主力资金数据活跃度获取"""
    a = quote_data(cycle=cy, k=k, sb=sb)  # 获取数据
    total = len(a)  # 求跳动总数
    a['last'] = (a['bid'] + a['ask']) / 2  # 取中值
    for i in range(total - 1):
        a.loc[[i + 1], ['volume']] = a['bid'][i + 1] - a['bid'][i]  # 获取差值
    up_number = len(a.loc[a["volume"] >= 0]) - 1  # 向上跳动的数目
    dw_number = len(a.loc[a["volume"] < 0])  # 向下跳动的数目
    up_price = a.loc[a["volume"] >= 0]['volume']  # 向上所有价格差
    dw_price = a.loc[a["volume"] < 0]['volume']  # 向下所有价格差
    up_total = round(up_price.sum(), 3)  # 向上跳动累加和
    dw_total = round(dw_price.sum(), 3)  # 向下跳动累加和
    k_solid = round((up_total + dw_total), 3)  # k线实体部分
    data = {'up_price': up_price,
            'up_number': up_number,
            'up_sum': up_total,
            'dw_price': dw_price,
            'dw_number': dw_number,
            'dw_sum': dw_total,
            'k_solid': k_solid,
            'total': total,  # K跳动总数
            'k_data': a,  # K线总数据
            }
    return data


def main_capital_figure(cy='m1', k=10, sb=symbol):
    """主力跳动量图形展示，基于每分钟"""
    # 设置正常显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    m = []  # 上涨仓库
    d = []  # 下跌仓库
    percentage = []  # 百分比
    for t in range(k):
        dt = main_capital_activity(cy=cy, k=t, sb=sb)
        dw_sum = -1 * dt['dw_sum']
        m.append(dt['up_sum'])
        d.append(dw_sum)
        if dt['up_sum'] > dw_sum:  # 上涨百分比
            percentage.append(round(dw_sum/dt['up_sum'], 2))
        else:
            percentage.append(round(dt['up_sum']/dw_sum, 2))
    wid = 0.3
    index_up = np.arange(k)
    index_dw = index_up + 0.3
    plt.bar(index_up, m[::-1], width=wid, color='r', label='上涨')
    plt.bar(index_dw, d[::-1], width=wid, color='g', label='下跌')

    plt.legend()  # 显示图例
    plt.ylabel('跳动量')  # 纵坐标轴标题
    plt.xlabel('百分比%', color='b')
    plt.title('主力资金活跃度判断')  # 图形标题
    plt.xticks(index_up + wid / 2, percentage[::-1])
    plt.show()


def peak(cy='m1', k=100):
    """历史极值点获取"""
    high = cycle_judge_price(cy, k).high
    low = cycle_judge_price(cy, k).low
    record_high = high[0]
    record_low = low[0]
    high_list = []
    low_list = []

    i = 0

    while i < len(high)-6:
        middle_high = high[i+3]
        middle_low = low[i+3]
        if high[i+0] < middle_high and high[i+1] < middle_high and high[i+2] < middle_high:
            if high[i+4] < middle_high and high[i+5] < middle_high and high[i+6] < middle_high:
                high_list.append(middle_high)

        if low[i+0] > middle_low and low[i+1] > middle_low and low[i+2] > middle_low:
            if low[i+4] > middle_low and low[i+5] > middle_low and low[i+6] > middle_low:
                low_list.append(middle_low)
        i += 1
    print(high_list[::-1])
    print(low_list[::-1])
    return high_list, low_list


def peak_test(f=0.5):
    how, low = peak(cy="m1", k=120)
    as_k = ask()
    bi_d = bid()
    for ll in how:
        if ll in itv(ask-f, ask+f):
            td.sell(volume=0.01)
    for sel in low:
        if sel in itv(bid-f, bid+f):
            td.buy(volume=0.01)


class Peak(object):
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, "_instance"):
    #         cls._instance = super().__new__(cls, *args, **kwargs)
    #     return "_instance"
    #
    # def __init__(self):
    #     pass

    @staticmethod
    def peak(cy='m1', k=100):
        """历史极值点获取"""
        high = cycle_judge_price(cy, k).high
        low = cycle_judge_price(cy, k).low
        high_time = cycle_judge_price(cy, k).time
        low_time = cycle_judge_price(cy, k).time
        peak_high = pd.DataFrame(columns=['time', 'high'])
        peak_low = pd.DataFrame(columns=["time", "low"])
        i, h, l = 0, 0, 0  # i 循环遍历获取的K线数据， h统计high满足极值点的数目， l统计low满足极值点的数目

        while i < len(high) - 6:
            middle_high = high[i + 3]  # 第三根K线数据，最高值
            middle_low = low[i + 3]
            middle_high_time = high_time[i + 3]
            middle_low_time = low_time[i + 3]

            if high[i + 0] < middle_high and high[i + 1] < middle_high and high[i + 2] < middle_high:
                if high[i + 4] < middle_high and high[i + 5] < middle_high and high[i + 6] < middle_high:
                    peak_high.loc[h] = middle_high_time, middle_high  # 满足条件，更新数据
                    h += 1

            if low[i + 0] > middle_low and low[i + 1] > middle_low and low[i + 2] > middle_low:
                if low[i + 4] > middle_low and low[i + 5] > middle_low and low[i + 6] > middle_low:
                    peak_low.loc[l] = middle_low_time, middle_low
                    l += 1
            i += 1
        # print(peak_high, '\n')
        # print(peak_low, '\n')
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
            'h_cont': h_cont,  # {1871: 1, 1873: 3, 1875: 2, 1874: 1, 1876: 1}
            'l_cont': l_cont,  # {1869: 1, 1870: 3, 1871: 3, 1872: 4}
            'high_list': high_list,
            'low_list': low_list,
            'res_high': res_high,  # [1873]---> 3次
            'res_low': res_low,  # [1872]---> 4次
            'one_max_high_value': one_max_high_value,  # 3
            'one_max_low_value': one_max_low_value  # 4
        }
        return result






