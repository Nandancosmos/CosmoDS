from cobaya import run
from model import CosmoBG
# from DESI_liklihood import DESIDR2BAOLikelihood
mu_H0 = 67.0    # Mean (mu) for the H0 Gaussian prior
sigma_H0 = 2.0
info_test = {

    "theory": {
        "cosmo": {
            "external": CosmoBG,
        "provides": ["angular_diameter_distance", "comoving_angular_distance", "Hubble", "rdrag"]
        }
    },
    "likelihood": {
        "bao.desi_dr2": {"stop_at_error": False},
        "sn.desy5": None,   # optional
    },

    "params": {

        # --- Standard Cosmological Parameters ---
        "H0": {
            "prior": {"min": 60, "max": 80},
            "proposal": 0.2,
            "ref": 67.4,
            "latex": "H_0"
        },

        "Omegab0": {
            "prior": {"min": 0.01, "max": 0.1},
            "ref": 0.049,
            "proposal": 0.0005,
            "latex": r"\Omega_b"
        },

        "Omegam0": {
            "prior": {"min": 0.1, "max": 0.5},
            "ref": 0.315,
            "proposal": 0.005,
            "latex": r"\Omega_\mathrm{m}"
        },

        "Mb": {
            "prior": {"min": -20, "max": -18},
            "ref": -19.24,
            "proposal": 0.01,
            "latex": r"\M_{b}"
        },

        # --- Quintessence Model Parameters (V ~ phi^m) ---
        "x0": {
            "prior": {"min": 0, "max": 0.5},
            "proposal": 0.1,
            "ref": 0.01,
            "latex": "x_0"
        },

        "lambda0": {
            "prior": {"min": 0.0, "max": 2.0},
            "proposal": 0.1,
            "ref": 0.5,
            "latex": r"\lambda_0"
        },

        # Power-law index of the potential (fixed)
        "m": 2,

        # --- Derived Parameters ---
        "Omega_phi0": {
            "derived": "lambda Omegam0: 1 - Omegam0",
            "latex": r"\Omega_{\phi,0}"
        },

        "w_phi0": {
            "derived": "lambda x0, Omegam0: (2*x0**2 + Omegam0 - 1) / (1 - Omegam0)",
            "latex": r"w_{\phi,0}"
        },

        "rd": {
            "derived": "lambda rdrag: rdrag",
            "latex": r"r_d"
        },

        # y0 from Friedmann constraint (late-time)
        "y0": {
            "derived": (
                "lambda x0, Omegam0: "
                "np.sqrt(max(0.0, 1.0 - x0**2 - Omegam0))"
            ),
            "latex": r"y_0"
        }
    },
    "sampler": {"mcmc": {
#         "max_samples": 50000,
        "Rminus1_stop": 0.02,
        "burn_in": 40}},
    "resume": True,
    "output": "chains/desy5/test_run",
    "debug": True
}
updated_info, sampler = run(info_test, debug=True)
