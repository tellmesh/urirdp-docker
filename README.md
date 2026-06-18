# urirdp-docker

Minimal Docker package for a Linux GUI instance exposed through **RDP** and automated through URI calls:

- `rdp://` — RDP/session/display status
- `kvm://` — high-level screen automation
- `him://` — Human Input Module: mouse and keyboard
- `ocr://` — OCR over screenshots
- `llm://` — mock vision/planning layer for choosing actions

The design keeps transport separate from command semantics:

```text
URL transport:  http://127.0.0.1:8795/uri/call
URI command:    kvm://local/task/command/click-text
RDP access:     127.0.0.1:3389
```

## Run

```bash
docker compose up --build urirdp
```

Then connect by RDP:

```text
host: 127.0.0.1
port: 3389
user: urisys
password: urisys
```

Override credentials with environment variables:

```bash
RDP_USER=adam RDP_PASSWORD='change-me' docker compose up --build urirdp
```

## Call the URI server

Dry-run/mock mode, safe by default:

```bash
curl -X POST http://127.0.0.1:8795/uri/call \
  -H 'Content-Type: application/json' \
  -d '{
    "uri":"kvm://local/task/command/click-text",
    "payload":{"text":"OK"},
    "context":{"approved":true,"dry_run":true}
  }'
```

Real desktop control requires an active RDP session and explicit opt-in:

```bash
URISYS_ALLOW_REAL=1 docker compose up --build urirdp
```

Then call with:

```json
{"context":{"approved":true,"allow_real":true,"display":":10","xauthority":"/home/urisys/.Xauthority"}
```

Automated real-mode smoke test (single container, bootstrap inside urirdp):

```bash
./scripts/test-real-docker.sh
```

Separate **RDP e2e** (two containers: `urirdp` + `rdp-client` with `xfreerdp` + `Xvfb`) — manual or CI only:

```bash
make test-rdp-real
# or:
docker compose -f docker-compose.rdp-e2e.yml up --build --abort-on-container-exit --exit-code-from rdp-client
```

Fast Docker smoke (mock/dry-run only):

```bash
./scripts/test-docker.sh
```

Keep real mode running manually:

```bash
URISYS_ALLOW_REAL=1 docker compose up --build urirdp
docker exec urirdp-gui bash /opt/urirdp/docker/bootstrap-rdp-session.sh
./scripts/call-http.sh   # dry-run by default; edit for allow_real
```

## Flow

```bash
urisys-rdp flow flows/rdp-kvm-smoke.uri.flow.yaml --approve --dry-run
```

Inside Docker this is served by:

```text
urisys-rdp serve --host 0.0.0.0 --port 8795
```

## Why RDP + KVM?

`rdp://` describes the GUI session. `kvm://` performs task-level automation. `kvm://` can call:

```text
kvm://local/monitor/primary/query/screenshot
ocr://local/image/latest/query/text
llm://local/vision/query/analyze
him://local/mouse/command/click
him://local/keyboard/command/type
```

That means the same KVM contract can later target other systems: a local Linux desktop, VM, Windows RDP gateway, VNC backend, browser container, or physical KVM appliance.

## Security

Real input control is disabled by default. The package requires both approval and `allow_real`/`URISYS_ALLOW_REAL=1` before using `xdotool` and `scrot` against the active X session.

## Stack (standalone packs)

```text
tellmesh/
├── urirdpedge/          → urisys-rdp CLI + HTTP (:8795)
├── urirdp/              → rdp:// pack only
├── urikvm/ urihim/ uriocr/ urillm/
├── urishell/ urienv/ uribrowser/
├── `uricore` (`uri_control.edge`)/          → Runtime + shared HTTP transport
└── urirdp-docker/       → Dockerfile, config, flows, markpacts
```

Local tests:

```bash
./scripts/test-local.sh
```

Build from tellmesh root:

```bash
docker build -f urirdp-docker/Dockerfile /path/to/tellmesh
```

## Docs

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/KVM_AUTOMATION.md](docs/KVM_AUTOMATION.md)
- [docs/RDP_USAGE.md](docs/RDP_USAGE.md)
- [docs/MARKPACT.md](docs/MARKPACT.md)

## Ekosystem TellMesh

Orchestrator: **[urisys](https://github.com/tellmesh/urisys)** · Mapa: **[MESH.md](https://github.com/tellmesh/urisys/blob/main/docs/MESH.md)** · Model: **[ECOSYSTEM.md](https://github.com/tellmesh/urisys/blob/main/../docs/ECOSYSTEM.md)**

| Pole | Wartość |
|------|---------|
| **Warstwa** | Docker glue |
| **Obraz** | RDP desktop automation |
| **Zależności** | urirouter, uricore, urirdpedge |

Runtime edge: **`uri_control.edge`** w pakiecie **`uricore`** (legacy `urisysedge` usunięty 2026-06).
Router intencji: **`urirouter`** (`uri_router`) — resolve + HTTP/MQTT delegate.

<!-- end-ecosystem -->
