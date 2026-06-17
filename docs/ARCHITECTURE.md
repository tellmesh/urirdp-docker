# Architecture — urirdp-docker

```text
RDP client (:3389)
  → XRDP + XFCE in container
  → X11 display (usually :10)

URI client
  → POST /uri/call :8795
  → urirdpedge (urisys-rdp)
  → urisysedge.Runtime + urisysedge.http.serve
  → standalone packs:
       urirdp   (rdp://)
       urikvm   (kvm://)
       urihim   (him://)
       uriocr   (ocr://)
       urillm   (llm://)
       urishell (shell://)
       urienv   (env://)
       uribrowser + lab_browser aliases (browser://)
  → X11 tools: xdotool, scrot, tesseract
```

`URL` is transport. `URI` is command identity.

Example:

```text
POST http://127.0.0.1:8795/uri/call
{
  "uri": "kvm://local/task/command/click-text",
  "payload": {"text": "OK"},
  "context": {"approved": true}
}
```

Pipeline inside `kvm://.../click-text`:

```text
kvm://.../monitor/primary/query/screenshot
ocr://.../image/latest/query/text
llm://.../vision/query/analyze
him://.../mouse/command/click
```

## Related repos

| Repo | Role |
|------|------|
| `urirdpedge` | compose + serve |
| `urirdp` | `rdp://` only |
| `urisysedge` | shared runtime |
| `uricore` | optional routing engine under Runtime |
