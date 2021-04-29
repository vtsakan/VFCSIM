from threading import Thread
import time
import queue;

class processor(Thread):
   def __init__(self, name, speed, data, QOUT):
       # Call the Thread class's init function
       Thread.__init__(self)
       self.name = name;
       self.speed = speed;
       self.data = data;
       self.OUT = QOUT;

   def run(self):
       #print('PROCESSING', self.name, '=', self.speed)
       time.sleep(self.data/self.speed);
       self.OUT[self.name].put(self.data);
