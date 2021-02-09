#!/usr/bin/env python3
import json
import platform
from os import path


def get_manifest_path() -> str:
    if platform.system() == "Darwin":
        return path.expanduser(
            "~/Library/Application Support/Mozilla/NativeMessagingHosts/witchcraft_host.json"
        )
    elif platform.system() == "Windows":
        raise Exception("Sorry, Windows is not supported")
    else:
        return path.expanduser("~/.mozilla/native-messaging-hosts/witchcraft_host.json")

def get_manifest_content() -> dict:
    return {
        "name": "witchcraft_host",
        "description": "Native host for the Witchcraft userscript manager",
        "path": path.join(path.dirname(path.abspath(__file__)), "witchcraft_host.py"),
        "type": "stdio",
        "allowed_extensions": ["witchcraft@witch.craft"]
    }

def main():
    manifest_path = get_manifest_path()
    manifest_content = get_manifest_content()
    with open(manifest_path, "w") as f:
        f.write(json.dumps(manifest_content, indent="  "))


if __name__ == "__main__":
    main()
