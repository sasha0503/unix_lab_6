import random
import time
import matplotlib.pyplot as plt
import tqdm

from multiprocessing import Process


class Vector:
    def __init__(self, vector):
        self.vector = vector
        self.length = len(vector)

    def __repr__(self):
        return f"Vector({self.vector})"

    def __mul__(self, other):
        if isinstance(other, Vector):
            return sum([self.vector[i] * other.vector[i] for i in range(self.length)])
        elif isinstance(other, int):
            return Vector([self.vector[i] * other for i in range(self.length)])
        else:
            raise TypeError("Multiplication is not defined for this type")

    def __rmul__(self, other):
        return self.__mul__(other)

    @property
    def shape(self):
        return self.length, 1


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def __repr__(self):
        return f"Matrix({self.matrix})"

    def T(self):
        return Matrix(list(zip(*self.matrix)))

    @property
    def shape(self):
        return len(self.matrix), len(self.matrix[0])


def _mul(pairs, pairs_idx, res_mat) -> None:
    for pair, idx in zip(pairs, pairs_idx):
        res_mat[idx[0]][idx[1]] = Vector(pair[0]) * Vector(pair[1])


def matrix_mult(a: Matrix, b: Matrix, n_workers: int = 1) -> Matrix:
    assert a.shape[1] == b.shape[0], "Matrices are not aligned"
    b_t = b.T()
    threads = []
    total = a.shape[0] * b.shape[1]
    operations_per_thread = total // n_workers
    result = [[0 for _ in range(b.shape[1])] for _ in range(a.shape[0])]
    counter = 0
    pairs = []
    idx = []
    current_pairs = []
    current_idx = []
    for i in range(0, a.shape[0]):
        for j in range(0, b.shape[1]):
            current_pairs.append((a.matrix[i], b_t.matrix[j]))
            current_idx.append((i, j))
            counter += 1
            if counter % operations_per_thread == 0 and len(threads) < n_workers - 1:
                pairs.append(current_pairs)
                idx.append(current_idx)
                current_pairs = []
                current_idx = []
    if current_pairs:
        pairs.append(current_pairs)
        idx.append(current_idx)
    for i in range(len(pairs)):
        threads.append(Process(target=_mul, args=(pairs[i], idx[i], result)))
        threads[-1].start()
    for thread in threads:
        thread.join()

    return Matrix(result)


if __name__ == '__main__':
    n = 600
    m = 600
    k = 200

    matrix_a = Matrix([[random.randint(0, 10) for _ in range(m)] for _ in range(n)])
    matrix_b = Matrix([[random.randint(0, 10) for _ in range(k)] for _ in range(m)])

    times = []
    N_RUNS = 15
    for n_processes in tqdm.trange(1, N_RUNS):
        start_time = time.time()
        matrix_c = matrix_mult(matrix_a, matrix_b, n_workers=n_processes)
        times.append(time.time() - start_time)

    plt.plot(range(1, N_RUNS), times)
    plt.xticks(range(1, N_RUNS))
    plt.xlabel("Number of processes")
    plt.ylabel("Time, s")
    plt.show()
