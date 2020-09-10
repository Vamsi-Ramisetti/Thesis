import time
from threading import Thread,Event
import threading
from random import randint
import random
import math
import datetime
from monitor import *
import datetime
#Job  class is a class to simulate virtual load on a machine
class Job:
    def __init__(self,load_factor,id_num):
        self.load_factor = load_factor
        self.id = id_num
        #below attributes used to calculates the reqsponse time
        self.start_time = None
        self.end_time = None
    
    #this function simulates the delay in processing by sleep function
    def execute(self,clock_speed):
        #print(f'started processing Job->{self.id}')
        sleep_time = (self.load_factor / clock_speed) #the latency is proportional to the clock_speed
        time.sleep(sleep_time)
        self.end_time = datetime.datetime.now().timestamp()
        #print(f'finished processing Job->{self.id}')
        
# Job que is used as a cache/store the tasks temporily before processing
class JobQue:
    def __init__(self):
        self.Job_list = list()
        self.length = 0
        
    def add(self,Job):
        #print(f'Job->{Job.id} added to the que')
        Job.start_time = datetime.datetime.now().timestamp()
        self.Job_list.append(Job)
        self.length +=1
        
    def get(self):
        item = self.Job_list.pop(0)
        #print(f'Job->{item.id} removed from the que')
        self.length -=1
        return item
    '''
    clear removes all the items from the job que
    '''
    def clear(self):
        self.Job_list.clear()
        self.length = 0
        
###################### driver/test code #############################
'''
Job1 = Job(3, 1)
Job2 = Job(4, 2)

tq = JobQue()
tq.add(Job1)
tq.add(Job2)
print(tq.length)

tq.get()
print(tq.length)

tq.get()
print(tq.length)
'''

VARIANCE_SCALE = 0.1 # control the variation from sin wave
SCALE = 10
INCREMENT = math.pi/36 

# Job generator to randomly generate the Jobs at random time intervals
class JobGenerator(Thread):
    def __init__(self,Job_que,latency,monitor):
        self.Job_que = Job_que
        self.id_counter = 0
        self.monitor= monitor

        self.latency = latency #easily adjust the speed of Job generator
        self.angle_counter = random.random()
        
        self._stopevent = Event()
        Thread.__init__(self, name='Job_generator')

        #history of 8 entries of new tasks added
        self.history = list()
    
    #randomly generate Job to simulate virtual load
    def generate_Job(self):
        #number of jobs
        n = generate_N(self.angle_counter)
        self.history.append(n)
        self.angle_counter += INCREMENT
        self.monitor.new_job.append((n*5,datetime.datetime.now().timestamp()))
        #print(f'{n} jobs added to the que')
        for i in range(int(n)):
            #generate load and id for the Job
            load_factor = 5
            id = self.id_counter
            #add Job the Job to the que
            job = Job(load_factor,id)
            #print(f'Job {job.id} generated')
            self.id_counter+=1
            self.Job_que.add(job)

    #store the values of new jobs generated
    def update_history(self,n):
        self.history.append(n)

    #returns the list of last n entries
    def get_history(self,n):
        return self.history[-n:]
        

    #main function which contains the code
    def run(self):
        print('generator starts')
        while not self._stopevent.isSet():
            self.generate_Job()
            self._stopevent.wait(self.latency)
        print('generator closing')

    #stop the thread
    def join(self, timeout=None):
        #print('generator stops')
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)

def generate_N(angle):
    N = int((math.sin(angle) + random.random()*VARIANCE_SCALE)*SCALE)
    return abs(N)

###################### driver/test code ################################
'''
tq = JobQue()
m = Monitor()
t_gen = JobGenerator(tq,0.01,m)

t_gen.start()
time.sleep(60)

#the code used for periodic synthetic data generation
import pickle
file = open('history.pkl','wb')#save the history in the pickle file
pickle.dump(t_gen.history,file)
file.close()

t_gen.join()
'''
