from examples.simplest_example import (
    get_default_settings,
    get_simplest_model_sliding,
)
import nosnoc

NS_VALUES = range(1, 5)
N_FINITE_ELEMENT_VALUES = range(2, 5)


# TODO: add control stages instead of just simulation
def main_w_test():
    model = get_simplest_model_sliding()

    for ns in NS_VALUES:
        for Nfe in N_FINITE_ELEMENT_VALUES:
            for pss_mode in nosnoc.PssMode:
                for irk in nosnoc.IRKSchemes:
                    settings = get_default_settings()
                    settings.step_equilibration = nosnoc.StepEquilibrationMode.HEURISTIC_MEAN
                    settings.print_level = 0
                    settings.n_s = ns
                    settings.N_finite_elements = Nfe
                    settings.irk_scheme = irk
                    settings.pss_mode = pss_mode

                    if pss_mode == nosnoc.PssMode.STEWART:
                        nx = 1
                        nz = 5
                        nh = 1
                    elif pss_mode == nosnoc.PssMode.STEP:
                        nx = 1
                        nz = 3
                        nh = 1

                    if irk == nosnoc.IRKSchemes.RADAU_IIA:
                        n_end = 0
                    elif irk == nosnoc.IRKSchemes.GAUSS_LEGENDRE:
                        if pss_mode == nosnoc.PssMode.STEWART:
                            n_end = nz - 2
                        elif pss_mode == nosnoc.PssMode.STEP:
                            n_end = nz - 1

                    nw_expected = nx + Nfe * (ns * (nx + nz) + nh + nx) + (Nfe - 1) * (n_end)
                    try:
                        solver = nosnoc.NosnocSolver(settings, model)
                        assert (solver.w.shape[0] == nw_expected)
                    except AssertionError:
                        raise Exception(f"Test failed with setting:\n {settings=} \n{model=}")
    print("main_w_test: SUCCESS")


if __name__ == "__main__":
    main_w_test()