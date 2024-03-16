# ZNE Quantum Circuit Noise Mitigation
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Overview
Explore noise mitigation in quantum circuits using Zero-Noise Extrapolation (ZNE) techniques. This repository provides tools to mitigate noise in quantum circuits, employing depolarizing noise models, unitary folding methods, and various extrapolation techniques for enhanced fidelity and reliability.



## Usage

### Getting Started

To get started with ZNE Quantum Circuit Noise Mitigation, follow these steps:

### 1. Clone this Repository
Clone this repository to your local machine using the following command:
```bash
git clone https://github.com/albertojromerot/ZNE-Quantum-Circuit-Noise-Mitigation.git
```

### 2. Install dependencies:

Before running the code, ensure that you have Python and pip installed on your system. You can download and install Python from the [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) installed on your system before proceeding with the installation. 

Next, navigate to the cloned repository directory:

```bash
cd ZNE-Quantum-Circuit-Noise-Mitigation
```

Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

This command will install all necessary Python packages specified in the requirements.txt file, including libraries for quantum computing and data analysis.

If you prefer using a virtual environment, you can create and activate one before installing dependencies:

```bash
python -m venv venv     # Create a virtual environment
source venv/bin/activate  # Activate the virtual environment on macOS/Linux
.\venv\Scripts\activate   # Activate the virtual environment on Windows
```

Once the virtual environment is activated, you can proceed to install the dependencies using the pip install -r requirements.txt command as mentioned above.

By following these steps, you'll have the repository cloned to your machine and all required dependencies installed, ready to explore the ZNE techniques for noise mitigation in quantum circuits.



### Detailed Usage Instructions

Explore the functionalities of each component in the repository:

### Noise Model

- **`noise_model.py`**: Implement depolarizing noise models by modifying the `depolarizing_noise_gate` function. Specify the qubit and the probability of error.

```python
# Example usage of depolarizing noise model
from noise_model import depolarizing_noise_gate

# Apply depolarizing noise to qubit 0 with 10% probability
depolarizing_noise_gate(qubit=0, probability=0.1)
```

### Quantum Circuits

- **`quantum_circuits.py`**: Create quantum circuits using the provided functions. Modify the circuits as needed for testing different scenarios.

```python
# Example usage of quantum circuits
from quantum_circuits import create_quantum_circuit

# Create a quantum circuit with 2 qubits
qc = create_quantum_circuit()
```

### Unitary Folding

- **`unitary_folding.py`**: Apply unitary folding to mitigate noise in quantum circuits. Ensure you understand the structure of the circuit and the noise model before applying the folding method.

```python
# Example usage of unitary folding
from unitary_folding import apply_unitary_folding

# Apply unitary folding to mitigate noise in the quantum circuit
apply_unitary_folding(circuit=qc, noise_model=noise_model)
```

### Extrapolation Methods

- **`extrapolation_methods.py`**: Explore different extrapolation methods such as Linear, Polynomial, and Exponential to estimate the zero-noise limit. Implement these methods based on your data and requirements.

```python
# Example usage of extrapolation methods
from extrapolation_methods import linear_extrapolation

# Perform linear extrapolation on the data
extrapolated_value = linear_extrapolation(data)
```

## Comparison

- **`comparison.py`**: Compare mitigated and unmitigated results using appropriate metrics. Visualize the comparison if necessary for better understanding.

```python
# Example usage of comparison
from comparison import compare_results

# Compare mitigated and unmitigated results
comparison_result = compare_results(unmitigated, mitigated)
```

Feel free to explore and experiment with different components to understand the noise mitigation techniques better.



## Documentation
- Detailed explanations of the ZNE technique, noise mitigation methods, and extrapolation techniques are provided within the code files.


## Example Notebooks

Explore how to use the ZNE Quantum Circuit Noise Mitigation library with these example notebooks:

- [Zero-Noise Extrapolation Task](notebooks/Zero_Noise_Extrapolation_(ZNE)_Task.ipynb): This notebook demonstrates how to mitigate noise in quantum circuits using the Zero-Noise Extrapolation (ZNE) technique. It provides a step-by-step guide on implementing depolarizing noise models, applying unitary folding methods, and using various extrapolation techniques to estimate the zero-noise limit. The notebook includes example code for creating a simple noise model, generating quantum circuits, applying unitary folding, extrapolating zero noise, and comparing mitigated and unmitigated results. Additionally, it showcases how to visualize extrapolation curves to gain insights into noise mitigation performance. Users can follow along with the provided examples to understand the principles of ZNE and its application in quantum computing.

Feel free to experiment with these notebooks to understand the functionality of the library better.


## License
This project is licensed under the MIT License, a widely-used open-source license that grants users significant freedoms to use, modify, and distribute the software. By using this repository, you agree to comply with the terms of the license.

### MIT License Overview:
- **Permissions**: Users are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software.
- **Conditions**: The software is provided "as is," without warranty of any kind, express or implied. Users must include the original copyright notice and disclaimer in all copies or substantial portions of the software.
- **Limitations**: The MIT License places minimal restrictions on users, primarily requiring attribution and preserving the license text.

By using this repository, you agree to comply with the terms of the MIT License.

For detailed information about the MIT License, see the [LICENSE](LICENSE) file.



## Contribution

Contributions are welcome! If you'd like to contribute to this project, we appreciate your help in making it better. There are several ways you can contribute:

### Reporting Bugs
If you encounter any bugs or unexpected behavior while using the code, please help us by reporting them. To report a bug:

1. Check the existing issues to see if the bug has already been reported.
2. If not, open a new issue and provide detailed steps to reproduce the bug, along with any relevant information about your environment.
3. Use clear and descriptive titles and descriptions to make it easier for us to understand and address the issue.

### Requesting Features
If you have ideas for new features or improvements to the existing functionality, we'd love to hear from you. To request a feature:

1. Check the existing issues to see if the feature has already been requested.
2. If not, open a new issue and describe the feature you'd like to see added, along with any use cases or benefits it would provide.
3. Use clear and descriptive titles and descriptions to help us understand your suggestion.

### Making Pull Requests
If you'd like to contribute code changes, improvements, or new features directly to the project, please follow these steps:

1. Fork the repository and create a new branch for your changes.
2. Implement your changes, ensuring that they adhere to the project's coding standards and guidelines.
3. Write tests to cover your code changes, if applicable.
4. Ensure that your code is well-documented, with clear explanations of any new functionality or changes.
5. Open a pull request, providing a detailed description of your changes and any related issues or motivations behind the changes.
6. Be responsive to feedback and address any review comments promptly to facilitate the merging of your changes.

### Discussion and Planning
For significant changes or features, we encourage you to discuss them by opening an issue before submitting a pull request. This allows for collaborative discussion and planning, ensuring that proposed changes align with the project's goals and direction.

Thank you for your contributions and support in improving this project!



### Code of Conduct
We are committed to fostering an open and inclusive community where everyone feels welcome to contribute, participate, and collaborate. As such, we expect all contributors, maintainers, and community members to adhere to our Code of Conduct.

Our Code of Conduct outlines the standards of behavior and mutual respect expected from all participants in this project. It applies to all interactions within project spaces, including GitHub discussions, issues, pull requests, and any other project-related communication channels.

#### Key Principles
- **Respect**: Treat others with kindness, empathy, and respect, regardless of their background, identity, or beliefs.
- **Inclusivity**: Create an environment where everyone feels valued, included, and empowered to participate and contribute.
- **Openness**: Foster open and constructive communication, and welcome diverse perspectives and opinions.
- **Collaboration**: Work together collaboratively, listen actively, and be open to feedback and constructive criticism.

#### Unacceptable Behavior
We do not tolerate any form of harassment, discrimination, or disrespectful behavior, including but not limited to:
- Offensive language or imagery
- Personal attacks or insults
- Discrimination based on race, gender, sexual orientation, disability, religion, nationality, or any other protected characteristic
- Intimidation, threats, or bullying
- Unwelcome sexual advances or attention

#### Reporting Violations
If you witness or experience any behavior that violates our Code of Conduct, please report it to the project maintainers immediately. You can report violations by [contacting us directly](alberto.zne.projectmaintainer@gmail.com) or by opening an issue on GitHub.

#### Enforcement
Project maintainers are responsible for enforcing the Code of Conduct and addressing any reported violations promptly and fairly. In cases where violations occur, appropriate actions will be taken, which may include warnings, temporary or permanent bans, or other measures deemed necessary to maintain a positive and inclusive community environment.

By participating in this project, you are expected to adhere to the principles and guidelines outlined in our Code of Conduct. Together, we can create a welcoming and inclusive community where everyone can thrive and contribute to the project's success.



## Authors
  - [Alberto Romero Torres](https://github.com/albertojromerot)
  - LinkedIn: [Alberto Romero Torres](https://www.linkedin.com/in/alberto-romero-torres/)
  - Email: alberto.zne.projectmaintainer@gmail.com

  

## Acknowledgments

This project was inspired by the [Zero-Noise Extrapolation (ZNE)](https://mitiq.readthedocs.io/en/stable/guide/zne.html) documentation provided by Mitiq, a quantum error mitigation library. The concept of ZNE and its applications in noise mitigation techniques greatly influenced the development of this repository.

Additionally, we would like to express our gratitude to the [Quantum Open Source Foundation (QOSF)](https://www.qosf.org) for their contributions to the advancement of quantum computing research and open-source initiatives. Their dedication to fostering collaboration and innovation in the quantum computing community has been instrumental in shaping this project.

We extend our thanks to the individuals and organizations who have shared their knowledge, expertise, and resources, contributing to the growth and development of quantum computing technologies worldwide.

  
