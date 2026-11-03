# Pulmonary Alveolar Dead Space (Bohr-Enghoff) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Physiological Alveolar Dead Space Fraction ($V_D / V_T$) and Alveolar Gas Exchange Calculator based on the Bohr-Enghoff formulation.

```mermaid
flowchart TD
    A[Arterial PaCO2 & Mixed Expired PECO2] --> B[Compute V_D / V_T = PaCO2 - PECO2 / PaCO2]
    C[Barometric Pressure & FiO2] --> D[Alveolar Gas Equation: PAO2]
    D & E[Arterial PaO2] --> F[Alveolar-Arterial Gradient: P A-a O2]
    B & F --> G[Ventilation-Perfusion Matching Evaluation]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Standard Bohr-Enghoff Formula**: Resolves arterial-to-expired carbon dioxide gradient into non-perfused alveolar fraction.
- **Alveolar Gas Equation**: Age-adjusted physiological shunt and diffusion gradient analysis.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
