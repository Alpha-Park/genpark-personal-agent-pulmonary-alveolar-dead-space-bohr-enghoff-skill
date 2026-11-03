"""
MCP Server for Pulmonary Alveolar Dead Space (Bohr-Enghoff) Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import PulmonaryAlveolarDeadSpaceClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-pulmonary-alveolar-dead-space-bohr-enghoff-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_dead_space",
                        "description": "Calculate Bohr-Enghoff physiological dead space (V_D/V_T) and alveolar-arterial oxygen gradient.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "paco2_mmhg": {"type": "number", "description": "Arterial partial pressure of CO2 (mmHg)."},
                                "peco2_mixed_expired_mmhg": {"type": "number", "description": "Mixed expired partial pressure of CO2 (mmHg)."},
                                "pao2_arterial_mmhg": {"type": "number", "description": "Arterial partial pressure of O2 (mmHg, optional)."},
                                "fio2_fraction": {"type": "number", "description": "Fraction of inspired O2 (default: 0.21)."},
                                "age_years": {"type": "integer", "description": "Subject age in years (default: 30)."}
                            },
                            "required": ["paco2_mmhg", "peco2_mixed_expired_mmhg"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "evaluate_dead_space":
            client = PulmonaryAlveolarDeadSpaceClient()
            try:
                res = client.evaluate_dead_space(
                    paco2_mmhg=float(args["paco2_mmhg"]),
                    peco2_mixed_expired_mmhg=float(args["peco2_mixed_expired_mmhg"]),
                    pao2_arterial_mmhg=float(args["pao2_arterial_mmhg"]) if "pao2_arterial_mmhg" in args and args["pao2_arterial_mmhg"] is not None else None,
                    fio2_fraction=float(args.get("fio2_fraction", 0.21)),
                    age_years=int(args.get("age_years", 30))
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
