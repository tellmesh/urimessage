# UriPack: urimessage

Self-contained Markpact — definitions, full source, run config. Unpack & run: `urisys markpact run urimessage/urimessage.markpact.md --as service` (writes `.markpact/`).

```yaml markpact:pack
apiVersion: urisys.io/v1
kind: UriPack
metadata:
  id: urimessage-pack
  version: 1.0.0
  language: python
description: Simple alert/message dispatch mock for lab and node.
schemes:
- message
capabilities:
- id: message.alert.send
  uri: message://local/alert/command/send
  kind: command
  operation: message.alert.send
  handler: python://urimessage.handlers:alert_send
  side_effects: true
  approval: required
policy:
  default: deny_mutations_without_approval
runtime:
  default_environment: mock
  supports:
  - mock
  - local
  - docker
```

```yaml markpact:run
modes:
- pack
- service
- flow
- interface
- adapter
default: service
scheme: message
service:
  port: 8790
  wire: POST /uri/call
flow:
  ids: []
adapter:
  wire: POST /uri/call
  events: GET /events
```

```python markpact:module path=urimessage/__init__.py
from __future__ import annotations

from importlib.resources import files

from .routes import register

__all__ = ["register", "manifest_path"]


def manifest_path():
    return files(__package__).joinpath("manifest.yaml")
```

```python markpact:module path=urimessage/handlers.py
from __future__ import annotations

from typing import Any


def alert_send(payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("text") or "")
    channel = str(payload.get("channel") or "alert")
    severity = str(payload.get("severity") or "info")
    return {
        "ok": True,
        "text": text,
        "channel": channel,
        "severity": severity,
        "delivered": bool(text),
        "echo": True,
    }
```

```python markpact:module path=urimessage/routes.py
from __future__ import annotations

from importlib.resources import files

from urisysedge.manifest import register_manifest_file


def register(rt):
    register_manifest_file(rt, files(__package__).joinpath("manifest.yaml"))
```

```markdown markpact:docs
# urimessage

`message://` URI capability pack — alert/message dispatch (mock MVP).

Standalone sibling repo under `tellmesh/urimessage`.
```

