---
name: genpark-personal-agent-pulmonary-alveolar-dead-space-bohr-enghoff-skill
description: Bohr-Enghoff Alveolar Dead Space Fraction (V_D / V_T) and physiological ventilation-perfusion mismatch analyzer. Calculates dead space ventilation and alveolar-arterial oxygen gradient.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - pulmonary
  - respiratory
  - dead-space
  - gas-exchange
  - openclaw
  - genpark
  - mcp
---

# Pulmonary Alveolar Dead Space (Bohr-Enghoff) Skill

## Overview
This skill computes the fraction of tidal volume that does not participate in pulmonary gas exchange:
- **Bohr-Enghoff Dead Space Fraction ($V_D / V_T$)**: Measures alveolar regions ventilated but unperfused. Normal resting baseline is 0.20 to 0.35.
- **Exercise Capillary Recruitment**: With physical exertion, increased pulmonary perfusion recruits apical capillaries, reducing $V_D / V_T$ to below 0.20.
- **Alveolar Gas Equation & A-a Gradient**: Derives the expected and actual alveolar-arterial gradient to detect diffusion blocks and shunting.

## Mathematical Formulation
1. **Bohr-Enghoff Equation**:
   $$\frac{V_D}{V_T} = \frac{\text{PaCO}_2 - \text{PECO}_2}{\text{PaCO}_2}$$
2. **Alveolar Gas Equation**:
   $$P_A\text{O}_2 = F_i\text{O}_2 \times (P_{\text{atm}} - P_{H_2O}) - \frac{\text{PaCO}_2}{R}$$
3. **Alveolar-Arterial Gradient**:
   $$P(A-a)\text{O}_2 = P_A\text{O}_2 - \text{PaO}_2$$
4. **Age-Adjusted Normal A-a Gradient**:
   $$\text{Expected } P(A-a)\text{O}_2 = \frac{\text{Age}}{4} + 4$$

## Usage
```python
from client import PulmonaryAlveolarDeadSpaceClient

client = PulmonaryAlveolarDeadSpaceClient()
res = client.evaluate_dead_space(
    paco2_mmhg=40.0,
    peco2_mixed_expired_mmhg=28.0,
    pao2_arterial_mmhg=95.0
)
print(res["evaluation"]["classification"])
```
