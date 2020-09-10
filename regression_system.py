from job import *
from node import *
from controller import *
from monitor import *

q = JobQue()
m = Monitor()
#generate 0-21 job per second
t_gen = JobGenerator(q,1,m)
#create a Node Manager allocate the nodes
nm = NodeManager(q,m)

t_gen.start()
nm.provision(5)
nm.start()

#create a controller to control the scaling of resources
controller = LinearRegressionController(nm,q,t_gen)
controller.start()

time.sleep(180)

t_gen.join()
time.sleep(5)
nm.join()
controller.join()

m.store_data('regression')
m.plot_all()