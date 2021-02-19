import pandas as pd
from HP_formula import *
import MetaTrader5 as mt5
import HP_mt5 as hmt5

# 建立与MetaTrader 5程序端的连接
if not hmt5.initialize():
    print("initialize() failed, error code =", hmt5.last_error())
    quit()

'''
TIMEFRAME 是一个包含可能图表周期值的枚举
ID	         描述
TIMEFRAME_M1	1分钟
TIMEFRAME_M2	2 分钟
TIMEFRAME_M3	3 分钟
TIMEFRAME_M4	4 分钟
TIMEFRAME_M5	5 分钟
TIMEFRAME_M6	6 分钟
TIMEFRAME_M10	10 分钟
TIMEFRAME_M12	12 分钟
TIMEFRAME_M12	15 分钟
TIMEFRAME_M20	20 分钟
TIMEFRAME_M30	30 分钟
TIMEFRAME_H1	1 小时
TIMEFRAME_H2	2 小时
TIMEFRAME_H3	3 小时values
TIMEFRAME_H4	4 小时
TIMEFRAME_H6	6 小时
TIMEFRAME_H8	8 小时
TIMEFRAME_H12	12 小时
TIMEFRAME_D1	1 天
TIMEFRAME_W1	1 周
TIMEFRAME_MON1	1 个月
'''
# 在UTC时区，获取01.10.2020开始的10个EURUSD H4柱形图
rates = hmt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_H1, 0, 2440)
df = hmt5.tohpdata(rates)
print(df)

# 下面是小白仿通达信公式系统计算
# 首先要对数据预处理
mydf = df.copy()
CLOSE = mydf['close']
LOW = mydf['low']
HIGH = mydf['high']
OPEN = mydf['open']
C = mydf['close']
L = mydf['low']
H = mydf['high']
O = mydf['open']


def RSI(N1=6, N2=12, N3=24):
    """
    RSI 相对强弱指标
    """
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1, 1) / SMA(ABS(CLOSE - LC), N1, 1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2, 1) / SMA(ABS(CLOSE - LC), N2, 1) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3, 1) / SMA(ABS(CLOSE - LC), N3, 1) * 100

    return RSI1, RSI2, RSI3


# 假定我们使用RSI指标
r1, r2, r3 = RSI()

mydf = mydf.join(pd.Series(r1, name='RSI1'))
mydf = mydf.join(pd.Series(r2, name='RSI2'))
mydf = mydf.join(pd.Series(r3, name='RSI3'))
mydf['S80'] = 80  # 增加上轨80轨迹线
mydf['X20'] = 20  # 增加下轨20轨迹线

mydf = mydf.tail(100)  # 显示最后100条数据线

# 下面是绘线语句
mydf.S80.plot.line()
mydf.X20.plot.line()
mydf.RSI1.plot.line(legend=True)
mydf.RSI2.plot.line(legend=True)
mydf.RSI2.plot.line(legend=True)

MACD()

# 断开与MetaTrader 5程序端的连接
hmt5.shutdown()
