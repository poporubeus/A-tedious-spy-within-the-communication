# A tedious spy within the quantum communication
QKD algorithm written in Python aims to show the effect of a spy inside the quantum communcation between two parties. 

# Description
BB84 protocol is an algorithm invented for the first time by Charles Bennett and Gilles Brassard who asked themselves if quantum cryptography could have been better than its already known classical counterpart.
![Img](Images/Dr._Charles_Bennett_IBM_Fellow.jpg)

Theoretically the answer is "Yes" because, thanks to Quantum Mechanics and its principles, every time an eavesdropper had access to the "quantum message" transmitted by the parties, he would have been detected by his necessity of making a measurement on the target qubit.
In fact, accessing the content of the message could not be possibile without measuring the message itself, or making a measurement of the entity thet encodes it. This translate into breaking the symmetry of Quantum Mechanics: states are superpositions of many probability amplitudes and only a measurement can "select" a unique state out of them. 

### The algorithm
Suppose Alice and Bob would like to communicate by a quantum device. The idea is that they need to encode each bit of message inside a qubit. Basically the number of bits that compose the message is the same of the number of qubits needed for the process. They need also a set of basis states that work as the encrypting and decrypting key for the classical cryptography framework. In fact, qubits are nothing else than photons who must be polarized before sending. If each polarization matches, than who recives the photons can apply a reversed process, then measure it to get the information about the classical message itself, otherwise, by measuring into a complete different basis state (physicists like to say projecting into a new basis state vectors)
