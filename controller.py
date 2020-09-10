'''
these classes are responsible for provisioning the resources in the machine.
'''
import threading
from threading import Thread
import time
from node import *
from job import *
from statistics import mean
from monitor import *

CONTROLLER_INTERVAL=2

class ThresholdController(Thread):
    def __init__(self,node_manager,job_que,job_gen):
        self.nm = node_manager
        self.job_que = job_que 
        self.job_gen = job_gen

        self._stopevent = threading.Event()
        threading.Thread.__init__(self, name='processing instance')

    def run(self):
        while not self._stopevent.isSet():
            #check the number of jobs in the queue
            n = (self.nm.job_que.length)
            print(f'number of task in the que {n}')
            print(f'number of active nodes {len(self.nm.node_list)}')
            #capacity to provision
            if n > 10:
                #add 2 nodes to the system
                nodes = len(self.nm.node_list)
                self.nm.provision(nodes + 2)
            if n < 2:
                #remove 2 nodes to the system
                nodes = len(self.nm.node_list)
                self.nm.provision(nodes - 2)
            #provision the resources
            self._stopevent.wait(1)

    def join(self, timeout=None):
        self._stopevent.set()
        self.nm.provision(0)#stop all nodes
        threading.Thread.join(self, timeout)

import numpy as np
from sklearn.linear_model import LinearRegression


class LinearRegressionController(ThresholdController):
    def run(self):
        time.sleep(2)#offset from task generator
        while not self._stopevent.isSet():
            history = self.job_gen.get_history(4)
            x = np.array(range(len(history))).reshape((-1, 1))
            y = np.array(history)
            model = LinearRegression()
            model.fit(x, y)
            #predict the value of next load
            m = abs(model.predict(np.array([len(history)]).reshape((-1, 1))))
            #check the number of jobs in the queue
            n = (self.nm.job_que.length)
            #capacity to provision
            N = int((m + n/4))
            print(f'number of task in the que {n}')
            print(f'number of active nodes {len(self.nm.node_list)}')
            self.nm.provision(N)
            #provision the resources
            self._stopevent.wait(1)




