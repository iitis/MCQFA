from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller
from qiskit.visualization import plot_circuit_layout

from experiment import *


def optimized_tr(experiment, backend, length, n, k, p, opt):
    if experiment == "rz":
        qc = create_circuit_rz(n, length, k, p)
    elif experiment == "ry":
        qc = create_circuit_rz(n, length, k, p)

    return transpile(qc, backend, optimization_level=opt)


def single_tr(experiment, backend, length, p, opt):

    qc = get_single_circuit(experiment, length, p)
    return transpile(qc, backend, optimization_level=opt)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "experiment",
        type=str,
        choices=["rz", "ry"],
        help="rz or ry should be selected.",
    )
    parser.add_argument(
        "implementation",
        type=str,
        choices=["single", "optimized"],
        help="To run a single qubit automaton type single. To run the optimized implementation type optimized.",
    )
    parser.add_argument(
        "backend",
        type=str,
        default="belem",
        help="IBMQ backend to be used. Type simulator for local simulator. Default is belem.",
    )
    parser.add_argument("-p", type=int, default=11, help="p value. Default is 11.")
    parser.add_argument(
        "-n", type=int, default=3, help="Number of qubits. Default is 3."
    )
    parser.add_argument("length", type=int, default=11, help="Length of the string.")
    parser.add_argument(
        "-k",
        nargs="+",
        type=int,
        default=[3, 5, 7],
        help="List of k values. Type seperated by space.",
    )
    parser.add_argument(
        "-opt", type=int, default=2, help="Optimization level. Default is 2."
    )
    parser.add_argument(
        "-circuit",
        action="store_true",
        default=False,
        help="Whether to draw transpiled circuit. Default is False.",
    )

    parser.set_defaults(pre=True)
    args = parser.parse_args()

    machine = get_backend(args.backend)

    if args.implementation == "optimized":
        tp = optimized_tr(
            args.experiment, machine, args.length, args.n, args.k, args.p, args.opt
        )
    elif args.implementation == "single":
        tp = single_tr(args.experiment, machine, args.length, args.p, args.opt)
    basis = machine.configuration().basis_gates
    pass_ = Unroller(basis)
    pm = PassManager(pass_)
    new_circuit = pm.run(tp)
    print(new_circuit.count_ops())
    if args.circuit:
        print(tp.draw(output="text"))
