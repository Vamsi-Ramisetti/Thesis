import time
from threading import Thread,Event
import threading
from random import randint
from job import *

# Node represents a basic CPU node that run on a cloud server
class Node(Thread):
    def __init__(self,Job_que,speed,node_id,response_time_list):
        self.Job_que = Job_que
        self.id = node_id
        self.speed = speed #speed of the Node in Hz eg,10Hz = 10 jobs per second
        
        self.response_time_list = response_time_list# store the response time of the jobs executed
        self._stopevent = Event()
        Thread.__init__(self, name='Job_generator')

        #flag to mark the node as idle
        self.idle = False
    
    #execute the job extracted from the queue
    def execute_job(self):
        job = self.Job_que.get()
        job.execute(self.speed)
        self.response_time_list.append(job.end_time - job.start_time)# store the response time
        #print(f'Job {job.id} executed')
        
    #main run loop
    def run(self):
        #print(f'node {self.id} starts')
        while not self._stopevent.isSet():
            if self.Job_que.length >0:
                self.idle = False
                self.execute_job()
            else:
                self.idle = True
                #print(f"node {self.id} is idle")
        #print(f'node {self.id} closed')

    #stop the thread
    def join(self, timeout=None):
        #print(f'node {self.id} stops')
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)

'''
this class is used to encapsulate the mangement function of the nodes.
'''
CLOCK_SPEED = 5

class NodeManager(Thread):
    def __init__(self,job_que,monitor):
        self.node_list = list()
        self.id_counter = 0
        self.job_que = job_que
        self.monitor = monitor

        self._stopevent = Event()
        Thread.__init__(self, name='Job_generator')
    '''
    create a node and start it
    '''
    def add_node(self,n):
        time.sleep(1)
        for i in range(n):
            node = Node(self.job_que,CLOCK_SPEED,self.id_counter,self.monitor.response_time_list)
            node.start()
            self.id_counter += 1
            self.node_list.append(node)
    '''
    stop N node at once
    '''
    def stop_node(self,n):
        for i in range(n):
            if len(self.node_list)>0:
                node = self.node_list.pop(-1)
                node.join()
    '''
    check the load every 0.5 second. check the number of idle nodes, cpu power, pending tasks etc.
    '''
    def run(self):
        time.sleep(1)
        while not self._stopevent.isSet():
            current_time = datetime.datetime.now().timestamp()
            self.monitor.resources.append((len(self.node_list)*CLOCK_SPEED,current_time))
            idle_nodes = [n for n in self.node_list if n.idle ]
            self.monitor.idle_nodes.append((len(idle_nodes),current_time))
            self.monitor.pending_tasks.append((self.job_que.length,current_time))
            time.sleep(0.5)


    #stop the thread
    def join(self, timeout=None):
        #print(f'node {self.id} stops')
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)
    '''
    provision N nodes.
    if we have more than N nodes.stop some nodes
    if we have less than N nodes.start some nodes
    do change anything in case we have same number of nodes
    '''
    def provision(self,N):
        diff = N - len(self.node_list)
        if diff >0: 
            self.add_node(diff)
        elif diff<0:
            self.stop_node(abs(diff))
        else:
            pass

####################### driver/test ##########################
'''
q = JobQue()
t_gen = JobGenerator(q,0.1)

t_gen.start()
time.sleep(2)

nm = NodeManager(q)
nm.add_node(10)

time.sleep(5)
t_gen.join()
nm.stop_node()
'''