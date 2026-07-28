"""Report metadata persistence and safe rich-text rendering."""

import getpass
import html
from datetime import datetime
from pathlib import Path

from .constants import REPORT_STYLES
from .metadata import metadata_path as metadata_path
from .metadata import new_metadata as new_metadata
from .metadata import read_metadata, update_metadata


def append_message(path, asset_name, message_type, message, hours=0, user=None, now=None):
    """Append a note or report entry to an asset's sidecar metadata file."""
    created_time = (now or datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
    message_user = user or getpass.getuser()

    def add_message(data):
        data = data or new_metadata()
        messages = data.setdefault("messages", [])
        data["assetName"] = asset_name
        data["assetType"] = Path(path).suffix.lower().lstrip(".")
        data["createdTime"] = data.get("createdTime") or created_time
        messages.append(
            {
                "type": message_type,
                "message": message,
                "user": message_user,
                "createdTime": created_time,
                "hours": hours,
            }
        )
        return data

    return update_metadata(path, add_message)


def read_messages(path):
    metadata = read_metadata(path)
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
