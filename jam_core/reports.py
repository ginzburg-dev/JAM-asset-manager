"""Report metadata persistence and safe rich-text rendering."""

import html
from datetime import datetime
from pathlib import Path

from .constants import ASSET_METADATA_TEMPLATE, REPORT_STYLES
from .storage import read_json, write_json


def metadata_path(path):
    return Path(path).with_suffix(".json")


def new_metadata():
    return {
        "assetName": ASSET_METADATA_TEMPLATE["assetName"],
        "assetType": ASSET_METADATA_TEMPLATE["assetType"],
        "createdTime": ASSET_METADATA_TEMPLATE["createdTime"],
        "messages": [],
    }


def append_message(path, asset_name, message_type, message, hours=0, user="user", now=None):
    """Append a note or report entry to an asset's sidecar metadata file."""
    sidecar_path = metadata_path(path)
    data = read_json(sidecar_path) or new_metadata()
    messages = data.setdefault("messages", [])
    created_time = (now or datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
    data["assetName"] = asset_name
    data["assetType"] = Path(path).suffix.lower().lstrip(".")
    data["createdTime"] = data.get("createdTime") or created_time
    messages.append(
        {
            "type": message_type,
            "message": message,
            "user": user,
            "createdTime": created_time,
            "hours": hours,
        }
    )
    write_json(sidecar_path, data)
    return data


def read_messages(path):
    metadata = read_json(metadata_path(path))
    return metadata.get("messages", []) if isinstance(metadata, dict) else []


def render_history(messages):
    """Render report entries safely for a Qt rich-text widget."""
    blocks = []
    for message in messages:
        message_type = message.get("type", "")
        if message_type not in REPORT_STYLES:
            continue
        label, header_color, body_color = REPORT_STYLES[message_type]
        date = html.escape(str(message.get("createdTime", "")))
        user = html.escape(str(message.get("user", "")))
        hours = html.escape(str(message.get("hours", 0)))
        byline = user if message_type == "note" else "{}&nbsp;&nbsp;&nbsp;{}h".format(user, hours)
        body = "<br>".join(
            html.escape(line) for line in str(message.get("message", "")).splitlines()
        )
        blocks.append(
            '<div style="margin:0 0 8px 0">'
            '<p align="right" style="margin:0;background-color:{header}">'
            "{label}&nbsp;&nbsp;{date}</p>"
            '<p align="right" style="margin:0;font-style:italic;background-color:{header}">'
            "{byline}</p>"
            '<p align="left" style="margin:0;padding:4px;background-color:{body_color}">'
            "{body}</p></div>".format(
                header=header_color,
                label=label,
                date=date,
                byline=byline,
                body_color=body_color,
                body=body,
            )
        )
    return "".join(blocks)
