import trand as td
import copy
import matplotlib.pyplot as plt
import data_get as dg
import time
from interval import Interval as itv
from data_get import Peak

td.login()


def ma_deviation(cycle="m1", short=5, long=30):
    """均线之差效果图判断"""
    h1_5 = dg.ema(cycle, n=short)
    h1_30 = dg.ema(cycle, n=long)
    x_value = h1_5["ema"] - h1_30["ema"]
    xx = copy.deepcopy(x_value)
    i = 0
    while i != 299:
        xx[i] = x_value[i+1] - x_value[i]
        i += 1
    plt.bar([i for i in range(300)], x_value)
    plt.show()


def single_k(cy, k, func, capital=100):
    """基于单K线实时检测，
    cy：周期
    k: 定位K线，从哪里开始
    func：策略函数名
    capital：入金
    """
    for i in range(k, 0, -1):
        qd = dg.quote_data(cycle=cy, k=i)
        func(cy, qd, k)


def ema1(cy, data, k):
    k = k+2  # 表示批次，用于ema定位最后数据的ema
    m1_5 = dg.ema(cycle=cy, n=5, k=k, data=data, bach=k)
    m1_15 = dg.ema(cycle=cy, n=15, k=k, data=data, bach=k)

    return m1_5, m1_15


# single_k(cy="m15", func=ema1, k=2)

def buy_sell_only(buy_factor, sell_factor):
    """多单条件满足，开多平空
       空单条件满足，开空平多
       前提，同一时刻多空条件只能有一个成立
    """
    while True:
        a = td.Ticket_Comment()
        lens = len(a.tb)
        if buy_factor:  # 买单条件到
            if lens == 0:  # 没有任何单子
                td.buy(volume=0.01)
            elif (lens != 0) and (a.tb[0].type == 1):  # 或者已经有个空单子
                td.buy(volume=0.01)
                for i in range(lens):  # 平掉空单
                    if a.tb[i].type == 1:
                        td.close_tickets(lt=a.tb[i].volume, tp=a.tb[i].type, tk=a.tb[i].ticket)

        elif sell_factor:  # 卖单条件
            if lens == 0:  # 没有任何单子
                td.sell(volume=0.01)
            elif (lens != 0) and (a.tb[0].type == 0):  # 或者已经有个多单子
                td.sell(volume=0.01)
                for i in range(lens):  # 平掉多单
                    if a.tb[i].type == 0:
                        td.close_tickets(lt=a.tb[i].volume, tp=a.tb[i].type, tk=a.tb[i].ticket)
        else:
            print('没有做单条件满足，请等待...')
        time.sleep(1)


def extrusion_trend(lot=0.01, tp=1, sl=-3.8):
    """挤压行情走势"""
    x = 0
    y = 1
    while True:
        a = td.Ticket_Comment()
        lens = len(a.tb)
        if lens == 0:  # 开始随机下两单
            td.sell(volume=lot)
        for i in range(lens):
            if a.tb[i].profit > tp:  # 遍历盈利大于1的单子平仓，并顺势继续下单
                a.close_tickets(volume=a.tb[i].volume, typ=a.tb[i].type, ticket=a.tb[i].ticket)
                if lens in itv(1, 1.1) and a.tb[i].type == 0:  # 如果是多单盈利
                    td.buy(volume=lot)
                elif lens in itv(1, 1.1) and a.tb[i].type == 1:  # 如果是空单
                    td.sell(volume=lot)
            elif a.tb[i].profit in itv(-999, sl):  # 如果亏损-3.8，平掉，反向下单
                # x, y = y, x
                a.close_tickets(volume=a.tb[i].volume, typ=a.tb[i].type, ticket=a.tb[i].ticket)
                if lens in itv(1, 1.1) and a.tb[i].type == x:  # 多单亏损，反向下
                    td.sell(volume=lot)
                elif lens in itv(1, 1.1) and a.tb[i].type == y:  # 空单亏损，下多单
                    td.buy(volume=lot)
        time.sleep(0.1)


def position_order():
    """获取持仓单子，已经改单子的盈利"""
    p = {}
    tk_list = []
    obj = td.Ticket_Comment()
    lens = len(obj.tb)
    for i in range(lens):
        ticket = obj.tb[i].ticket
        profit = round(obj.tb[i].profit, 2)
        p[ticket] = profit
        tk_list.append(ticket)
    result = {'profit': p, 'tk_list': tk_list, "obj": obj}
    return result


# def extrusion_trend1(lot=0.01, tp=0.5, pct=0.2, sl=-3.8):
#     """顺势策略"""
#     result = position_order()
#     profit_dict = result["profit"]
#     tk_list = result["tk_list"]
#     obj = result["obj"]
#     zero = 0.00001*0.00001
#     while True:
#         # screen_list = []  # 盈利值大于screen阈值存储仓库
#         real_time_list = []  # 实时单子的单号仓库
#         a = td.Ticket_Comment()
#         lens = len(a.tb)
#         if lens == 0:  # 开始随机下两单
#             td.sell(volume=lot)
#         for i in range(lens):
#             real_time_list.append(a.tb[i].ticket)  # 先把所有单子存储起来
#
#             if a.tb[i].ticket not in profit_dict:  # 是否增加新的单子
#                 tk = a.tb[i].ticket
#                 profit = round(a.tb[i].profit, 2)
#                 profit_dict[tk] = profit  # 更新新单子，存储
#                 tk_list.append(tk)  # 并把单号提取出来
#
#             if a.tb[i].profit > profit_dict[obj.tb[i].ticket]:  # 检查单子盈利值是否创新高
#                 profit_dict[obj.tb[i].ticket] = round(a.tb[i].profit, 2)  # 并且记录更新
#
#             if a.tb[i].profit > profit_dict[obj.tb[i].ticket]:  # 检查单子盈利值是否创新高
#                 profit_dict[obj.tb[i].ticket] = round(a.tb[i].profit, 2)  # 并且记录更新
#
#             pf = (a.tb[i].profit / (profit_dict[obj.tb[i].ticket] + zero))
#             if (a.tb[i].profit > tp+zero) and (pf <= pct):
#                 td.close_tickets(lt=a.tb[i].volume, tp=a.tb[i].type, tk=a.tb[i].ticket)
#
#                 if lens in itv(1, 1.1) and a.tb[i].type == 0:  # 如果是多单盈利
#                     td.buy(volume=lot)
#
#                 elif lens in itv(1, 1.1) and a.tb[i].type == 1:  # 如果是空单
#                     td.sell(volume=lot)
#
#             elif a.tb[i].profit in itv(-999, sl):  # 如果亏损-3.8，平掉，反向下单
#                 td.close_tickets(lt=a.tb[i].volume, tp=a.tb[i].type, tk=a.tb[i].ticket)
#
#                 if lens in itv(1, 1.1) and a.tb[i].type == 0:  # 多单亏损，反向下
#                     td.sell(volume=lot)
#
#                 elif lens in itv(1, 1.1) and a.tb[i].type == 1:  # 空单亏损，下多单
#                     td.buy(volume=lot)
#
#         for r in tk_list:  # 遍历记录仓库，检查是否有新单子删除
#             if r not in real_time_list:
#                 tk_list.remove(r)  # 从仓库清除删除单子的痕迹
#                 profit_dict.pop(r)
#         print(profit_dict)
#         time.sleep(0.2)


def buy_stop_limit(high_line, buy_line, lot=0.01, sl=10, tp=10, beat=0.3, sb="XAUUSD"):
    """上涨到指定价格，回落到指定位置买入"""
    buy_signal_lamp = False  # 上线买入信号灯
    while True:  # 循环判断当前买价是否达到指定高度的价格区间
        if dg.ask(sb=sb) in itv(high_line-beat, high_line+beat):
            buy_signal_lamp = True  # 灯亮
            break
        else:
            # print("------------------------>未 达 到 指 定 上线 继续等待............")
            time.sleep(0.02)
    while True:  # 灯亮并且当前买价回落至指定做多价格振幅区间，买入
        if buy_signal_lamp and ((dg.ask(sb=sb)) == (buy_line in itv(buy_line-beat, buy_line+beat))):
            td.buy(symbol=sb, volume=lot, sl=sl, tp=tp)
            break
        else:
            # print("------------------------>达到上线,但未达到指定买入价格............")
            time.sleep(0.02)


def shock(high_line, low_line, lot=0.01, sl=4, tp=4, beat=0.3, sb="XAUUSD"):
    """指定上下线震荡策略"""
    while True:
        a = td.Ticket_Comment()
        lens = len(a.tb)
        if lens in itv(0, 1):
            if dg.ask(sb=sb) in itv(high_line-beat, high_line+beat):
                td.sell(volume=lot, sl=sl, tp=tp, symbol=sb)

            elif dg.ask(sb=sb) in itv(low_line - beat, low_line + beat):
                td.buy(volume=lot, sl=sl, tp=tp, symbol=sb)
            else:
                # print("------------------------>未 达 到 指 定 上线 继续等待............")
                time.sleep(0.02)
        if lens in itv(1, 5):
            for i in range(lens):
                if a.tb[i].profit > 1.8:  # 遍历盈利大于1的单子平仓
                    td.close_tickets(lt=a.tb[i].volume, tp=a.tb[i].type, tk=a.tb[i].ticket)
        time.sleep(0.2)
td.shutdown()





















