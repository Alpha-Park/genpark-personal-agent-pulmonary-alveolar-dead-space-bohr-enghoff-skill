"""
Example usage of Pulmonary Alveolar Dead Space (Bohr-Enghoff) Skill.
Demonstrates normal physiological dead space vs exercise perfusion vs severe pulmonary mismatch.
"""

import json
from client import PulmonaryAlveolarDeadSpaceClient


def main():
    print("=== Testing Pulmonary Alveolar Dead Space (Bohr-Enghoff) Skill ===")
    client = PulmonaryAlveolarDeadSpaceClient()

    # 1. Normal healthy resting adult (PaCO2=40, PECO2=28, PaO2=95, room air FiO2=0.21, Age=32)
    res_normal = client.evaluate_dead_space(
        paco2_mmhg=40.0,
        peco2_mixed_expired_mmhg=28.0,
        pao2_arterial_mmhg=95.0,
        fio2_fraction=0.21,
        age_years=32
    )
    print("\n[Case 1: Normal Healthy Adult at Rest]")
    print(json.dumps(res_normal, indent=2))

    # 2. Vigorous aerobic exercise (capillary recruitment drops V_D / V_T < 0.20)
    res_exercise = client.evaluate_dead_space(
        paco2_mmhg=38.0,
        peco2_mixed_expired_mmhg=32.0,
        pao2_arterial_mmhg=98.0,
        fio2_fraction=0.21,
        age_years=25
    )
    print("\n[Case 2: Aerobic Exercise Capillary Recruitment]")
    print(json.dumps(res_exercise, indent=2))

    # 3. Pathological alveolar dead space expansion (PaCO2=46, PECO2=18, severe mismatch / wasted ventilation)
    res_impaired = client.evaluate_dead_space(
        paco2_mmhg=46.0,
        peco2_mixed_expired_mmhg=18.0,
        pao2_arterial_mmhg=62.0,
        fio2_fraction=0.21,
        age_years=60
    )
    print("\n[Case 3: Pathological Dead Space Expansion]")
    print(json.dumps(res_impaired, indent=2))

    # Assertions
    assert res_normal["vd_vt_ratio"] == 0.30
    assert res_exercise["vd_vt_ratio"] < 0.20
    assert res_impaired["vd_vt_ratio"] > 0.50
    print("\n[SUCCESS] All Pulmonary Dead Space test cases passed!")


if __name__ == "__main__":
    main()
