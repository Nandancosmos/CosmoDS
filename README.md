# CosmoDS Documentation

## Overview
CosmoDS is a project that involves cosmological MCMC analysis using Cobaya. It includes model fitting and various visualization techniques to analyze cosmological data effectively.

## Files Description
- **mcmc_analysis.py**: This script contains the core MCMC analysis code utilizing the Cobaya library.
- **visualization_notebooks/**: A directory containing Jupyter notebooks for visualizing results of the cosmological models.
- **config.yaml**: Configuration file for setting parameters and options for the analysis.
- **README.md**: A comprehensive documentation file for the project.

## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nandancosmos/CosmoDS.git
   cd CosmoDS
   ```
2. **Install dependencies**:
   Make sure to have Python 3.x installed. Use pip to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. To run the MCMC analysis, execute:
   ```bash
   python mcmc_analysis.py
   ```
2. After the analysis, open Jupyter notebooks in the `visualization_notebooks/` directory to explore results and visualizations.

## Requirements
- Python 3.x
- cobaya
- matplotlib
- numpy
- pandas

For complete requirements, refer to the `requirements.txt` file.

## License
This project is licensed under the MIT License.