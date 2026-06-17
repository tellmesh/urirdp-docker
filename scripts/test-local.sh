#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
TELLMESH="$(cd .. && pwd)"
export PYTHONPATH="$TELLMESH:$TELLMESH/urisysedge:$TELLMESH/urioperators:$TELLMESH/urirdp:$TELLMESH/urirdpedge:$TELLMESH/urikvm:$TELLMESH/urihim:$TELLMESH/uriocr:$TELLMESH/urillm:$TELLMESH/urishell:$TELLMESH/uribrowser"
python3 -m pytest tests -q
urisys-rdp --config config/rdp-kvm-profile.json --events data/events.jsonl flow flows/rdp-kvm-smoke.uri.flow.yaml --approve --dry-run >/tmp/urirdp-flow.json
python3 -m json.tool /tmp/urirdp-flow.json >/dev/null
echo "local tests passed"
