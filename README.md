# State-efficient QFA algorithm for quantum computers

Responsible person: Özlem Salehi (osalehi[at]iitis.pl).

The code necessary for running the experiments in the paper "State-efficient QFA Algorithm for Quantum Computers" is given here.

The code was tested under Windows. You should install Qiskit to be able to run the codes. In order to access IBMQ backends, you should create an account on https://www.ibm.com/quantum-computing/ and follow the instructions given [here](https://quantum-computing.ibm.com/lab/docs/iql/manage/account/ibmq). 

## Data used in the manuscript

Data used in the manuscript is located inside the data folder. 

## Reproducing data

### Single qubit MCQFA

Run the following command in the main directory to run single-qubit MCQFA using the default values which were used in the manuscript. The results are saved as a pickle file.


```
python experiments.py single ry
```

You can pass optional arguments to modify default parameters:

```-backend```: IBMQ backend to be used. Type simulator for local simulator and the name for ibmq simulator. Default is belem.
                        
```-p```: p value. Default is 11.

```-length```: Word length until which the simulations will be run. Default is 2 times the word length.

```-shots```: Number of shots. Default is 8192.

```-verbose```: If this option is seleced, output is printed on screen.

Here is another example run:

```
python experiments.py rz single -backend simulator -p 31 -length 5 -shots 1000 -verbose 
```

### Optimized MCQFA

Run the following command in the main directory to run optimized MCQFA:

```
python experiments.py optimized ry
```

The above command runs optimized MCQFA with the implementation using Ry gates, using the default values which were used in the manuscript. The results are saved as pickle file.

In the addition to the optional parameters given above, the following may be provided when running the optimized experiment.

,```-n```: Number of qubits. Default is 3.

```-k```: Set of k values (type by leaving space). Default is 3 5 7. Number of entries should be equal to number of qubits.

### Fidelity calculation

Run the following command to calculate fidelities of the states prodecued in the noisy and noiseless experiements.

```
python fidelity.py
```

The above command runs optimized MCQFA both using the noise model from IBM Belem backend and using the simulator using the default values indicated in the manuscripted. The fidelities are saved as pickle files inside data folder.

The following optional parameters may be provided:

```-p```: p value. Default is 11.

```-n```: Number of qubits. Default is 3.

```-backend```: IBMQ backend to be used. Default is belem.

```-length```: Word length until which the simulations will be run. Default is 2 times the word length.

```-k```: Set of k values (type by leaving space). Default is 3 5 7. Number of entries should be equal to number of qubits.

```-shots```: Number of shots. Default is 10000.

```-plot```: If this option is seleced, plot is generated.
