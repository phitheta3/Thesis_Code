# FAIR Data Parser for MulSKIPS PVD Simulations

This directory contains a unified Python parser that automates the execution, analysis, and FAIR data export of Physical Vapor Deposition (PVD) simulations using the MulSKIPS atomistic simulation environment. The parser produces NeXus files compliant with the FAIRmat `NXmicrostructure_imm_config` and `NXmicrostructure_imm_results` schema definitions.

---

## 📦 Installation

1. Clone the full repository:

   ```bash
   git clone https://github.com/phitheta3/Thesis_Code.git
   cd Thesis_Code/cnr-imm.ct/PVD_SiC_Workflow
   ```

2. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download and install the MulSKIPS simulation engine**:

   - GitHub: [https://github.com/MulSKIPS](https://github.com/MulSKIPS)
   - Follow the build instructions provided in the MulSKIPS repository to compile and install the simulation environment.
   - On Apple Silicon (Mac M1/M2), refer to Appendix E of the thesis for a custom Makefile and linking instructions.

Dependencies include:

- `h5py`
- `numpy`
- `nexusformat`
- `pymulskips` (custom module)
- `matplotlib` (optional, for visualization)

---

## ▶️ How to Use

You can run the parser directly:

```bash
python Parser.py --input config.yaml
```

Or open the Jupyter notebook version:

```bash
jupyter notebook Parser_30_04_25.ipynb
```

The parser will:

- Run a MulSKIPS PVD simulation via `run_PVD_SiC.py`
- Analyze the output using `analyze_PVD_SiC.py`
- Extract structured metadata and simulation results
- Generate a `.nxs` NeXus file compatible with FAIRmat

---

## 🔄 Workflow

```
[User Input (YAML)]
        ↓
[Run Simulation (MulSKIPS)]
        ↓
[Analyze Results (growth rate, etc.)]
        ↓
[Extract Metadata + Results]
        ↓
[Write NeXus File (NXmicrostructure_imm_*)]
        ↓
[Publish to NOMAD / Zenodo]
```

---

## 🧬 Metadata Structure

The NeXus file (`SiC_sample_XXX.nxs`) includes:

### NXmicrostructure\_imm\_config

- `simulation_code`: "MulSKIPS"
- `substrate_material`: e.g., "3C-SiC"
- `deposition_method`: "PVD"
- `growth_direction`: [0, 0, 1]
- `parameters`: deposition flux, temperature, time, etc.

### NXmicrostructure\_imm\_results

- `growth_rate`: float (e.g., nm/s)
- `final_thickness`: float (e.g., nm)
- `vacancy_density`: float or array
- `surface_height_profile`: array (optional)
- `trajectory_file`: optional `.xyz` or inlined

📘 Schema references:

- [`NXmicrostructure_imm_config`](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_imm_config.html)
- [`NXmicrostructure_imm_results`](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_imm_results.html)

---

## 📁 Project Structure

```
PVD_SiC_Workflow/
├── run_PVD_SiC.py                # Executes MulSKIPS simulation
├── analyze_PVD_SiC.py            # Post-processes output
├── Parser_30_04_25.ipynb         # Jupyter pipeline version
├── SiC_sample_153.nxs            # Example output in NeXus format
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

---

## 📚 References

This tool is part of the Master's thesis:

> **Filippo Ruberto**\
> *FAIR Data Management of the Results from the MulSKIPS Atomistic Simulation Environment for PVD, CVD, and Laser Annealing*\
> Master in Data Management and Curation – SISSA, 2025

Developed at **CNR-IMM\@CT**

- Supervisor: Ioannis Deretzis
- Area Supervisor: Matteo Biagetti (AREA Science Park)
- Project context: NFFA-DI

### External resources:

- [MulSKIPS GitHub](https://github.com/MulSKIPS)
- [FAIRmat NeXus definitions](https://fairmat-nfdi.github.io/nexus_definitions/)
- [NOMAD Repository](https://nomad-lab.eu)
- [Zenodo](https://zenodo.org)

---

## 🤪 License and Acknowledgments

This workflow is developed for educational and research purposes under FAIR principles.\
Please cite the thesis or contact the author for academic use.

