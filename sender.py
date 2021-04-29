from threading import Thread
import time;
import queue;
import random;
import csv;
import socket;
import pickle;

class sender(Thread):
    def __init__(self, name, QIN, QOUT, bandwidth):
       # Call the Thread class's init function
       Thread.__init__(self)
       self.name = name;
       self.IN = QIN;
       self.OUT = QOUT;
       self.bandwidth = bandwidth;


       self.serverAddressPort   = ("127.0.0.1", 20005)
       self.bufferSize          = 1024
       self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

       #msgFromServer = UDPClientSocket.recvfrom(bufferSize)
       #msg = "Message from Server {}".format(msgFromServer[0])
       print('Message sent')

    def run(self):
        qos_file = open(self.name + 'QoS.csv', mode='w');
        fieldnames = ['time'];
        qos_writer = csv.DictWriter(qos_file, fieldnames=fieldnames);
        qos_writer.writeheader()


        while(True):
           if (not self.OUT[self.name].empty()):
               #print(self.name, ' has data')
               d = self.OUT[self.name].get();
               id = int(self.name[2]);
               #print('id = ', id);
               #print(self.OUT.keys())
               hop = 'VF'+str(id+1);

               p = [];
               for h in self.OUT.keys():
                   p.append(h[0:3]);
                   #print(p)

               if (hop not in p):
                   print('I am ', self.name, ' and I am the consume service');
                   print('Frame processed at ', time.time());
                   msgFromClient       = time.time();
                   outdata = pickle.dumps(msgFromClient);
                   #bytesToSend         = str.encode(msgFromClient)
                   self.UDPClientSocket.sendto(outdata, self.serverAddressPort)
                   qos_writer.writerow({'time': time.time()})
               else:
                   res = [];
                   for serv in self.OUT.keys():
                       if hop in serv:
                           res.append(serv);
                   r = random.choice(res);
                   print(r);
                   #simulate network time
                   time.sleep(d/self.bandwidth);
                   self.IN[r].put(d);
