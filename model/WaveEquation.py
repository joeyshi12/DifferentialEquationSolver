import numpy as np

from model.PDE import PDE


class WaveEquation(PDE):
    c: float

    def __init__(self, c: float, boundary_type: int, p, q, f, g):
        self.c = c
        super().__init__(boundary_type, p, q)
        self.f = f  # initial values
        self.g = g  # initial derivatives

    def integrate_dirichlet(self, dx: float, dt: float, n: int, m: int, k) -> np.array:
        u = []
        u_0 = [self.f(i * dx) for i in range(n + 1)]    # initial values
        u.append(u_0)
        u_1 = [(k ** 2 * u_0[i + 1] + 2 * (1 - k ** 2) * u_0[i] + k ** 2 * u_0[i - 1]) / 2 + dt * self.g(i * dx)
               for i in range(1, n)]                    # next values
        u_1 = [self.p(dt)] + u_1 + [self.q(dt)]         # next boundary values
        u.append(u_1)
        for j in range(2, m + 1):
            self.add_layer_dirichlet(dt, j, k, n, u)
        return np.array(u)

    def integrate_neumann(self, dx: float, dt: float, n: int, m: int, k: float) -> np.array:
        u = []
        u_0 = [self.f(i * dx) for i in range(n + 1)]                                    # initial values
        u_0 = [u_0[1] - 2 * self.p(0) * dx] + u_0 + [u_0[-2] + 2 * self.q(0) * dx]      # initial boundary values
        u.append(u_0)
        u_1 = [(k ** 2 * u_0[i + 1] + 2 * (1 - k ** 2) * u_0[i] + k ** 2 * u_0[i - 1]) / 2 + dt * self.g(i * dx)
               for i in range(n + 1)]                                                   # next values
        u_1 = [u_1[1] - 2 * self.p(dt) * dx] + u_1 + [u_1[-2] + 2 * self.q(dt) * dx]    # next boundary values
        u.append(u_1)
        for j in range(2, m + 1):
            self.add_layer_neumann(dt, dx, j, k, n, u)
        u = np.delete(u, 0, 1)
        u = np.delete(u, n + 1, 1)
        return np.array(u)

    def integrate_mixed_1(self, dx: float, dt: float, n: int, m: int, k: float) -> np.array:
        u = []
        u_0 = [self.f(i * dx) for i in range(n + 1)]                # initial values
        u_0 = u_0 + [u_0[-1] + 2 * self.q(0) * dx]                  # initial boundary values
        u.append(u_0)
        u_1 = [(k ** 2 * u_0[i + 1] + 2 * (1 - k ** 2) * u_0[i] + k ** 2 * u_0[i - 1]) / 2 + dt * self.g(i * dx)
               for i in range(1, n + 1)]                            # next values
        u_1 = [self.p(dt)] + u_1 + [u_1[-1] + 2 * self.q(dt) * dx]  # next boundary values
        u.append(u_1)
        for j in range(2, m + 1):
            self.add_layer_mixed_1(dt, dx, j, k, n, u)
        u = np.delete(u, n + 1, 1)
        return np.array(u)

    def integrate_mixed_2(self, dx: float, dt: float, n: int, m: int, k: float) -> np.array:
        u = []
        u_0 = [self.f(i * dx) for i in range(n + 1)]                # initial values
        u_0 = [u_0[0] - 2 * self.p(0) * dx] + u_0                   # initial boundary values
        u.append(u_0)
        u_1 = [(k ** 2 * u_0[i + 1] + 2 * (1 - k ** 2) * u_0[i] + k ** 2 * u_0[i - 1]) / 2 + dt * self.g(i * dx)
               for i in range(n)]                                   # next values
        u_1 = [u_1[0] - 2 * self.p(dt) * dx] + u_1 + [self.q(dt)]   # next boundary values
        u.append(u_1)
        for j in range(2, m + 1):
            self.add_layer_mixed_2(dt, dx, j, k, n, u)
        print(u)
        u = np.delete(u, 0, 1)
        return np.array(u)

    def calc_k(self, dx: float, dt: float) -> float:
        return self.c * dt / dx

    def node_val(self, u: np.array, k: float, i: int, j: int) -> float:
        return k ** 2 * u[j - 1][i + 1] + 2 * (1 - k ** 2) * u[j - 1][i] + k ** 2 * u[j - 1][i - 1] - u[j - 2][i]

    def get_stable_m(self, L: float, n: int, t: float) -> int:
        m = 2 * np.ceil(self.c * t * n / L)
        return int(m)