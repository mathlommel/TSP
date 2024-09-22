import datetime
import numpy as np
import pathlib
import time
import tsplib95

from Algorithms.OKsolve_dfj import solve_dfj
from Algorithms.OKsolve_hk import solve_hk
from Algorithms.OKsolve_lk import solve_lk
from Algorithms.OKsolve_mtz import solve_mtz
from Algorithms.OKsolve_nn import solve_nn
from Algorithms.OKsolve_ac import solve_ac



def load_instance(instance_name):
    path = pathlib.Path(__file__).parent.joinpath(instance_name)
    prob = tsplib95.load(path)
    nodes = list(prob.get_nodes())
    edges = list(prob.get_edges())
    n = len(nodes)
    M = np.zeros((n, n))
    for edge in edges:
        i, j = edge
        M[i-1, j-1] = prob.get_weight(*edge)
        M[j-1, i-1] = prob.get_weight(*edge)
    return M


if __name__ == "__main__":
    instance = "gr24.tsp"
    method   = "ac"         # choices: "ac", "ct", "dfj", "hk", "lk", "mtz", "nn"

    print("Instance   : {}".format(instance))
    print("Method     : {}".format(method))

    M = load_instance(instance)

    t0 = time.time()
    if method == "ac":
        cost = solve_ac(M)
    elif method == "dfj":
        cost = solve_dfj(M)
    elif method == "hk":
        cost = solve_hk(M)
    elif method == "lk":
        cost = solve_lk(M)
    elif method == "mtz":
        cost = solve_mtz(M)
    elif method == "nn":
        cost = solve_nn(M)
    else:
        raise NotImplementedError
    t1 = time.time()

    print("Solve time : {}".format(datetime.timedelta(seconds=t1-t0)))
    print("Tour cost  : {}".format(cost))
