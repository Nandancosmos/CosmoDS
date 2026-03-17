# CosmoDS Documentation

# CosmoDS

**CosmoDS (Cosmological Dynamical Systems)** is a Python toolkit designed to study cosmological models at the background level using **dynamical system analysis** within the **Cobaya** inference framework. The package allows users to implement cosmological models in terms of dynamical variables and constrain them using modern cosmological datasets.

CosmoDS provides a flexible and modular framework to explore scalar-field dark energy models and other late-time cosmological scenarios while leveraging the powerful Bayesian inference tools implemented in Cobaya.

---

## Overview

Many cosmological models, particularly those involving scalar-field dark energy, are often studied using **dynamical system techniques**. In this approach, the cosmological evolution equations are rewritten as a system of autonomous differential equations in terms of dimensionless phase-space variables. This formulation provides a powerful framework to analyze the stability and evolution of cosmological models.

Modern cosmological parameter estimation is commonly performed using Bayesian inference frameworks such as **Cobaya**, which typically rely on Boltzmann solvers like **CLASS** or **CAMB** to compute cosmological observables. However, many theoretical models are constructed primarily to describe **late-time cosmic acceleration** and do not require a full treatment of early-universe perturbations.

Implementing such models in Boltzmann codes can therefore be unnecessarily complicated. CosmoDS provides an alternative approach by computing the **background cosmological evolution using dynamical system equations**, while still allowing parameter inference through the Cobaya framework.

---

## Features

- Dynamical system formulation of cosmological models
- Numerical integration of cosmological background evolution
- Direct interface with **Cobaya**
- Compatible with modern cosmological likelihoods
- Modular architecture for implementing new models
- Support for **Markov Chain Monte Carlo (MCMC)** parameter estimation
- Efficient background-only cosmological analysis

---

## Example Model

As a demonstration, CosmoDS includes an implementation of a **quintessence scalar-field dark energy model** with a power-law potential


$$ V(\phi) = V_0 \phi^m $$ 


The cosmological evolution is expressed in terms of the dimensionless dynamical variables

$$ x = \frac{\kappa \dot{\phi}}{\sqrt{6}H}, \qquad
y = \frac{\kappa \sqrt{V(\phi)}}{\sqrt{3}H} , \qquad \lambda = -\frac{1}{\kappa V(\phi)}\frac{dV(\phi)}{d\phi}. $$

Using these variables, the cosmological equations can be rewritten as an autonomous dynamical system that can be numerically integrated to compute cosmological observables such as:

- Hubble expansion rate \(H(z)\)
- Luminosity distance \(D_L(z)\)
- Angular diameter distance \(D_A(z)\)

These observables are then used in likelihood analyses within Cobaya.

---

## Files Description
- **cobaya_mcmc.py**: This script contains the core MCMC analysis code utilizing the Cobaya library.
- **plot.ipynb**: A Jupyter notebooks for visualizing results of the cosmological models.
- **model.py**: The cosmological model is implimented here.
- **README.md**: A comprehensive documentation file for the project.

## Setup
 **Clone the repository**:
   ```bash
   git clone https://github.com/Nandancosmos/CosmoDS.git
   cd CosmoDS
   ```

   

## Usage
1. To run the MCMC analysis, execute:
   ```bash
   python cobaya_mcmc.py
   ```
2. After the analysis, open Jupyter notebooks in the directory to explore results and visualizations.

## Requirements
- Python 3.x
- cobaya
- matplotlib
- numpy
- pandas

## Citation

If **CosmoDS** helps you in your research, please cite the corresponding paper describing the software and methodology and our research.

### Software paper

```bibtex
@misc{roy2026cosmodspythontoolkitconstraining,
      title={CosmoDS: A Python toolkit for constraining cosmological models via dynamical systems analysis with Cobaya}, 
      author={Nandan Roy and Prasanta Sahoo},
      year={2026},
      eprint={2603.14740},
      archivePrefix={arXiv},
      primaryClass={astro-ph.CO},
      url={https://arxiv.org/abs/2603.14740}, 
}

@article{Sahoo:2025cvz,
    author = "Sahoo, Prasanta and Roy, Nandan and Mondal, Himadri Shekhar",
    title = "{Constraint on momentum-transferred dark energy using DESI DR2}",
    eprint = "2506.21295",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.CO",
    doi = "10.1140/epjc/s10052-026-15341-8",
    journal = "Eur. Phys. J. C",
    volume = "86",
    number = "2",
    pages = "200",
    year = "2026"
}

@article{Thanankullaphong:2026anl,
    author = "Thanankullaphong, Phusuda and Sahoo, Prasanta and Hassan Puttasiddappa, Prajwal and Roy, Nandan",
    title = "{Quintom Dark Energy: Future Attractor and Phantom Crossing in Light of DESI DR2 Observation}",
    eprint = "2601.02284",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.CO",
    month = "1",
    year = "2026"
}
