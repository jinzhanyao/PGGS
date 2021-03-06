import networkx as nx 
import numpy as np
import random
import matplotlib.pyplot as plt
from pgg_ import createGroup, playPGG, update_strategy
from lattice import set_population, square_lattice
from plot_graph import plot_lattice
import time, os
import pickle
import csv

os.system('clear')
LENGTH = 100
TOT_POP = int(LENGTH**2)
C_POP = int(TOT_POP*3333/10000)
D_POP = int(TOT_POP*3333/10000)
PC_POP = TOT_POP - C_POP - D_POP
PD_POP = 0
POP = [C_POP,D_POP,PC_POP,PD_POP]
GEN = 10000000
RUNS = 1
VISUALIZE = True
a = 1
r = 3
K = 0.1
c= 0.2
fine = 0.3
avg_deg = 4.
req_gen = np.array([10,40,150,1000])*TOT_POP

G= square_lattice(LENGTH)
set_population(G,POP)
NODES = [n for n in G.nodes()]
NEIGHBORS = []
for i in range(len(NODES)):
    NEIGHBORS.append([n for n in G.neighbors(i)])
GROUPS = [createGroup(G,node) for node in NODES]



G1 = G.copy()
coop_no, punish_no = [], []
for n in NODES:
    group = GROUPS[n]
    coop_no.append(len([i for i in group if G1.nodes[i]['nature']]))
    punish_no.append(len([i for i in group if G1.nodes[i]['punish']]))
playPGG(G1,a,c,fine,r,GROUPS,coop_no, punish_no,[])
FILTERED_NODES = NODES.copy()
for n in NODES:
    if len(NEIGHBORS[n])==0:
        FILTERED_NODES.remove(n)

pop_ = POP.copy()
cpop_,ppop_, dpop_ = [C_POP/TOT_POP],[PC_POP/TOT_POP],[D_POP/TOT_POP]
if VISUALIZE:
    ax1 = plt.figure().add_subplot(111)
    ax1.set(aspect='equal')
start_time = time.time()
bar_len = 30
gen_list = [1]

for gen in range(GEN):
    pop_, node_, change, id_list = update_strategy(G1,K,pop=pop_,nodes = FILTERED_NODES,neighbors=NEIGHBORS)
    coop_no, punish_no = playPGG(G1,a,c,fine,r,GROUPS,coop_no, punish_no,id_list, change,node=node_)

    bar = '\u2588'*((gen+1)*bar_len//GEN)+'\u2591'*(bar_len-(gen+1)*bar_len//GEN)
    end_time = time.time()
    print("Generation {}/{} {} {:.1%} Runtime : {:.1f} secs".format((gen+1)//TOT_POP, GEN//TOT_POP, bar, (gen+1)/GEN,end_time-start_time),end='\r')
    if (gen+1)%1000==1:
        plot_lattice(G1,ax1)
        plt.savefig(f'./Figures/Figure_{(gen+1)}.tiff')

print(" "*100,end='\r')
print("Runtime :", end_time-start_time, 'secs')
#pickle.dump(np.array([gen_list,cpop_,dpop_,ppop_]),open('./data.pickle','wb'))
ax = plt.figure().add_subplot(1,1,1)
ax.set_xscale('log')
gen_list = np.array(gen_list)
ax.plot(gen_list/TOT_POP,cpop_,label='Cooperators',color='blue')
ax.plot(gen_list/TOT_POP,dpop_,label='Defectors',color='red')
ax.plot(gen_list/TOT_POP,ppop_,label='Punishers (C)',color='green')
ax.set_xlabel('iterations')
ax.set_ylabel('fractions')
#plt.title(f"c = {c}  fine = {fine}")
plt.legend(loc='best')
plt.savefig('./Figures/sql_evolution.png')
'''
file = open('data2.txt','a')
for i in range(len(cpop_)):
    file.write(str(cpop_[i])+"\t"+str(dpop_[i])+"\t"+str(ppop_[i])+"\n")
file.close()
'''