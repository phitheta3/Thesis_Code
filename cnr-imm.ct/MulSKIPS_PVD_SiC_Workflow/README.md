MulSKIPS PVD Workflow for 3C-SiC

This repository provides a full Python-based workflow to simulate and analyze Physical Vapor Deposition (PVD) processes on 3C-SiC substrates using the atomic-scale simulator MulSKIPS. The workflow includes simulation execution, post-processing, and export of results in FAIR-compliant NeXus format (.nxs) according to FAIRmat standards via the NOMAD platform.

Overview

The workflow covers:
- Execution of PVD simulations with MulSKIPS  
- Automated analysis of growth rate, surface roughness, and vacancy concentration  
- Export to NeXus format conforming to NXmicrostructure_imm_config and NXmicrostructure_imm_results (FAIRmat)

Project Structure

.
├── run_PVD_SiC.py            # Script to launch MulSKIPS simulation
├── analyze_PVD_SiC.py        # Post-processing and analysis script
├── Parser_May_2.ipynb        # Jupyter notebook automating full pipeline
├── SiC_sample_153.nxs        # Example output file (FAIRmat-compliant)
├── requirements.txt          # Dependencies list
├── input_files/              # Input geometries and simulation parameters
├── results/                  # Output: .xyz, logs, surface/growth data
└── README.md

Requirements

- Python ≥ 3.8  
- Python packages: numpy, pandas, matplotlib, h5py  
- MulSKIPS compiled from source  
- FAIRmat NeXus definitions (NXmicrostructure_imm_config, NXmicrostructure_imm_results)

Install dependencies with:

pip install -r requirements.txt

Setup

1. Clone and compile MulSKIPS:

git clone https://github.com/MulSKIPS/MulSKIPS.git
cd MulSKIPS
make all

2. Configure paths:
- Set the path to the MulSKIPS executable in run_PVD_SiC.py
- Adjust input/output folder paths as needed

How to Use

1. Run a PVD Simulation

python run_PVD_SiC.py --sample_id 153 --lenx 60 --leny 60 --lenz 960 \
                      --gr 287 --TotTime 0.39 --randseed 9117116

2. Analyze the Simulation Output

python analyze_PVD_SiC.py --input_dir results/sample_153/

The analysis includes:
- Growth rate (spline, polyfit, or finite difference methods)
- Surface roughness in microns
- Vacancy types and concentrations (SV, CV, SAV, CAV, XV)

3. Generate FAIR NeXus Output

Open and run Parser_May_2.ipynb to:
- Parse data from surf_height.txt, results.txt, and .xyz files
- Build a NeXus .nxs file embedding simulation config and results
- Conform to FAIRmat schemas: NXmicrostructure_imm_config and NXmicrostructure_imm_results

Note: Although FAIRmat may automatically classify the .nxs file as an "Experiment", it originates from a simulation.

Output Files

File              | Description
----------------- | ----------------------------------------
results.txt       | Growth rate, roughness, and vacancy data
runlog.txt        | Full simulation log
surf_height.txt   | Time-resolved surface height profile
I*.xyz            | Atomic configurations at each time step
*.nxs             | FAIRmat-compliant NeXus output

Citation

If you use this workflow, please cite:
- MulSKIPS: Fisicaro et al., Phys. Rev. Materials 4, 2020
- FAIRmat: Wilkinson et al., Scientific Data 3, 2016

A bibtex.bib file with full references is provided in the repository.

License

This project is released under the MIT License. See the LICENSE file for details.

Acknowledgements

Developed as part of the FAIR data initiative for materials science:
- CNR-IMM@CT (https://www.imm.cnr.it/)
- FAIRmat Project (https://www.fairmat-nfdi.eu/)
