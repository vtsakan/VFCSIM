from random import seed
seed(1)

import numpy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import simpy


class Sender(object):
    def __init__(self, env, nextcable, sendrate):
        self.env = env
        self.sendrate = sendrate
        self.nextcable = nextcable
        env.process(self.start())

    def start(self):
        for i in range(1000):
            self.nextcable.put(self.env.now)
            yield self.env.timeout(self.sendrate)


class Receiver(object):
    def __init__(self, env, precable):
        self.env = env
        self.precable = precable
        env.process(self.start())

    def start(self):
        msg = yield self.precable.get()
        record.append(env.now / 1000)
        while True:
            yield self.precable.get() # なにもしない


class Cable(object):
    def __init__(self, env, delay):
        self.env = env
        self.delay = delay
        self.store = simpy.Store(env)

    def latency(self, value):
        yield self.env.timeout(self.delay)
        self.store.put(value)

    def put(self, value):
        self.env.process(self.latency(value))

    def get(self):
        return self.store.get()


class Node(object):
    def __init__(self, env, precable, nextcable, ethmpfsize, t_rcvtsk, t_sndtsk, t_switching, t_hello):
        self.env = env
        self.rtos = simpy.PriorityResource(env, capacity=1)
        self.rcvmbx = simpy.Store(env)
        self.numrcv = 0
        self.sndmbx = simpy.Store(env)
        self.numsnd = 0

        self.precable = precable
        self.nextcable = nextcable
        self.ethmpfsize = ethmpfsize
        self.t_rcvtsk = t_rcvtsk
        self.t_sndtsk = t_sndtsk
        self.t_switching = t_switching
        self.t_hello = t_hello

        self.rcv_ok = simpy.Container(env, init=0)
        self.snd_ok = simpy.Container(env, init=0)

        env.process(self.lanintr())
        env.process(self.ip_snd())

    def lanintr(self):
            msg = yield self.precable.get()
            env.process(self.ip_rcv())
            self.rcvmbx.put(msg)
            self.numrcv += 1
            while True:
                msg = yield self.precable.get()
                self.rcvmbx.put(msg)
                self.numrcv += 1

    def ip_rcv(self):
            if self.t_hello != 0:
                yield self.env.timeout(self.t_hello)
            while True:
                with self.rtos.request(priority=2) as req:
                    yield req
                    while self.numrcv != 0 and self.numsnd < self.ethmpfsize:
                        msg = yield self.rcvmbx.get()
                        yield self.env.timeout(self.t_rcvtsk)
                        self.sndmbx.put(msg)
                        self.numrcv -= 1
                        self.numsnd += 1
                    self.snd_ok.put(1)
                yield self.rcv_ok.get(1)

    def ip_snd(self):
            while True:
                yield self.snd_ok.get(1)
                with self.rtos.request(priority=2) as req:
                    yield req
                    yield self.env.timeout(self.t_switching)
                    while self.numsnd != 0:
                        msg = yield self.sndmbx.get()
                        yield self.env.timeout(self.t_sndtsk)
                        self.nextcable.put(msg)
                        self.numsnd -= 1
                    self.rcv_ok.put(1)


record = []
total = 17
load = 5

for num in range(total):
    simtime = num*300 + 1
    PKT_SIZE = 64 # byte
    SEND_RATE = (PKT_SIZE + 20) * 8 /load
    cables = []
    nodes = []
    hello = 0

    env = simpy.Environment()
    cables.append(Cable(env, 1)) # 1us
    sender = Sender(env, cables[0], SEND_RATE)
    for i in range(num):
        cables.append(Cable(env, 28)) # 28us
        hello = 0
        if i == 0:
            hello = 60
        nodes.append(Node(env, cables[i], cables[i+1], 54, 12.7, 7.13, 1.5, hello))
    receiver = Receiver(env, cables[num])

    env.run(until=simtime)

record5 = record
ax = plt.subplot(111)
ax.plot(df['load'], df['b5mbps'], 'r.-', label='actual result')
ax.plot(numpy.arange(1,total), record, 'g.-', label='simulation')
customize(ax, 16, 5, 'numNodes', 'totalDelay', 'maxDelay@5mbps')
