import matplotlib.pyplot as plt
from matplotlib import rc
from qiskit.providers.aer import QasmSimulator
from qiskit.quantum_info import state_fidelity

from experiment import *


def optimized_noise_density(experiment, machine, p, word_length, k, n, shots):
    d = []
    backend = get_backend(machine)

    for length in range(1, word_length + 1):

        if experiment == "ry":
            qc = create_circuit_ry(n, length, k, p)
        elif experiment == "rz":
            qc = create_circuit_rz(n, length, k, p)
        if machine != "simulator":
            backend = QasmSimulator(method="density_matrix").from_backend(backend)
        else:
            backend = QasmSimulator(method="density_matrix")
        qc.save_density_matrix()
        result = execute(qc, backend, shots=shots).result()
        d.append((length, result))
    return d


def calc_densities(p, word_length, k, n, shots, backend):
    density_z = optimized_noise_density("rz", backend, p, word_length, k, n, shots)
    density_y = optimized_noise_density("ry", backend, p, word_length, k, n, shots)
    ideal_z = optimized_noise_density("rz", "simulator", p, word_length, k, n, shots)
    ideal_y = optimized_noise_density("ry", "simulator", p, word_length, k, n, shots)
    return density_z, density_y, ideal_z, ideal_y


def calc_fidelity(density_noise, density_ideal):
    f = []
    for result1, result2 in zip(density_noise, density_ideal):
        d1 = result1[1].data()["density_matrix"]
        d2 = result2[1].data()["density_matrix"]
        f.append(state_fidelity(d1, d2))
    return f

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", type=int, default=11, help="p value. Default is 11.")
    parser.add_argument(
        "-n", type=int, default=3, help="Number of qubits. Default is 3."
    )
    parser.add_argument(
        "-backend",
        type=str,
        default="belem",
        help="IBMQ backend to be used. Default is belem.",
    )
    parser.add_argument(
        "-length",
        type=int,
        default=-1,
        help="Word length until which the simulations will be run. Default is 2 times the word length.",
    )
    parser.add_argument(
        "-k",
        nargs="+",
        type=int,
        default=[3, 5, 7],
        help="List of k values. Type seperated by space.",
    )
    parser.add_argument(
        "-shots", type=int, default=10000, help="Number of shots. Default is 10000."
    )
    parser.add_argument(
        "-plot",
        action="store_true",
        default=False,
        help="Whether to generate the plot. Default is False.",
    )

    parser.set_defaults(pre=True)
    args = parser.parse_args()
    if args.length == -1:
        args.length = args.p * 2

    density_z, density_y, ideal_z, ideal_y = calc_densities(args.p, args.length, args.k, args.n, args.shots, args.backend)

    f_z_avg = calc_fidelity(density_z, ideal_z)
    f_y_avg = calc_fidelity(density_y, ideal_y)
    file_z = open("f_z_avg", "wb")
    pickle.dump(f_z_avg, file_z)
    file_y = open("f_y_avg", "wb")
    pickle.dump(f_y_avg, file_y)

    if args.plot:

        plt.rcParams.update({"font.size": 10})

        rc("font", **{"family": "serif", "serif": ["Computer Modern"]})
        rc("text", usetex=True)

        s1 = plt.scatter(range(1, args.length+1), f_z_avg, marker="o")
        s2 = plt.scatter(range(1, args.length+1), f_y_avg, marker="x")

        plt.legend([s1, s2], ["New", "Original"])
        # plt.legend(title='')

        plt.xlabel("String Length")
        plt.ylabel("Fidelity")
        # plt.show()
        plt.savefig("fidelities.pdf")
