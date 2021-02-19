#[小白混沌交易] 
'''
[小白混沌高频交易策略] 

最大多单=10
最大空单=10
x=0.5 #价格步长
y=1.0  #总赢利阀值
z=-4.0  #亏损阀值

1、软件启动，取1分钟线价格p。
2、如果p变动+x，且 多单数<最大多单，开多单。p=p+x
3、如果p变动-x，且 空单数<最大空单，开空单。p=p-x
4、如果总盈利大于y，清仓。
5、止赢：记录每个订单的最大盈利值，如果盈利回撤25%以上，且盈利大于0.01，平掉该订单。
6、止损：如果订单盈利小于z,平掉该订单。
7、从第2步循环。
用订单价格对比，或订单时间延迟，来避免重复开单。

'''
#引入相关库
import numpy as np
import time
import pandas as pd
import talib
from HP_formula import *   #公式库
import MetaTrader5 as mt5
import HP_mt5 as hmt5
import HP_quant as hqu   #量化回测
import data_get as dg
from interval import Interval as itv

tp = 0.12
sl = -3.8
pf = 0.70
#symbol="GOLD_"
symbol="XAUUSD"
#symbol="EURUSD"
magic=0
p_up=2810.00  #上限不开多
p_down=790.00  #下限不开空

p_num=5   #开单数
p_step=0.2 #步长
lot=0.01  #开单量

date=0  #当前日期
LG = 67080706  # 账号
SERVER = "ForexTimeFXTM-Demo02"  # 服务器
PAS = "Zs123456"  # 密码


#初始化小白mt5库
hmt5.init()

hmt5.login(login=LG, server=SERVER,password=PAS)


#输出mt5连接相关信息
hmt5.info()

#计算夹板值
rates= mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 10)
data2=hmt5.tohpdata(rates)
data2['time']=[x[11:19] for x in data2.time.astype(str)]
#print(data2)

mydf=data2.copy()
mydf=mydf.reset_index(level=None, drop=True ,col_level=0, col_fill='')
CLOSE= mydf['close']
HIGH=mydf['high']
LOW=mydf.low
OPEN=mydf.open

# BOLL 布林带指标
def BOLL(N=26, P=2):
    """
    BOLL 布林带
    """
    MID = MA(CLOSE, N)
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P
    return UPPER, MID, LOWER



ask=hmt5.symbol_info_tick(symbol).ask
bid=hmt5.symbol_info_tick(symbol).bid

print('点差：' , ask-bid)
#=============================




#获取用户登陆信息
accountinfo=mt5.account_info()
print(accountinfo)
print('盈亏',accountinfo.profit)
print('净值',accountinfo.equity)
ask=hmt5.symbol_info_tick(symbol).ask
bid=hmt5.symbol_info_tick(symbol).bid

print('点差：' , ask-bid)

#hmt5.sell(symbol = "XAUUSD",volume=0.01)
hmt5.reload_positions2(symbol=symbol)


price=ask
price2=bid
ask3=ask
bid3=bid


dingdan={}  #订单列表

ma=0  #买多次数
mb=0  #买空次数
run=True
i=0
while run:
    peak = dg.Peak()
    result = peak.peak_process('m5', 100)
#    if i>2:
#        break
    print("第%d次工作"%i)
    #计算布林轨值
    rates= mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 100)
    data2=hmt5.tohpdata(rates)
    data2['S_time']=[x[11:19] for x in data2.time.astype(str)]
    data2['S_date']=[x[0:10] for x in data2.time.astype(str)]
    data2['STIME']=[x for x in data2.time.astype(str)]
    # 转为时间数组
    timeArray = time.strptime(data2['STIME'].iloc[-1], "%Y-%m-%d %H:%M:%S")
    # 转为时间戳
    timeStamp = int(time.mktime(timeArray))


    #获取用户登陆信息
    accountinfo=mt5.account_info()
    
    姓名=accountinfo.name
    服务器=accountinfo.server
    货币=accountinfo.currency
    用户名=accountinfo.login
    结余=accountinfo.balance
    总净值=accountinfo.equity
    总盈亏=accountinfo.profit
    预付款维持率=accountinfo.margin_level
    #print(accountinfo)
    
    print()
    # print('----------用户信息----------')
    # print('姓名:',姓名)
    # print('服务器:',服务器,'   用户名:',用户名)
    # print('总盈亏:',总盈亏,'  总净值:',总净值,'   结余:',结余)
    # print('总盈亏:',总盈亏,'   预付款维持率:',round(预付款维持率,2),"%")
    
    
    mydf=data2.copy()
    mydf=mydf.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    CLOSE= mydf['close']
    HIGH=mydf['high']
    LOW=mydf.low
    OPEN=mydf.open
    
    u,m,l=BOLL()
    mydf['u']=u
    mydf['m']=m
    mydf['l']=l
    
    len3=len(mydf)
    u2=list(u)[len3-1]
    m2=list(m)[len3-1]
    l2=list(l)[len3-1]   
    len2=len(mydf)

    df3=hmt5.reload_positions2(symbol=symbol)
    if 总盈亏>1.0:
        hmt5.qingcang()
        print('总盈亏盈利,全部清仓!')
        df3=hmt5.reload_positions2(symbol=symbol)



    print(df3)
    ask=hmt5.symbol_info_tick(symbol).ask
    bid=hmt5.symbol_info_tick(symbol).bid
    dc=ask-bid
    # print('ask : ',ask,'ask3',ask3,'price',price)
    # print('bid : ',bid,'bid3',bid3,'price2',price2)
    print('点差：' , round(dc,5))
    df3=hmt5.reload_positions2(symbol=symbol)
    positions_total=mt5.positions_total()
    if  positions_total>0:
        dd=hmt5.get_positions_df()
        if len(dd)>0:
            l2=len(dd)
            for j in range(l2):
                swap2=dd.at[j,'swap']
                tt2=dd.at[j,'ticket']
                pp2=dd.at[j,'profit']+swap2
                ty2=dd.at[j,'type']
                vv2=dd.at[j,'volume']
                cc2=dd.at[j,'comment']
                time2=dd.at[j,'time']-8*60*60
                time3=(timeStamp-time2)/60
                if tt2 in dingdan:
                    if dingdan[tt2]<pp2:
                        dingdan[tt2]=pp2
                    elif pp2/(dingdan[tt2]+0.000001)<pf :
                        if pp2>tp:
                            #print(pp2/dingdan[tt2],pp2,tt2)
                            hmt5.zhiying(profit=pp2-0.02,magic=magic)
                        else:
                            dingdan[tt2]=0
                    
                    if pp2<sl:
                        if ty2==0 :
                            hmt5.pingcang(tt2,magic=magic,comment2="ping "+cc2)
                            price=ask
                        elif ty2==1 :
                            hmt5.pingcang(tt2,magic=magic,comment2="ping "+cc2)
                            price2=bid


                else:
                    if pp2>0:
                        dingdan[tt2]=pp2
                    else:
                        dingdan[tt2]=0
                        
    positions_total=mt5.positions_total()

    p2=ask-price
    p3=price2-bid
    l2=0
    l3=0
    xx=5.00
    xx2=5.00    
    if  positions_total>0:
        hmt5.reload_positions2(symbol=symbol)
        dd=hmt5.get_positions_df()
        if len(dd)>0:
            dd2=dd[dd.type==0]
            dd3=dd[dd.type==1]
            l2=len(dd2)
            l3=len(dd3)
            xx=abs(dd2.price_open-ask).min()
            xx2=abs(dd3.price_open-bid).min()
            if l2==0:
                xx=5.00
            if l3==0:
                xx2=5.00
        else:
            xx=5.00
            xx2=5.00
 
    print('多单数',l2,'多步差',round(p2,5))
    print('空单数',l3,'空步差',round(p3,5))
    print('xx=',xx)
    print('xx2=',xx2)
    print('买多次数:',ma,'  买空次数:',mb)
    lot2=lot
    b_buy = True if dg.bid() in itv(min(result["low_list"]), max(result["low_list"])) else False
    s_sell = True if dg.bid() in itv(min(result["high_list"]), max(result["high_list"])) else False
    if p2>p_step and  l2<p_num and dc<0.9  and xx>0.1:
        #1.判断买单差价>0.5
        print('买',l2)
        hmt5.buy(symbol = symbol,volume=lot2,magic=magic)
        #hmt5.zhisun2(symbol = symbol,profit=10000,up=-0.30,type2=1,magic=magic)
        price=ask
        bid3=bid
        ma=ma+1
        #如果卖单数量最大,平仓亏损最大的卖单
        if l3==p_num:
            dingdanhao=list(dd3.ticket)[l3-1]
            hmt5.pingcang(dingdanhao,magic=magic)

    if p3>p_step  and l3<p_num and dc<0.9 and xx2>0.1:
        #判断卖单差价>0.5
        print('卖',l3)
        price2=bid
        hmt5.sell(symbol =symbol,volume=lot2,magic=magic)
        #hmt5.zhisun2(symbol = symbol,profit=10000,up=-0.30,type2=0,magic=magic)
        ask3=ask
        mb=mb+1
        #如果买单数量最大,平仓亏损最大的买单
        if l2==p_num:
            dingdanhao=list(dd2.ticket)[l3-1]
            hmt5.pingcang(dingdanhao,magic=magic)

    ask=hmt5.symbol_info_tick(symbol).ask
    bid=hmt5.symbol_info_tick(symbol).bid

    if ask<ask3:
        ask3=ask
        price=ask


    if bid>bid3:
        bid3=bid
        price2=bid

    time.sleep(1)
    
    i=i+1