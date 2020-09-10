from matplotlib import pyplot as plt
import pickle
from statistics import mean

class Monitor:
    def __init__(self):
        self.response_time_list = list()
        self.new_job = list()
        self.resources = list()
        self.idle_nodes = list()
        self.pending_tasks = list()
    '''
    store the data for further computing.this is used for debugging purpose
    '''
    def store_data(self,dir):
        #save response time list
        file = open(f'./{dir}/response_time.pkl','wb')
        pickle.dump(self.response_time_list,file)
        file.close()
        #save new job list
        file = open(f'./{dir}/new_job.pkl','wb')
        pickle.dump(self.new_job,file)
        file.close()
        #save resources
        file = open(f'./{dir}/resources.pkl','wb')
        pickle.dump(self.resources,file)
        file.close()
        #save idle nodes
        file = open(f'./{dir}/idle.pkl','wb')
        pickle.dump(self.idle_nodes,file)
        file.close()
        #save pending nodes
        file = open(f'./{dir}/pending.pkl','wb')
        pickle.dump(self.pending_tasks,file)
        file.close()

    '''
    load the stored data.this is used for debugging purpose
    '''
    def load_data(self,dir):
        #load response time list
        file = open(f'./{dir}/response_time.pkl','rb')
        self.response_time_list = pickle.load(file)
        file.close()
        #load new job list
        file = open(f'./{dir}/new_job.pkl','rb')
        self.new_job = pickle.load(file)
        file.close()
        #load resources
        file = open(f'./{dir}/resources.pkl','rb')
        self.resources = pickle.load(file)
        file.close()
        #load idle nodes
        file = open(f'./{dir}/idle.pkl','rb')
        self.idle_nodes = pickle.load(file)
        file.close()
        #load pending nodes
        file = open(f'./{dir}/pending.pkl','rb')
        self.pending_tasks = pickle.load(file)
        file.close()

    '''
    plot the variation of response time of job
    the lesser the better.
    '''
    def plot_response_time(self):
        x = range(len(self.response_time_list))
        y = self.response_time_list
        plt.title('Response Time for job/tasks feeded into the system')
        plt.plot(x,y,label='response time')
        plt.ylabel('Response Time in Seconds')
        plt.xlabel('ID of the task')#we use simple counter to assign id
        plt.legend()
        plt.show()

        # average response time
        mean_response_time = mean(y)
        print(f'The mean response time: {mean_response_time}')

    '''
    the number of pending task on the system.lower is better
    '''
    def plot_pending_tasks(self):
        x1 = [i[1] for i in self.pending_tasks]
        y1 = [i[0] for i in self.pending_tasks]
        plt.title('Number of Pending tasks in the system ')
        plt.plot(x1,y1,label='Pending tasks')
        plt.ylabel('Number of Pending tasks')
        plt.xlabel('timestamps')#we use simple counter to assign id
        plt.legend()
        plt.show()

        # average response time
        avg_pending_task= mean(y1)
        print(f'Average number of pending tasks in the system: {avg_pending_task}')

    '''
    plot the variation of load with respect to task.
    '''
    def load_vs_resource(self):
        x1 = [i[1] for i in self.new_job]
        y1 = [i[0] for i in self.new_job]
        x2 = [i[1] for i in self.resources]
        y2 = [i[0] for i in self.resources]
        plt.title('Load vs Processing power allocated')
        plt.plot(x1,y1,label='Load coming in the system')
        plt.plot(x2,y2,label='Processing Power provisioned')
        plt.ylabel('Normalised Load')
        plt.xlabel('timestamps')
        plt.legend()
        plt.show()

        # average load
        mean_load = mean(y1)
        print(f'Mean load on the system {mean_load}')
        mean_processing_power = mean(y2)
        print(f'Mean processing power allocated {mean_processing_power}')

    '''
    plot the percentage of idle machines wrt time.
    '''
    def idle_machines(self):

        x1 = [i[1] for i in self.idle_nodes]
        idle_nodes = [i[0] for i in self.idle_nodes]
        total_nodes = [i[0]/5 for i in self.resources]#cpu power/clock speed give the number of nodes

        y1 = list()
        for i in range(len(total_nodes)):
            if total_nodes[i]==0:
                y1.append(0)
                continue
            y1.append(idle_nodes[i]/total_nodes[i]*100)

        plt.title('Percentage of idle Machine with respect to time')
        plt.plot(x1,y1,label='Percentage of idle Machines')

        plt.ylabel('% Percentage of idle Machines')
        plt.xlabel('timestamps')
        plt.legend()
        plt.show()

        # average number of idle machines
        mean_avg = mean(y1)
        print(f'Average percentage of idle machines is {mean_avg}')

    '''
    plot all the graphs
    '''
    def plot_all(self):
        self.plot_response_time()
        self.load_vs_resource()
        self.idle_machines()
        self.plot_pending_tasks()

'''
########################### test graphs ##########################
m = Monitor()
m.load_data('')
m.plot_all()

m.plot_response_time()
m.load_vs_resource()
m.idle_machines()
m.plot_pending_tasks()
'''

