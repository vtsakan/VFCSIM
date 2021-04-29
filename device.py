from threading import Thread
import time
import queue;

class device(Thread):
    def __init__(self, name, cpu, bandwidth, QIN, QOUT):
       # Call the Thread class's init function
       Thread.__init__(self)
       self.name = name;
       self.VFs = queue.Queue();
       self.cpu = cpu;
       self.IN = QIN;
       self.OUT = QOUT;
       self.bandwidth = bandwidth;

    def run(self):
       while True:
           if (not self.VFs.empty()):
               print('new VF');
               v = self.VFs.get();
               v.start();
       #time.sleep(self.data/self.speed);
       #self.OUT[self.name].put(self.data);

    def addVF(self, newVF):
        newVF.setUndertakeCPU(self.cpu);
        self.VFs.put(newVF);
        print('VF added')

    def removeVF(self, oldVF):
        self.VFs.remove(oldVF);

    def getCPU(self):
        return self.cpu;
