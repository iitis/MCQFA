import argparse
import pickle

import numpy as np
from math import pi
from qiskit import *


def create_circuit_ry(n,length,k,p):
    qc = QuantumCircuit(n, n)

    for i in range(n):
        qc.h(i)
    qc.barrier()
    for i in range(length):
        qc.ry(2 * 2 * k[0] * pi / p, n-1)
        for j in range(n-1):
            qc.cry(2 * 2 * k[j+1] * pi / p, j, n-1)
        qc.barrier()
    for i in range(n):
        qc.h(i)
    return qc

def create_circuit_rz(n,length,k,p):
    qc = QuantumCircuit(n, n)

    for i in range(n):
        qc.h(i)
    qc.sx(n-1)
    qc.barrier()
    for i in range(length):
        qc.rz(2 * 2 * k[0] * pi / p, n-1)
        for j in range(n-1):
            qc.crz(2 * 2 * k[j+1] * pi / p, j, n-1)
        qc.barrier()
    qc.sxdg(n - 1)
    for i in range(n):
        qc.h(i)
    return qc

def get_backend(backend):
    provider = IBMQ.load_account()
    if backend == "simulator":
        machine = Aer.get_backend("qasm_simulator")
    else:
        machine = provider.get_backend(f"ibmq_{backend}")
    return machine

def execute_circuit(qc,machine,shots,opt):
    job = execute(qc, machine, shots=shots, optimization_level=2)
    result = job.result()
    return result.get_counts()

def optimized(experiment, backend, p, word_length, k,n,shots):
    machine = get_backend(backend)
    d = []

    for length in range(1, word_length + 1):

        if experiment == "ry":
            qc = create_circuit_ry(n,length,k,p)
        elif experiment == "rz":
            qc = create_circuit_rz(n, length, k, p)
        qc.measure(qc.qubits, qc.clbits)

        counts = execute_circuit(qc,machine,shots,2)
        print("Word length",length, counts)
        d.append((length, counts))
    return d

def get_single_circuit(experiment,length,p):
    qc = QuantumCircuit(1, 1)
    if experiment == "rz":
        qc.sx(0)
    qc.barrier
    for _ in range(length):
        if experiment == "ry":
            qc.ry(2 * 2 * pi / p, 0)
        elif experiment == "rz":
            qc.rz(2 * 2 * pi / p, 0)
        qc.barrier()
    if experiment == "rz":
        qc.sxdg(0)
    return qc


def single(experiment, backend, p, word_length, shots):
    machine = get_backend(backend)
    d = []
    for length in range(word_length+1):
        qc= get_single_circuit(experiment, length, p)
        qc.measure(qc.qubits, qc.clbits)

        counts = execute_circuit(qc, machine, shots, 2)
        print("Word length", length, counts)
        d.append((length, counts))
    return d


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("implementation", type=str, choices=["single", "optimized"],
                        help="To run a single qubit automaton type single. To run the optimized implementation type optimized.")
    parser.add_argument("experiment", type=str, choices=["rz", "ry"],
                        help="rz or ry should be selected.")
    parser.add_argument("-backend", type=str,default="belem",
                        help="IBMQ backend to be used. Type simulator for local simulator and the name for ibmq simulator. Default is belem.")
    parser.add_argument("-p", type=int,default=11,
                        help="p value. Default is 11.")
    parser.add_argument("-n", type=int, default=3,
                        help="Number of qubits. Default is 3.")
    parser.add_argument("-length", type=int,default=-1,
                        help="Word length until which the simulations will be run. Default is 2 times the word length.")
    parser.add_argument('-k', nargs="+", type=int, default=[3,5,7],
                        help="List of k values. Type seperated by space.")
    parser.add_argument('-shots', type=int, default=8192,
                        help="Number of shots. Default is 8192.")
    parser.add_argument('-verbose', action="store_true", default=False,
                        help="Whether to print the simulation results. Default is False.")

    parser.set_defaults(pre=True)
    args = parser.parse_args()

    if args.length ==-1:
        args.length = args.p *2

    if args.implementation == "optimized":
        data = optimized(args.experiment,args.backend,args.p,args.length,args.k,args.n,args.shots)
        filehandler = open(f"{args.implementation}_{args.experiment}_{args.p}_{args.n}_{args.k}_{args.backend}.", "wb")
    elif args.implementation == "single":
        data = single(args.experiment, args.backend, args.p, args.length, args.shots)
        filehandler = open(f"{args.implementation}_{args.experiment}_{args.p}_{args.backend}.", "wb")


    pickle.dump(data, filehandler)