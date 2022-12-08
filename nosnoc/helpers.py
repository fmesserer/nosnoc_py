import numpy as np
from .nosnoc import NosnocSolver


class NosnocSimLooper:

    def __init__(self, solver: NosnocSolver, x0: np.ndarray, Nsim: int):
        self.solver = solver
        self.Nsim = Nsim

        self.xcurrent = x0
        self.X_sim = [x0]
        self.time_steps = np.array([])
        self.theta_sim = []
        self.lambda_sim = []

        self.cpu_nlp = np.zeros((Nsim, solver.settings.max_iter_homotopy))

    def run(self):
        for i in range(self.Nsim):
            self.solver.set("x", self.xcurrent)
            results = self.solver.solve()
            # collect
            self.X_sim += results["x_list"]
            self.xcurrent = self.X_sim[-1]
            self.cpu_nlp[i, :] = results["cpu_time_nlp"]
            self.time_steps = np.concatenate((self.time_steps, results["time_steps"]))
            self.theta_sim += results["theta_list"]
            self.lambda_sim += results["lambda_list"]

    def get_results(self):
        self.t_grid = np.concatenate((np.array([0.0]), np.cumsum(self.time_steps)))

        results = {
            "X_sim": self.X_sim,
            "cpu_nlp": self.cpu_nlp,
            "time_steps": self.time_steps,
            "t_grid": self.t_grid,
            "theta_sim": self.theta_sim,
            "lambda_sim": self.lambda_sim,
        }
        return results