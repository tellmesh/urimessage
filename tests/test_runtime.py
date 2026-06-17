from __future__ import annotations

from urisysedge.runtime import Runtime

import urimessage


def test_alert_send():
    rt = Runtime()
    urimessage.register(rt)
    res = rt.call(
        "message://local/alert/command/send",
        {"text": "hello", "channel": "ops", "severity": "info"},
        {"approved": True},
    )
    assert res["ok"]
    assert res["result"]["delivered"] is True
