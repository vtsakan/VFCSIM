from threading import Thread
import time
import queue;
from sender import sender;
from processor import processor;

class VF(Thread):
    def __init__(self, name, QIN, QOUT, outload, mips, bandwidth):
       # Call the Thread class's init function
       Thread.__init__(self)
       self.name = name;
       self.IN = QIN;
       self.OUT = QOUT;
       self.myprocessor = 0;
       self.outload = outload;
       self.undertakeCPU = 0;
       self.mips = mips;
       self.bandwidth = bandwidth;
       self.mysender = sender(self.name, QIN, QOUT, self.bandwidth)
   # Override the run() function of Thread class

    def run(self):
       print('Started loading contents from VF : ', self.name)

       self.mysender.start();

       while(True):
           #time.sleep(0.1)
           if (not self.IN[self.name].empty()):
               #print(self.name, ' received data');
               data = self.IN[self.name].get();
               #self.myprocessor = processor(self.name, self.undertakeCPU, data, self.OUT);
               #self.myprocessor.start();
               #self.myprocessor.join();

               #processing
               time.sleep(self.mips/self.undertakeCPU);
               #forward for sending to the next VF
               self.OUT[self.name].put(self.outload);
               #process
               #self.OUT[self.name].put('I outputing data');
       print('Finished: ', self.name)
       self.mysender.join();

    def setUndertakeCPU(self, c):
        self.undertakeCPU = c;
