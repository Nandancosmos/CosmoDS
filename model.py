import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
from cobaya.theory import Theory
from scipy.integrate import quad

try:
    from scipy.integrate import cumulative_trapezoid
except ImportError:
    from scipy.integrate import cumtrapz as cumulative_trapezoid


class CosmoBG(Theory):

    provides = [
        "angular_diameter_distance",
        "comoving_angular_distance",
        "Hubble",
        "comoving_radial_distance",
        "rdrag"
    ]

    params = {
        "H0": None,
        "Omegam0": None,
        "x0": None,
        "lambda0": None,
        "m": None,
        "Mb": None, 
        "Omegab0": None,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._current_state = {}
        self.N = np.linspace(0, -32, 10000)
        self.c_km_s = 2.99792458e5


    # --------------------------------------------------
    # Dynamical system
    # --------------------------------------------------

    def equation(self, N, y, params_values):

        x, yphi, lam, H, dl = y

        H0 = params_values["H0"]
        Omegam0 = params_values["Omegam0"]
        m = params_values["m"]

        z = np.exp(-N) - 1

        Tcmb = 2.725
        h0 = H0 / 100

        zeq = (2.5E4) * (Omegam0 * h0**2) * (Tcmb / 2.7)**(-4)
        or0 = Omegam0 / (1 + zeq)

        dNdt = H
        dNdz = -1 / (1 + z)

        # -----------------------------
        # Dynamical system
        # -----------------------------

        zdynam = (1 + x*x - yphi*yphi)

        xprime = -3*x + np.sqrt(1.5)*lam*yphi*yphi + 1.5*x*zdynam

        yprime = -np.sqrt(1.5)*lam*x*yphi + 1.5*yphi*zdynam

        lamprime = np.sqrt(6)*(lam*lam/m)*x

        # -----------------------------
        # Hubble evolution
        # -----------------------------

        Hdot = -(3/2)*H*H*(
            ((H0/H)*(H0/H)*(Omegam0*(1+z)**3 + or0*(1+z)**4))
            + 2*x*x
        )

        eqH = Hdot / dNdt

        # -----------------------------
        # Luminosity distance
        # -----------------------------

        ddl_dz = dl/(1.0+z) + (self.c_km_s/H)*(1.0+z)

        ddl_dN = ddl_dz/dNdz

        return [xprime, yprime, lamprime, eqH, ddl_dN]


    # --------------------------------------------------
    # ODE solver
    # --------------------------------------------------

    def ode_solve_and_interpolate(self, params_values):

        N_min = float(np.min(self.N))

        N_eval = np.linspace(0, N_min, 10000)

        H0 = params_values["H0"]
        Omegam0 = params_values["Omegam0"]

        x0 = params_values["x0"]
        lam0 = params_values["lambda0"]

        Tcmb = 2.725
        h0 = H0 / 100

        zeq = (2.5E4)*(Omegam0*h0**2)*(Tcmb/2.7)**(-4)

        or0 = Omegam0/(1+zeq)

        dl0 = 0.0

        # Friedmann constraint

        arg = 1 - Omegam0 - or0 - x0**2

        y0 = np.sqrt(arg)

        init = [x0, y0, lam0, H0, dl0]

        sol = solve_ivp(
            lambda zz, yy: self.equation(zz, yy, params_values),
            t_span=(0.0, N_min),
            y0=init,
            t_eval=N_eval,
            rtol=1e-6,
            atol=1e-8,
            method="RK45"
        )

        H_interp = interp1d(sol.t, sol.y[3], kind='linear', fill_value="extrapolate")

        dl_interp = interp1d(sol.t, sol.y[4], kind='linear', fill_value="extrapolate")

        N_sol = sol.t
        z_sol = np.exp(-N_sol) - 1

        H_interpz = interp1d(z_sol, sol.y[3], kind='linear', fill_value="extrapolate")

        dl_interpz = interp1d(z_sol, sol.y[4], kind='linear', fill_value="extrapolate")

        return H_interp, dl_interp, H_interpz, dl_interpz, sol.t, sol.y, z_sol


    # --------------------------------------------------
    # Calculate cosmology
    # --------------------------------------------------

    def calculate(self, state, want_derived=True, **params_values):

        H_interp, dl_interp, H_interpz, dl_interpz, t_sol, y_sol, z_sol = \
            self.ode_solve_and_interpolate(params_values)

        Hz = H_interpz(z_sol)

        DL = dl_interpz(z_sol)

        H0 = params_values["H0"]
        Omegab0 = params_values.get("Omegab0")
        Omegam0 = params_values["Omegam0"]

        h = H0/100.0

        rd = 147.05*(Omegab0*h**2/0.02236)**(-0.13) * (Omegam0*h**2/0.1432)**(-0.23)

        rdrag = float(rd)

        obh2 = Omegab0*h*h
        om0 = Omegam0

        Tcmb = 2.725

        zeq = (2.5E4)*(om0*h**2)*(Tcmb/2.7)**(-4)

        or0 = om0/(1+zeq)

        g1 = (0.0783*(obh2)**(-0.238))/(1+39.5*(obh2)**0.763)

        g2 = 0.560/(1+21.1*(obh2)**1.81)

        zcmb = 1048*(1+0.00124*(obh2)**(-0.738))*(1+g1*(om0*h**2)**g2)


        def cs(z):

            R = (obh2/(1+z))*31500*(Tcmb/2.7)**(-4)

            return self.c_km_s/np.sqrt(3*(1+R))


        def Hz_f(z):

            Ez2 = om0*(1+z)**3 + or0*(1+z)**4 + (1-om0-or0)

            return np.sqrt(Ez2)*H0


        def Dm_integrand(x):

            return self.c_km_s/Hz_f(x)


        (dc2, dc1) = quad(Dm_integrand,0.0,zcmb)

        dMcmb = dc2


        def rs_integrand(x):

            return cs(x)/Hz_f(x)


        (rs2, rs1) = quad(rs_integrand,zcmb,np.inf)

        rcmb = rs2

        theta_s = rcmb/dMcmb


        state.update({

            "Hubble":{"z":list(z_sol),"H":list(Hz)},

            "angular_diameter_distance":{
                "z":list(z_sol),
                "dist":list(DL/((1.0+z_sol)**2))
            },

            "rdrag":rdrag,

            "theta_s":theta_s
        })


        if want_derived:

            state["derived"] = {

                "rdrag":rdrag,

                "theta_s":theta_s
            }

        self._current_state = state


    # --------------------------------------------------
    # Getters
    # --------------------------------------------------

    def get_angular_diameter_distance(self,z=None):

        da = self._current_state["angular_diameter_distance"]

        if z is None:

            return da

        val = np.interp(z,da["z"],da["dist"])

        return np.atleast_1d(val)


    def get_Hubble(self,z=None,units="km/s/Mpc"):

        c_km_s = 299792.458

        hubble = self._current_state["Hubble"]

        if z is None:

            return hubble

        Hz = np.interp(z,hubble["z"],hubble["H"])

        if units=="1/Mpc":

            Hz = Hz/c_km_s

        return np.atleast_1d(Hz)


    def get_rdrag(self):

        if "derived" in self._current_state:

            return float(self._current_state["derived"]["rdrag"])

        return float(self._current_state.get("rdrag",0.0))


    def get_theta_s(self):

        if "derived" in self._current_state:

            return float(self._current_state["derived"]["theta_s"])

        return float(self._current_state.get("theta_s",0.0))