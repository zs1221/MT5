import time, math
import MetaTrader5 as mt5
import pandas as pd


LG = 67080706  # 账号
SERVER = "ForexTimeFXTM-Demo02"  # 服务器
PAS = "Zs123456"  # 密码

T = 0.001  # 重新做单睡眠时间0.001，防止市场活跃，出现跳单
ML = 300  # 默认预付款比例最低 300% ，再低无法加仓
PC = 10  # 10% 仓位 请调用进行下单
PF = [0., 9**9] # 默认盈利0.2平仓

# 买单参数控制
SYMBOL_BUY = 'XAUUSD'
VOLUME_BUY = None # 不可指定，必须手动设置
SL_BUY = 10
TP_BUY = 10
DEVIATION_BUY = 20
COMMENT_BUY = 'buy'  # 做单描述信息
MAGIC_BUY = 888888  # 魔法单号

# 卖单参数控制
SYMBOL_SELL = 'XAUUSD'
VOLUME_SELL = None
SL_SELL = 10
TP_SELL = 10
DEVIATION_SELL = 20
COMMENT_SELL = 'sell'
MAGIC_SELL = 66666

LOGIN = False  # 判断是否登录，未登录禁止买卖


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)


# 链接服务器
def login(lg=LG, pas=PAS, server=SERVER):
    global LOGIN
    init = mt5.initialize(login=lg, server=server, password=pas)
    if init:
        LOGIN = True
    else:
        print("登录失败")

# 断开服务器
def shutdown():
    mt5.shutdown()


# 买入函数
def ask_false(volume, symbol=SYMBOL_BUY, sl=SL_BUY, tp=TP_BUY,
              deviation=DEVIATION_BUY, magic=MAGIC_BUY, comment=COMMENT_BUY):

    price = mt5.symbol_info_tick(symbol).ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "sl": price - sl,
        "tp": price + tp,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode),"1027 开启允许")
        print('buy---重新买入')
        time.sleep(T)
        return ask_false(volume=VOLUME_BUY)
    else:
        print("买入成功---买入价： ", price)
        return request, result.order

# 买入函数
def buy(volume, margin_level=ML, symbol=SYMBOL_BUY, sl=SL_BUY, tp=TP_BUY,
        deviation=DEVIATION_BUY, magic=MAGIC_BUY, comment=COMMENT_BUY):
    global VOLUME_BUY
    VOLUME_BUY = volume
    acc = account()
    margin_level = acc['margin_level']
    if LOGIN and (margin_level == 0. or margin_level >= ML) and volume < 1:
        return ask_false(symbol=symbol, volume=volume, sl=sl, tp=tp,
                         deviation=deviation, magic=magic, comment=comment)
    elif margin_level <= ML:
        print('资金太少，不要加仓...  预付款比例：  %.2f' % margin_level)
        print('或者手数太大 0.99')
    else:
        print('请链接MT5服务...或手数太高')


# 卖出函数
def bid_false(volume, symbol=SYMBOL_SELL, sl=SL_SELL, tp=TP_SELL,
               deviation=DEVIATION_SELL, magic=MAGIC_SELL, comment=COMMENT_SELL,):
    price = mt5.symbol_info_tick(symbol).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "sl": price + sl,
        "tp": price - tp,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print('sell---重新卖出')
        time.sleep(T)
        return bid_false(volume=VOLUME_SELL)
    else:
        print("卖出成功---卖出价： ", price)
        return request, result.order


# 卖出函数
def sell(volume, margin_level=ML, symbol=SYMBOL_SELL, sl=SL_SELL,tp=TP_SELL,
         deviation=DEVIATION_SELL, magic=MAGIC_SELL, comment=COMMENT_SELL):
    global VOLUME_SELL
    VOLUME_SELL= volume
    acc = account()
    margin_level = acc['margin_level']
    if LOGIN and (margin_level == 0. or margin_level >= ML) and volume < 1:
        return bid_false(symbol=symbol, volume=volume, sl=sl, tp=tp,
                         deviation=deviation, magic=magic, comment=comment)
    elif margin_level <= ML:
        print('资金太少，不要加仓...  预付款比例：  %.2f' % margin_level)
        print('或者手数太大 0.99')
    else:
        print('请链接MT5服务...或手数太高')


# 关闭买函数
def ask_buy_close(pid, symbol=SYMBOL_BUY, deviation=DEVIATION_BUY, comment="zs",
              action=mt5.TRADE_ACTION_DEAL, magic=234000):
    for p in pid[["ticket", "volume", "profit"]].values:
        price = mt5.symbol_info_tick(symbol).bid
        buy_request_close = {
            "action": action,
            "symbol": symbol,
            "volume": p[1],
            "type": mt5.ORDER_TYPE_SELL,
            "position": int(p[0]),
            "price": price,
            "deviation": deviation,
            "magic": magic,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        # 发送交易请求
        result = mt5.order_send(buy_request_close)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("retcode={}".format(result.retcode), "  1027 开启允许")


# 关闭卖函数
def bid_sell_close(pid, symbol=SYMBOL_BUY, deviation=DEVIATION_SELL, comment="zs",
              action=mt5.TRADE_ACTION_DEAL, magic=234000):
    for p in pid[["ticket", "volume", "profit"]].values:
        price = mt5.symbol_info_tick(symbol).ask
        sell_request_close = {
            "action": action,
            "symbol": symbol,
            "volume": p[1],
            "type": mt5.ORDER_TYPE_BUY,
            "position": int(p[0]),
            "price": price,
            "deviation": deviation,
            "magic": magic,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        # 发送交易请求
        result = mt5.order_send(sell_request_close)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("retcode={}".format(result.retcode), "  1027 开启允许")



# 关闭指定单子函数
def one_close(lot, type, ticket, price):
        request = {
            "action": 1,
            "symbol": SYMBOL_BUY,

            "volume": lot,
            "type": type,
            "position": ticket,
            "price": price,

            "deviation": 20,
            "magic": 123456,
            "comment": 'zzz',
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        # 发送交易请求
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("关闭失败:  ", result.retcode)
            return 0
        else:
            if type:
                print("买单 关闭成功 单号: {}".format(ticket))
                print("")
            else:
                print("卖单 关闭成功 单号: {}".format(ticket))
                print("")
            return 1


# 盈利单子判断
def tp_judgment(profit=[0.2]):
    """判断盈利值大于0.2就返回盈利的单号df格式"""
    usd_positions = mt5.positions_get(group=SYMBOL_BUY)
    if len(usd_positions):
        df = pd.DataFrame(list(usd_positions), columns=usd_positions[0]._asdict().keys())
        tp = df[["ticket", "profit", "volume", "type"]]
        # print(df)
        if isinstance(profit, list):
            if len(profit) == 1:
                tt = tp.loc[(tp["profit"]) >= profit[0]].head(100)
                # print("满足条件的单子是： ", "\n", tt)
                return tt[["ticket", "volume", "profit", "type"]]
            elif len(profit) == 2:
                tt = tp.loc[(tp["profit"] >= profit[0]) & (tp["profit"] <= profit[1])]
                # print("满足条件的单子是： ", "\n", tt)
                return tt[["ticket", "volume", "profit", "type"]]
            else:
                print("输入有误,只能是两个数")
        else:
            print("请输入 ‘列表’ 类型数据")
    else:
        print("无单子可关闭，请做单子..")

# 盈利单子类型分类
def tk_sort(pf):
    """根据盈利的单子进行种类分类，目的：快速平单"""
    pid = tp_judgment(profit=pf)
    try:
        tp = pid.groupby("type")["type"].count().reset_index(name="各种类总数")
    except Exception :
        print("单子已经平仓完成...")
        print("")
        time.sleep(0.1)
        return None
    try:
        if tp.shape[0] == 2:                       # 判断单子类型  买卖均在
            tk_buy = pid.loc[pid["type"] == 0]
            tk_sel = pid.loc[pid["type"] == 1]
            ask_buy_close(tk_buy)
            bid_sell_close(tk_sel)
            return 2
        if (tp.shape[0] == 1) & (tp.iloc[0, 0] == 0):  # 只有买单类型
            tk_buy = pid.loc[pid["type"] == 0]
            ask_buy_close(tk_buy)
            return 0
        if (tp.shape[0] == 1) & (tp.iloc[0, 0] == 1):  # 只有卖单类型
            tk_sel = pid.loc[pid["type"] == 1]
            bid_sell_close(tk_sel)
            return 1
    except Exception as er:
        pass

def account_position():  # 账户未结持仓数目
    positions_total = mt5.positions_total()
    if positions_total > 0:
        print("持仓单量: ", positions_total)
        return positions_total
    else:
        print('持仓单量: 0 ')
        return 0

# 关闭所有类型单子可以指定盈利值
def  close_profit(profit=PF, ptime=0.02):
    """pt指定关闭单子时间间隔"""
    while True:
        time.sleep(ptime)
        a = Ticket_Comment()
        if len(a.tb) == 0:
            break
        tk_sort(pf=profit)


def close_ticket(data):
    """关闭指定单不考虑是否盈利"""
    lt = data[0]['volume']
    tp = data[0]['type']
    tk = data[1]
    while True:
        price_ask = mt5.symbol_info_tick(SYMBOL_BUY).ask
        price_bid = mt5.symbol_info_tick(SYMBOL_BUY).bid
        if tp:  # 卖单tp=1
            if one_close(lot=lt, type=tp-1, ticket=tk, price=price_ask):
                break
            else:
                print('关闭失败')
                time.sleep(0.02)
        else:  # 买单tp=0
            if one_close(lot=lt, type=tp+1, ticket=tk, price=price_bid):
                break
            else:
                print('关闭失败')
                time.sleep(0.02)
    return {"单号": tk, "类型": tp, "手数": lt}


# 返回标准账户6条信息
def account():
    """获取账户标准信息6条"""
    tf = mt5.account_info()._asdict()
    return {i: tf[i] for i in tf if i in ['margin_free', 'margin_level', 'balance', 'equity', 'margin', 'profit']}


# 仓位控制函数
def position_control(position=PC):
    """仓位控制默认10%仓位下单"""
    acc = account()
    control = PC/100
    margin_free = acc['margin_free']
    if margin_free <= 40:
        lot = 0.01
    else:
        lot = math.floor(acc['margin_free']*control/3.88)/100
        if lot >= 1:
            lot = 0.99 # 平台问题只能最大下0.99手
    return lot


class Ticket_Comment(object):
    """订单数据的描述信息
    ticket  volume  type  profit  price_open  symbol  sl  tp  time
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, tk_id=None):
        if tk_id is None:
            try:
                self.tb = mt5.positions_get()
            except Exception as e:
                print('获取单子失败')
                time.sleep(3)
                self.tb = mt5.positions_get()
        else:
            self.tb = mt5.positions_get(ticket=tk_id)

    def lens(self):
        try:
            lens = len(self.tb)
        except TypeError:
            print("服务器关闭")
            return 0
        return lens

    @staticmethod
    def close_tickets(volume, typ, ticket):
        """关闭指定单不考虑是否盈利
        lt: 手数    tp: 类型    tk：单号
        """
        while True:
            price_ask = mt5.symbol_info_tick(SYMBOL_BUY).ask
            price_bid = mt5.symbol_info_tick(SYMBOL_BUY).bid
            if typ == 1:  # 卖单tp=1
                if one_close(lot=volume, type=typ-1, ticket=ticket, price=price_ask):
                    break
                else:
                    time.sleep(0.01)
            else:  # 买单tp=0
                if one_close(lot=volume, type=typ+1, ticket=ticket, price=price_bid):
                    break
                else:
                    time.sleep(0.01)
        return {"单号": ticket, "类型": typ, "手数": volume}


