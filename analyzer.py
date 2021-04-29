import socket
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.console
import numpy as np
from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import threading
from collections import deque
import sys
import pickle
from collections import deque
import plotly.graph_objs as go
import random
import numpy as np
import requests
import time



# Listen for incoming datagrams
'''
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)
    # Sending a reply to client

    #UDPServerSocket.sendto(bytesToSend, address)
'''

app = QtGui.QApplication([])
win = QtGui.QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1000,500)
win.setWindowTitle('pyqtgraph example: dockarea')


max_length = 100
mesHead = list();

processedframes = deque(maxlen=max_length);
myQIN = deque(maxlen=max_length);
QVF1 = deque(maxlen=max_length);
QVF3 = deque(maxlen=max_length);
IMUHead_ids = deque(maxlen=max_length)
IMUBack_ids = deque(maxlen=max_length)


times = deque(maxlen=max_length)
hrAx = deque(maxlen=max_length)
hrAy = deque(maxlen=max_length)
hrAz = deque(maxlen=max_length)
hrWx = deque(maxlen=max_length)
hrWy = deque(maxlen=max_length)
hrWz = deque(maxlen=max_length)

brAx = deque(maxlen=max_length)
brAy = deque(maxlen=max_length)
brAz = deque(maxlen=max_length)
brWx = deque(maxlen=max_length)
brWy = deque(maxlen=max_length)
brWz = deque(maxlen=max_length)


def UPDATEALL():
	updateBack();
	updateHead();
	updateFloor();

def readSOCKETQOS():
    global processedframes, myQIN, QVF1;

    localIP     = "127.0.0.1"
    localPort   = 20005
    bufferSize  = 1024
    #msgFromServer       = "Hello UDP Client"
    #bytesToSend         = str.encode(msgFromServer)
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")

    t0 = time.time();
    try:
        while (True):
            resdata = UDPServerSocket.recvfrom(bufferSize);
            print(resdata)
            data = pickle.loads(resdata[0]);
            if (isinstance(data, (float))):
                t1 = data;
                processedframes.append(1/(t1-t0));
                t0 = data;
            else:
                myQIN = data;
                print(data)
                for qin in myQIN:
                    n, s = qin;
                    if ('VF1' in n):
                        QVF1.append(s);
                    if ('VF3' in n):
                        QVF3.append(s);
    except (KeyboardInterrupt, SystemExit):
        raise;

def getProcessedFrames():
    global processedframes;
    try:


        ts = time.time();
		#ident = round(10000*ts);
		#URL = "http://localhost:1026/v2/entities?type=IMU_Head&attrs=Ax,Ay,Az,Wx,Wy,Wz&options=keyValues&q=timestamp>"+str(ident - 5000);
		#print(URL)
		#r = requests.get(url = URL)
		#data = r.json()
        data = message;
        processedframes.append(1)
    except Exception as e:
        print("ERROR2" + str(e))
		#break;


def readDBHead():
	global hrAx;
	global IMUHead_ids;
	try:
		ts = time.time();
		ident = round(10000*ts);
		URL = "http://localhost:1026/v2/entities?type=IMU_Head&attrs=Ax,Ay,Az,Wx,Wy,Wz&options=keyValues&q=timestamp>"+str(ident - 5000);
		#print(URL)
		r = requests.get(url = URL)
		data = r.json()
		for d in data:
			if d['id'] not in IMUHead_ids:
				IMUHead_ids.append(d['id']);
				#print(d['id'])
				hrAx.append(float(d['Ax']))
				hrAy.append(float(d['Ay']))
				hrAz.append(float(d['Az']))
				hrWx.append(float(d['Wx']))
				hrWy.append(float(d['Wy']))
				hrWz.append(float(d['Wz']))
				d = requests.delete("http://localhost:1026/v2/entities/" + str(d['id']))
	except Exception as e:
		print("ERROR2" + str(e))
		#break;




## Create docks, place them into the window one at a time.
## Note that size arguments are only a suggestion; docks will still have to
## fill the entire dock area and obey the limits of their internal widgets.
#d1 = Dock("Head IMU - Gyroscopes", size=(1, 1))     ## give this dock the minimum possible size
#d2 = Dock("Dock2 - Console", size=(500,300), closable=True)
#d3 = Dock("Dock3", size=(500,400))
#d4 = Dock("Dock4 (tabbed) - Plot", size=(500,200))

d1 = Dock("Head IMU - Gyroscopes", size=(500,200))     ## give this dock the minimum possible size
d2 = Dock("Head IMU - Accelerotemetres", size=(500,200))     ## give this dock the minimum possible size
d3 = Dock("Back IMU - Gyroscopes", size=(500,200))     ## give this dock the minimum possible size
d4 = Dock("Back IMU - Accelerometres", size=(500,200))     ## give this dock the minimum possible size



d5 = Dock("Pressure Mat", size=(500,200))
d6 = Dock("Skeleton Data", size=(500,200))

area.addDock(d1, 'left')

area.addDock(d2, 'left')
'''
area.addDock(d3, 'right')
area.addDock(d4, 'right')

area.addDock(d5, 'bottom')
area.addDock(d6, 'bottom')

area.addDock(d2, 'top', d1)
area.moveDock(d2, 'above', d1)
area.addDock(d4, 'top', d3)
area.moveDock(d4, 'above', d3)
'''
#area.addDock(d3, 'bottom', d1)## place d3 at bottom edge of d1
#area.addDock(d4, 'right')     ## place d4 at right edge of dock area
#area.addDock(d5, 'left', d1)  ## place d5 at left edge of d1
#area.addDock(d6, 'top', d4)   ## place d6 at top edge of d4

## Test ability to move docks programatically after they have been placed
#area.moveDock(d4, 'top', d2)     ## move d4 to top edge of d2
#area.moveDock(d6, 'above', d4)   ## move d6 to stack on top of d4
#area.moveDock(d5, 'top', d2)     ## move d5 to top edge of d2


## Add widgets into each dock

## first dock gets save/restore buttons
'''
w1 = pg.LayoutWidget()
label = QtGui.QLabel(""" -- DockArea Example --
This window has 6 Dock widgets in it. Each dock can be dragged
by its title bar to occupy a different space within the window
but note that one dock has its title bar hidden). Additionally,
the borders between docks may be dragged to resize. Docks that are dragged on top
of one another are stacked in a tabbed layout. Double-click a dock title
bar to place it in its own window.
""")
saveBtn = QtGui.QPushButton('Save dock state')
restoreBtn = QtGui.QPushButton('Restore dock state')
restoreBtn.setEnabled(False)
w1.addWidget(label, row=0, col=0)
w1.addWidget(saveBtn, row=1, col=0)
w1.addWidget(restoreBtn, row=2, col=0)
d1.addWidget(w1)
state = None
def save():
    global state
    state = area.saveState()
    restoreBtn.setEnabled(True)
def load():
    global state
    area.restoreState(state)
saveBtn.clicked.connect(save)
restoreBtn.clicked.connect(load)
'''
w1 = pg.PlotWidget(title="Processed frames")
curve11 = w1.plot(pen='r');
d1.addWidget(w1)
def updateHead():
    global processedframes;
    curve11.setData(processedframes)
    #curve12.setData(hrWy)
    #curve13.setData(hrWz)
timer1 = QtCore.QTimer()
timer1.timeout.connect(updateHead)
timer1.start(50)

w2 = pg.PlotWidget(title="IN QUEUES")
w2.addLegend();
curve21 = w2.plot(pen='g', name="VF1");
curve23 = w2.plot(pen='b', name="VF3");
d2.addWidget(w2)
def updatemyQ():
    global QVF1, QVF3;
    curve21.setData(QVF1)
    curve23.setData(QVF3)
    #curve12.setData(hrWy)
    #curve13.setData(hrWz)
timer2 = QtCore.QTimer()
timer2.timeout.connect(updatemyQ)
timer2.start(50)

'''
w2 = pg.PlotWidget(title="Head IMU Accelerometers")
curve21 = w2.plot(pen='r')
curve22 = w2.plot(pen='g')
curve23 = w2.plot(pen='b')
d2.addWidget(w2)
def updateHead():
    global curve21, curve22,curve23,data, ptr, p6, hrAx,hrAy, hrAz
    readDBHead();
    curve21.setData(hrAx)
    curve22.setData(hrAy)
    curve23.setData(hrAz)
timer2 = QtCore.QTimer()
timer2.timeout.connect(updateHead)
timer2.start(50)

w3 = pg.PlotWidget(title="Back IMU - Gyroscopes")
curve31 = w3.plot(pen='r')
curve32 = w3.plot(pen='g')
curve33 = w3.plot(pen='b')
d3.addWidget(w3)
def updateHead():
    global curve31, curve32,curve33,data, ptr, p6, hrWx,hrWy, hrWz
    readDBBack();
    curve31.setData(brWx)
    curve32.setData(brWy)
    curve33.setData(brWz)
timer3 = QtCore.QTimer()
timer3.timeout.connect(updateHead)
timer3.start(50)

w4 = pg.PlotWidget(title="Back IMU - Accelerometers")
curve41 = w4.plot(pen='r')
curve42 = w4.plot(pen='g')
curve43 = w4.plot(pen='b')
d4.addWidget(w4)
def updateHead():
    global curve41, curve42,curve43,data, ptr, p6, hrWx,hrWy, hrWz
    readDBBack();
    curve41.setData(brAx)
    curve42.setData(brAy)
    curve43.setData(brAz)
timer4 = QtCore.QTimer()
timer4.timeout.connect(updateHead)
timer4.start(50)





'''
w2 = pg.console.ConsoleWidget()
d2.addWidget(w2)

## Hide title bar on dock 3
d3.hideTitleBar()
#w3 = pg.PlotWidget(title="Plot inside dock with no title bar")
#w3.plot(np.random.normal(size=100))
w3 = pg.GraphicsWindow()
w3.setWindowTitle('pyqtgraph example: GraphItem')
v = w3.addViewBox()
v.setAspectLocked()

g = pg.GraphItem()
v.addItem(g)



d3.addWidget(w3)
## Define positions of nodes
pos = np.array([
    [0,0],
    [10,0],
    [0,10],
    [10,10],
    [5,5],
    [15,5]
    ])

## Define the set of connections in the graph
adj = np.array([
    [0,1],
    [1,3],
    [3,2],
    [2,0],
    [1,5],
    [3,5],
    ])

## Define the symbol to use for each node (this is optional)
symbols = ['o','o','o','o','t','+']

## Define the line style for each connection (this is optional)
lines = np.array([
    (255,0,0,255,1),
    (255,0,255,255,2),
    (255,0,255,255,3),
    (255,255,0,255,2),
    (255,0,0,255,1),
    (255,255,255,255,4),
    ], dtype=[('red',np.ubyte),('green',np.ubyte),('blue',np.ubyte),('alpha',np.ubyte),('width',float)])

## Update the graph
g.setData(pos=pos, adj=adj, pen=lines, size=1, symbol=symbols, pxMode=False)






'''
w4 = pg.PlotWidget(title="Back IMU")
curve1 = w4.plot(pen='r')
curve2 = w4.plot(pen='g')
curve3 = w4.plot(pen='b')
d4.addWidget(w4)
def updateBack():
    global curve1, curve2,curve3,data, ptr, p6, brWx, brWy, brWz
    readDBBack();
    curve1.setData(brWx)
    curve2.setData(brWy)
    curve3.setData(brWz)
timer2 = QtCore.QTimer()
timer2.timeout.connect(updateBack)
timer2.start(50)
'''

#    if ptr == 0:
#        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
#    ptr += 1
#timer = QtCore.QTimer()
#timer.timeout.connect(updateBack)
#timer.start(50)

'''
w5 = pg.ImageView()
w5.setImage(np.random.normal(size=(100,100)))
d5.addWidget(w5)
def updateFloor():
    global ci
    w5.setImage(np.random.normal(size=(100,100)))
#    if ptr == 0:
#        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
#    ptr += 1
timer5 = QtCore.QTimer()
timer5.timeout.connect(updateFloor)
timer5.start(50)




w6 = pg.GraphicsWindow()
w5.setWindowTitle('Skeleton Data')
v = w6.addViewBox()
v.setAspectLocked()

g = pg.GraphItem()
v.addItem(g)



d6.addWidget(w6)
## Define positions of nodes
pos = np.array([
    [0,0],
    [10,0],
    [0,10],
    [10,10],
    [5,5],
    [15,5]
    ])

## Define the set of connections in the graph
adj = np.array([
    [0,1],
    [1,3],
    [3,2],
    [2,0],
    [1,5],
    [3,5],
    ])

## Define the symbol to use for each node (this is optional)
symbols = ['o','o','o','o','t','+']

## Define the line style for each connection (this is optional)
lines = np.array([
    (255,0,0,255,1),
    (255,0,255,255,2),
    (255,0,255,255,3),
    (255,255,0,255,2),
    (255,0,0,255,1),
    (255,255,255,255,4),
    ], dtype=[('red',np.ubyte),('green',np.ubyte),('blue',np.ubyte),('alpha',np.ubyte),('width',float)])

## Update the graph
g.setData(pos=pos, adj=adj, pen=lines, size=1, symbol=symbols, pxMode=False)
'''



#w6 = pg.PlotWidget(title="Dock 6 plot")
#w6.plot(np.random.normal(size=100))
#d6.addWidget(w6)


win.show()







## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    STQOS = threading.Thread(target=readSOCKETQOS)
    STQOS.start();


    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
