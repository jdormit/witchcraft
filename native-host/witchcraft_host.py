#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import platform
import struct
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from os import path
from typing import Optional


class WitchcraftMessageType(Enum):
    RESOLVE = "resolve"
    CONTENTS = "contents"
    OPEN = "open"


@dataclass
class WitchcraftInput:
    type: WitchcraftMessageType
    filename: str

    @staticmethod
    def from_dict(data: dict) -> WitchcraftInput:
        return WitchcraftInput(
            filename=data["filename"], type=WitchcraftMessageType(data["type"])
        )


@dataclass
class WitchcraftResponse:
    type: WitchcraftMessageType
    filename: str
    contents: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "filename": self.filename,
            "contents": self.contents,
            "error": self.error,
        }


def open_file(filepath: str):
    if platform.system() == "Darwin":  # macOS
        subprocess.call(("open", filepath))
    elif platform.system() == "Windows":  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(("xdg-open", filepath))


def handleMessage(message: WitchcraftInput) -> WitchcraftResponse:
    resolved_path = path.expanduser(message.filename)
    if message.type is WitchcraftMessageType.CONTENTS:
        try:
            with open(resolved_path) as f:
                return WitchcraftResponse(
                    type=WitchcraftMessageType.CONTENTS,
                    filename=resolved_path,
                    contents=f.read(),
                )
        except OSError as e:
            return WitchcraftResponse(
                type=WitchcraftMessageType.CONTENTS,
                filename=message.filename,
                error=str(e),
            )
    elif message.type is WitchcraftMessageType.OPEN:
        open_file(resolved_path)
        return WitchcraftResponse(
            type=WitchcraftMessageType.OPEN, filename=resolved_path
        )
    else:
        return WitchcraftResponse(
            type=WitchcraftMessageType.RESOLVE, filename=resolved_path
        )


def getMessage() -> dict:
    rawLength = sys.stdin.buffer.read(4)
    if len(rawLength) == 0:
        sys.exit(0)
    messageLength = struct.unpack("=I", rawLength)[0]
    message = sys.stdin.buffer.read(messageLength).decode("utf-8")
    return json.loads(message)


def sendMessage(message: WitchcraftResponse) -> None:
    if message.error:
        sys.stderr.write(message.error)
    encoded_content = json.dumps(message.to_dict()).encode("utf-8")
    packed_content = struct.pack(f"{len(encoded_content)}s", encoded_content)
    encoded_length = struct.pack("=I", len(encoded_content))
    sys.stdout.buffer.write(encoded_length)
    sys.stdout.buffer.write(packed_content)
    sys.stdout.flush()


def main() -> None:
    message = getMessage()
    response = handleMessage(WitchcraftInput.from_dict(message))
    sendMessage(response)


if __name__ == "__main__":
    main()
