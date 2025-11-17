# ZNE Quantum Circuit Noise Mitigation

A small teaching repository demonstrating Zero-Noise Extrapolation (ZNE) with a
minimal single-qubit simulation. It includes a pure-Python density-matrix noise
model, unitary folding helpers, an example notebook, and a lightweight
experiment harness that exports CSVs for analysis in tools like Excel or Power
BI. This is intentionally compact for education and is not a full-featured ZNE
library like Mitiq.

## Modules
- **noise_model.py** – Implements a standard-library single-qubit density matrix
  and `depolarize_density_matrix(...)` helper for depolarizing channels.
- **unitary_folding.py** – Defines the base gate sequence (`BASE_SEQUENCE`) and
  helpers such as `run_folded_circuit(...)` and `expectation_p0(...)` to build
  folded circuits and read out the probability of measuring `|0⟩`.
- **extrapolation_methods.py** – Provides `linear_extrapolation(...)` and
  diagnostics for estimating the zero-noise intercept from noisy expectation
  samples.
- **notebooks/Zero_Noise_Extrapolation_(ZNE)_Task.ipynb** – A worked example that
  simulates folded circuits, performs linear extrapolation, and renders an SVG
  plot.
- **experiments/run_zne_sweep.py** – CLI harness for sweeping noise
  probabilities/fold factors and exporting results to CSV.

## Dependencies
- Core helpers and tests rely only on the Python standard library and `unittest`.
- The notebook and experiment harness use third-party libraries installed via
  `pip install -r requirements.txt`, including:
  - qiskit
  - numpy
  - scipy
  - matplotlib

## Getting started
```bash
git clone https://github.com/albertojromerot/ZNE-Quantum-Circuit-Noise-Mitigation.git
cd ZNE-Quantum-Circuit-Noise-Mitigation
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
pip install -r requirements.txt
```

### Running tests
```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

### Running the demo notebook
Execute the notebook headlessly and regenerate the SVG chart:
```bash
python notebooks/run_zne_notebook.py
```
This runs `notebooks/Zero_Noise_Extrapolation_(ZNE)_Task.ipynb`, refreshes code
cell outputs, and rewrites `notebooks/zne_results.svg`.

### Running a ZNE sweep and exporting CSV
Generate a CSV suitable for Excel/Power BI/pandas analysis:
```bash
python experiments/run_zne_sweep.py \
    --noise-probs 0.01,0.02,0.05 \
    --fold-factors 1,3,5 \
    --shots 2048 \
    --output results/zne_sweep_example.csv \
    --ideal 1.0
```
This sweeps noise probabilities and fold factors, computes unmitigated and
zero-noise estimates, and writes `results/zne_sweep_example.csv`.

## Intuition
Zero-Noise Extrapolation measures how expectation values degrade as noise is
artificially amplified (via folding). A simple linear fit of
(noise scale, expectation) pairs is extrapolated back to a noise scale of zero;
this intercept approximates the ideal, noise-free outcome and helps quantify how
much mitigation improves over the unmitigated measurement.
Feel free to explore and experiment with different components to understand the noise mitigation techniques better.



## Documentation
- Detailed explanations of the Zero-Noise Extrapolation (ZNE) technique, noise mitigation methods, and extrapolation techniques are provided within the code cells and markdown cells of the Jupyter Notebook "[Zero-Noise Extrapolation Task](notebooks/Zero_Noise_Extrapolation_(ZNE)_Task.ipynb)" available in this repository.

  Users can refer to this notebook for comprehensive explanations and insights into the implementation and workings of the ZNE techniques presented in the repository.


## Example Notebooks

Explore how to use the ZNE Quantum Circuit Noise Mitigation library with these example notebooks:

- [Zero-Noise Extrapolation Task](notebooks/Zero_Noise_Extrapolation_(ZNE)_Task.ipynb): This notebook demonstrates how to mitigate noise in quantum circuits using the Zero-Noise Extrapolation (ZNE) technique. It provides a step-by-step guide on implementing depolarizing noise models, applying unitary folding methods, and using various extrapolation techniques to estimate the zero-noise limit. The notebook includes example code for creating a simple noise model, generating quantum circuits, applying unitary folding, extrapolating zero noise, and comparing mitigated and unmitigated results. Additionally, it showcases how to visualize extrapolation curves to gain insights into noise mitigation performance. Users can follow along with the provided examples to understand the principles of ZNE and its application in quantum computing.

Feel free to experiment with these notebooks to understand the functionality of the library better.

### Running the demo notebook without Jupyter

The bundled ZNE notebook only relies on the Python standard library. To regenerate its outputs and the `zne_results.svg` visualization without launching a Jupyter server, run:

```bash
python notebooks/run_zne_notebook.py
```

The script executes all code cells in-place, captures stdout into the notebook outputs, and refreshes the SVG chart next to the notebook file.


## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
