from subprocess import Popen
import os
from mbc_py_interface import mbcNodal
import precice
import numpy as np

case = 'membrane'

input_file_name = case + '.mbd'
log_file = open('run_' + case + '.log', 'w')
process = Popen(['mbdyn', '-f', input_file_name],
                     stdout=log_file,
                     stderr=log_file)
process.stdin = ''
path = '{name}.sock'.format(name=case)
host = ''
port = 0
timeout = -1
verbose = 1
data_and_next = 1
refnode = 0
nodes = 576
labels = 0 # 16
rot = 0
accels = 0
nodal = mbcNodal(path, host, port, timeout, verbose,
                      data_and_next, refnode, nodes, labels,
                      rot, accels)
nodal.negotiate()
print(nodal.recv())
initialized = True


#10 Iteration
for i in range(10):

	#576 x 3 force tensor
	force_tensor = np.random.uniform(low=0.4*10**-3,high=0.7*10**-6,size=(576,3))
	
	###set_forces
	nodal.n_f[:] = np.ravel(force_tensor)
	###
    
	###solve(False)
	converged = False
	if nodal.send(converged):
		print('Something went wrong!')
		break
	if nodal.recv():
		print('Something went wrong!')
		break
	###
	
	print("\nCalculated displacement:")
	print(nodal.n_x)
	print("\n")
	
	###solve(True) -> Next step
	converged = True
	if nodal.send(converged):
		print('Something went wrong!')
		break
	if nodal.recv():
		print('Something went wrong!')
		break
	###

print("\nEND")
nodal.destroy()

    
    
    
        
