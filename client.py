"""
Pulmonary Alveolar Dead Space & Gas Exchange Client (Bohr-Enghoff Equation).
Zero-mock pure Python standard library implementation.
Calculates physiological dead space fraction (V_D / V_T), alveolar PO2 (PAO2),
alveolar-arterial oxygen gradient (P(A-a)O2), and ventilation-perfusion mismatch.
"""

import math
from typing import Dict, Any, Optional


class PulmonaryAlveolarDeadSpaceClient:
    """
    Computes Bohr-Enghoff physiological dead space fraction (V_D / V_T) and
    the Alveolar Gas Equation parameters to evaluate gas exchange efficiency.
    """

    def __init__(self):
        pass

    def evaluate_dead_space(
        self,
        paco2_mmhg: float,
        peco2_mixed_expired_mmhg: float,
        pao2_arterial_mmhg: Optional[float] = None,
        fio2_fraction: float = 0.21,
        patm_mmhg: float = 760.0,
        water_vapor_pressure_mmhg: float = 47.0,
        respiratory_exchange_ratio: float = 0.80,
        age_years: Optional[int] = 30
    ) -> Dict[str, Any]:
        """
        Calculates dead space fraction and alveolar-arterial oxygen gradient.
        paco2_mmhg: Arterial partial pressure of CO2 (mmHg).
        peco2_mixed_expired_mmhg: Mixed expired partial pressure of CO2 (mmHg).
        pao2_arterial_mmhg: Arterial partial pressure of O2 (mmHg, optional).
        fio2_fraction: Inspired fraction of O2 (0.21 for room air).
        patm_mmhg: Barometric pressure (default: 760 mmHg).
        water_vapor_pressure_mmhg: Tracheal water vapor pressure at 37 deg C (47 mmHg).
        respiratory_exchange_ratio: RER or RQ (default: 0.80).
        age_years: Patient age in years for normal Aa-gradient estimation.
        """
        if paco2_mmhg <= 0:
            raise ValueError("PaCO2 must be positive.")
        if peco2_mixed_expired_mmhg < 0 or peco2_mixed_expired_mmhg >= paco2_mmhg:
            raise ValueError("Mixed expired PECO2 must be >= 0 and strictly less than PaCO2.")
        if fio2_fraction <= 0 or fio2_fraction > 1.0:
            raise ValueError("FiO2 must be between 0.0 and 1.0.")

        # Bohr-Enghoff Equation: V_D / V_T = (PaCO2 - PECO2) / PaCO2
        vd_vt_ratio = (paco2_mmhg - peco2_mixed_expired_mmhg) / paco2_mmhg

        # Alveolar Gas Equation: PAO2 = FiO2 * (Patm - PH2O) - (PaCO2 / R)
        pao2_alveolar_mmhg = (fio2_fraction * (patm_mmhg - water_vapor_pressure_mmhg)) - (paco2_mmhg / respiratory_exchange_ratio)

        aa_gradient_mmhg = None
        expected_aa_gradient_mmhg = None
        aa_ratio = None

        if pao2_arterial_mmhg is not None and pao2_arterial_mmhg > 0:
            aa_gradient_mmhg = pao2_alveolar_mmhg - pao2_arterial_mmhg
            if pao2_alveolar_mmhg > 0:
                aa_ratio = pao2_arterial_mmhg / pao2_alveolar_mmhg
            if age_years is not None and age_years > 0:
                # Standard clinical age-adjusted normal A-a gradient formula: (Age / 4) + 4
                expected_aa_gradient_mmhg = (age_years / 4.0) + 4.0

        # Physiological evaluation
        # Normal resting V_D / V_T is 0.20 - 0.35 in healthy adults.
        # During exercise, recruitment drops it < 0.20.
        # In pulmonary embolism, COPD, acute ARDS, it elevates > 0.40.
        if vd_vt_ratio <= 0.20:
            classification = "Hyper-Efficient Gas Exchange / Exercise Recruitment"
            clinical_status = "Optimal pulmonary capillary perfusion with minimal alveolar dead space."
        elif vd_vt_ratio <= 0.35:
            classification = "Normal Physiological Dead Space"
            clinical_status = "Standard ventilation-perfusion matching at rest (V_D/V_T within 0.20 - 0.35)."
        elif vd_vt_ratio <= 0.50:
            classification = "Moderate Ventilation-Perfusion Mismatch / Wasted Ventilation"
            clinical_status = "Elevated alveolar dead space. Portions of ventilated alveoli lack adequate pulmonary capillary perfusion."
        else:
            classification = "Severe Alveolar Dead Space Expansion"
            clinical_status = "Critical dead space ventilation fraction (>0.50). High risk of pulmonary vascular obstruction or emphysema."

        return {
            "status": "success",
            "vd_vt_ratio": round(vd_vt_ratio, 3),
            "dead_space_percentage": round(vd_vt_ratio * 100.0, 1),
            "pao2_alveolar_mmhg": round(pao2_alveolar_mmhg, 1),
            "pa_a_gradient_mmhg": round(aa_gradient_mmhg, 1) if aa_gradient_mmhg is not None else None,
            "expected_normal_gradient_mmhg": round(expected_aa_gradient_mmhg, 1) if expected_aa_gradient_mmhg is not None else None,
            "a_a_ratio": round(aa_ratio, 3) if aa_ratio is not None else None,
            "evaluation": {
                "classification": classification,
                "clinical_status": clinical_status,
                "paco2_mmhg": paco2_mmhg,
                "peco2_mmhg": peco2_mixed_expired_mmhg
            }
        }
