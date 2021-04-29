from threading import Thread
import time
from VF import VF;
import queue;
from device import device;
import socket;
import pickle;

def createVF(name, outload, mips, bandwidth):
    QIN[name] = queue.Queue();
    QOUT[name] = queue.Queue();
    return VF(name, QIN, QOUT, outload, mips, bandwidth);

def getQsizes(Q):
    myq = [];
    for vf in Q.keys():
        tq = Q[vf];
        temp = [vf, tq.qsize()];
        myq.append(temp);

    return myq;

if __name__ == '__main__':

    serverAddressPort   = ("127.0.0.1", 20005)
    bufferSize          = 1024
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    QIN = {};
    QOUT = {};

    D1 = device('device01', 10000, 1000, QIN, QOUT);
    D2 = device('device02', 10000, 1000, QIN, QOUT);
    D3 = device('device03', 10000, 1000, QIN, QOUT);
    D4 = device('device04', 10000, 1000, QIN, QOUT);
    D5 = device('device05', 10000, 1000, QIN, QOUT);
    D6 = device('device06', 10000, 1000, QIN, QOUT);
    D7 = device('device07', 10000, 1000, QIN, QOUT);

    VF1   = createVF('VF1',   outload = 100,  mips = 1000, bandwidth = 1000000);
    VF2R1 = createVF('VF2R1', outload = 1000, mips = 1000, bandwidth = 1000000);
    VF3   = createVF('VF3',   outload = 100,  mips = 1000, bandwidth = 1000000);
    VF2R2 = createVF('VF2R2', outload = 1000, mips = 1000, bandwidth = 1000000);
    VF2R3 = createVF('VF2R3', outload = 1000, mips = 1000, bandwidth = 1000000);
    VF2R4 = createVF('VF2R4', outload = 1000, mips = 1000, bandwidth = 1000000);
    VF2R5 = createVF('VF2R5', outload = 1000, mips = 1000, bandwidth = 1000000);
    #VF2R5 = createVF('VF2R5', 5000);

    time.sleep(3);
    D1.addVF(VF1);
    D2.addVF(VF2R1);
    D3.addVF(VF3);
    D4.addVF(VF2R2);
    D5.addVF(VF2R3);
    D6.addVF(VF2R4);
    D7.addVF(VF2R5);

    time.sleep(5);

    D1.start();
    D2.start();
    D3.start();
    D4.start();
    D5.start();
    D6.start();
    D7.start();
    while(True):
        QIN['VF1'].put(500);
        time.sleep(1/16);

        msg       = getQsizes(QIN);
        print('msg = ', msg)
        outdata = pickle.dumps(msg);
        UDPClientSocket.sendto(outdata, serverAddressPort);

    time.sleep(15);
    D1.join()
    D2.join()
    D3.join()
    D4.join()
    D5.join()
    D6.join()
