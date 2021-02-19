# -*-coding:utf-8 -*-
# import zmq
# import time
#
#
# context = zmq.Context()
#
# socket = context.socket(zmq.REQ)
#
# b = socket.connect("tcp://localhost:5552")
#
#
# while True:
#     a = socket.send_string("")
#     response = socket.recv_unicode()
#     print(a, response)
#     time.sleep(2)


def a(func):
    print("a")
    def aa(da, *args, **kwargs):
        print("aa后执行")
        da *= 10
        func(da)
        print('aa--da: ', da)

    return aa



def b(func):
    print('b')
    def bb(da, *args, **kwargs):
        print("bb先执行")
        da += 1
        func(da)
        print('bb--da', da)
    return bb


def c(func):
    print('c')
    def cc(da, *args, **kwargs):
        print("cc先执行")
        da += 1
        func(da)  # bb.func -->aa.func
        print('cc--da', da)
    return cc


@c  # c(bb)
@b  # b(aa)
@a  # a(test)
def test(da):

    print('test:', da)
    return 2


a = test(1)
































