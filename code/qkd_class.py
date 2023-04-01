import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator
from random import randint
import matplotlib.pyplot as plt

class qkd():
  def __init__(self,n,nmin,nmax,shots,shot_list) -> None:
    
    self.n = n
    self.nmin = nmin
    self.nmax = nmax
    self.shots = shots
    self.shot_list = shot_list
    
  def bit_error_rate(self,Alice_mex,Alice_key, Bob_mex_reciv, Bob_guessd_key):
    '''
    Description: Function that computes the bit error rate of the communication: the portion of wrongly deciphered message bits given the right bits of key.
    
    Inputs:
    Alice_mex (list) : Alice bits of message;
    Alice_key (list) : Alice key used to encrypt the message;
    Bob_mex_reciv (list) : Bob's message bits associated to the right bits of key;
    Bob_guessd_key (list) : Bob's right bits of key used to decipher the message.

    Returns:
    res (float) : ratio between how many bits of message Bob missed given the right bit of key used to decipher the ith bit of message.
    '''
    missed_bits = 0
    num_right_key = 0
    for i in range(len(Alice_key)):
      if Alice_key[i] == Bob_guessd_key[i]:
        num_right_key += 1
        if Alice_mex[i] != Bob_mex_reciv[i]:
          missed_bits =+ 1
    if num_right_key == 0:
        return 0
    res = missed_bits / num_right_key
    return res
  
  def ber_for_escaping(self,Alice_mex,Alice_key, Bob_mex_reciv, Bob_guessd_key):
    escaped = 0
    
    num_right_key = 0
    for i in range(len(Alice_key)):
        if Alice_key[i] == Bob_guessd_key[i]:
            num_right_key += 1
            if Alice_mex[i] == Bob_mex_reciv[i]:
                escaped += 1
    if num_right_key == 0:
        return 0
    else:
        return escaped / num_right_key 


  
  def checking(self, Bob_total_mex):
    '''
    Description:
    Checking function checks if the total message that Bob got corresponds to the starting message sent by Alice.
    
    Inputs:
    Bob_total_mex (list) : Bob's message got from the process.
    
    Returns:
    True if the total Bob mex differs from -1.
    '''
    for i in range(len(Bob_total_mex)):
      if Bob_total_mex[i] == -1:
        return False
    return True
  
  def counting(self, total_length):
    '''
    Description:
    Function that counts how many sendings Alice must perform in order to allow Bob to get as many right message bits as possible.
    This resumes the algorithm efficiency: BB84 protocol needs several repetitions in order to work,
    because the presence of the noise or the intrusion of an eavesdropper can corrupt the message. To overcome this issue, Alice needs to send the message
    many times. This function computes the number of time Alice should repeat and store the result in a way to be plotted later as a function of the message length.
    
    Inputs:
    total_length (int) : message's dimension.
    
    Returns:
    count (int) : number of time Alice should repeat the process.
    '''
    count = 0
    ber = 0
    Alice_mex = []
    for i in range(total_length):
        Alice_mex.append(randint(0,1))
   
    Bob_tot_mex = np.full(total_length,-1)
    while self.checking(Bob_tot_mex) == False:
        count += 1
        Alice_key = []
        for i in range(total_length):
            Alice_key.append(randint(0,1))
        circuit = QuantumCircuit(total_length,total_length)
        for i in range(total_length):
            if (Alice_key[i] == 1 and Alice_mex[i] == 1):
                circuit.x(i)
                circuit.h(i)
            elif (Alice_key[i] == 0 and Alice_mex[i] == 1):
                circuit.x(i)
            elif (Alice_key[i] == 1 and Alice_mex[i] == 0):
                circuit.h(i)
        Bob_key = []
        circuit.barrier()
        for i in range(total_length):
            Bob_key.append(randint(0,1))
            if Bob_key[i] == 1:
                circuit.h(i)    
        circuit.measure_all()
        simulator = AerSimulator()
        compiled_circuit = transpile(circuit, simulator)
        job = simulator.run(compiled_circuit, shots = 1)
        result = job.result() 
        measure = result.get_counts(compiled_circuit)
        Bob_mex_list = np.empty(total_length)
        for key in measure.keys():
            Bob_mex_temp = key
            for i in range(total_length):
                Bob_mex_list[i] = int(Bob_mex_temp[total_length-1-i])
        Bob_mex = []
        for i in range(0,len(Bob_mex_list)):
            Bob_mex.append(int(Bob_mex_list[i]))
        for i in range(0, len(Alice_key)):
            if Alice_key[i] == Bob_key[i]:
                Bob_tot_mex[i] = Bob_mex[i] 
        ber += self.bit_error_rate(Alice_mex, Alice_key, Bob_tot_mex, Bob_key)
    ber/=count
    return count
  
  def simul(self):
    '''
    Description:
    simul is a function that simulates the quantum key distribution process.
    
    Inputs:
    None.
    
    Returns:
    figure.
    '''
    avg_counting_per_n = np.zeros(self.n)
    
    std_per_n = np.empty(self.n)
    
    counting_temp = np.zeros(self.shots)
    
    length = np.linspace(self.nmin,self.nmax,self.n)
    for i in range(len(avg_counting_per_n)):
        for j in range(self.shots):
            counting_temp[j] = self.counting(3*i+self.nmin)
          
        avg_counting_per_n[i] = counting_temp.mean()
        
        std_per_n[i] = counting_temp.std() ##El 10%
        
    figure = plt.figure(figsize=(10,6))
    #plt.plot(length, avg_counting_per_n, linestyle='dashed', marker='s', color='blue',label='Mean bits available with 50 rep')
    
    plt.errorbar(length, avg_counting_per_n, linestyle='dashed', yerr=std_per_n, fmt='sb', markersize=9, capsize=3, ecolor='b', barsabove=True)
    
    #plt.fill_between(length, avg_counting_per_n-std_per_n, avg_counting_per_n+std_per_n, alpha=0.1, color='blue')
    
    plt.xlabel('Message length')
    plt.ylabel('Number of message sendings')
    plt.title('BB84 efficiency')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()
    return figure
  
  def simul_w_many_shots(self):
    '''
    Description: Function simul_w_many_shots computes the number of time Alice should send the message to Bob
    given the number of repetition (shots) as a function of the message's length.

    Inputs:
    n (int) : message dimension to fix and to use for the plot;
    nmin (int) : minimum value of the starting message to send;
    nmax (int) : maximal value of the ending message to send.
    shot_list (list) : list of three integers that represent the number of times Alice should send the message. Note that this value MUST BE AN INTEGER.

    Returns:
    figure (image) : functions plotted.
    '''

    #array_list = []
    count_list=[]
    std_list=[]
    if all(isinstance(element, int) for element in self.shot_list):
        pass
    else:
        raise ValueError('Elements inside the shot_list are not all integers, please make sure you inserted correct types inside the list.')
    for shot in self.shot_list:
       counting_temp = np.zeros(shot)
    
    avg_counting = np.zeros(self.n)
    std_counting=np.empty(self.n)
    length = np.linspace(self.nmin,self.nmax,self.n)
    figure = plt.figure(figsize=(20,6))
    for i in range(3):
        for j in range(len(avg_counting)):
            for shot in range(self.shot_list[i]):

                counting_temp[shot] = self.counting(3*j+self.nmin)
            avg_counting[j] = counting_temp.mean()
            std_counting[j] = counting_temp.std()
        count_list.append(avg_counting)
        std_list.append(std_counting)
        color_legend=['r','b','g']
        label_list=['Mean bits with 1 sends', 'Mean bits with 2 sends', 'Mean bits with 10 sends']
        plt.plot(length, count_list[i], linestyle='dashed', marker='s', color=color_legend[i], label=label_list[i])
        plt.errorbar(length, count_list[i], linestyle='dashed', yerr=std_list[i], markersize=9, capsize=3, ecolor=color_legend[i], barsabove=True)
        plt.legend(loc='best')
    plt.xlabel('Message length')
    plt.ylabel('Number of message sendings')
    plt.title('BB84 efficiency')
    plt.grid(True)
    
    plt.show()
    return figure
  


def eaves_spy(total_length):
    count = 0
    ber = 0
    Alice_mex = []
    for i in range(total_length):
        Alice_mex.append(randint(0,1))
   
    Bob_tot_mex = np.full(total_length,-1)
    checking = qkd(10,3,30,20,0)
    while checking.checking(Bob_tot_mex) == False:
        count += 1
        Alice_key = []
        for i in range(total_length):
            Alice_key.append(randint(0,1))
        circuit = QuantumCircuit(total_length,total_length)
        for i in range(total_length):
            if (Alice_key[i] == 1 and Alice_mex[i] == 1):
                circuit.x(i)
                circuit.h(i)
            elif (Alice_key[i] == 0 and Alice_mex[i] == 1):
                circuit.x(i)
            elif (Alice_key[i] == 1 and Alice_mex[i] == 0):
                circuit.h(i)
        Eve_key = []
        for i in range(0,total_length):
            Eve_key.append(randint(0,1))
            if Eve_key[i] == 1:
                circuit.h(i)    
        circuit.measure_all()
        for i in range(0,total_length):
            if Eve_key[i] == 1:
                circuit.h(i)  
        circuit.barrier()
        Bob_key = []
        circuit.barrier()
        for i in range(total_length):
            Bob_key.append(randint(0,1))
            if Bob_key[i] == 1:
                circuit.h(i)    
        circuit.measure_all()
        simulator = AerSimulator()
        compiled_circuit = transpile(circuit, simulator)
        job = simulator.run(compiled_circuit, shots = 1)
        result = job.result() 
        measure = result.get_counts(compiled_circuit)
        Bob_mex_list = np.empty(total_length)
        for key in measure.keys():
            Bob_mex_temp = key
            for i in range(total_length):
                Bob_mex_list[i] = int(Bob_mex_temp[total_length-1-i])
        Bob_mex = []
        for i in range(0,len(Bob_mex_list)):
            Bob_mex.append(int(Bob_mex_list[i]))
        for i in range(0, len(Alice_key)):
            if Alice_key[i] == Bob_key[i]:
                Bob_tot_mex[i] = Bob_mex[i] 
        
        ber += checking.bit_error_rate(Alice_mex, Alice_key, Bob_tot_mex, Bob_key)
    ber/=count
    return count
   
   



def how_many_shots_with_eve(n,nmin, nmax, shots):
    
    avg_counting_per_n = np.zeros(n)
    
    std_per_n = np.empty(n)
    
    counting_temp = np.zeros(shots)
    
    length = np.linspace(nmin,nmax,n)
    for i in range(len(avg_counting_per_n)):
        for j in range(shots):
            counting_temp[j] = eaves_spy(3*i+nmin)
          
        avg_counting_per_n[i] = counting_temp.mean()
        
        std_per_n[i] = counting_temp.std() ##El 10%
        
    figure = plt.figure(figsize=(10,6))
    #plt.plot(length, avg_counting_per_n, linestyle='dashed', marker='s', color='blue',label='Mean bits available with 50 rep')
    
    plt.errorbar(length, avg_counting_per_n, linestyle='dashed', yerr=std_per_n, fmt='sb', markersize=9, capsize=3, ecolor='b', barsabove=True)
    
    #plt.fill_between(length, avg_counting_per_n-std_per_n, avg_counting_per_n+std_per_n, alpha=0.1, color='blue')
    
    plt.xlabel('Message length')
    plt.ylabel('Number of message sendings')
    plt.title('BB84 efficiency')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()
    return figure

#vis = how_many_shots_with_eve(10,3,30,20)

