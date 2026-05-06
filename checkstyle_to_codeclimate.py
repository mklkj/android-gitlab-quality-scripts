import hashlib
import json
import os
import sys
import xml.etree.ElementTree as ET

SEVERITY_MAP = {
    "error": "critical",
    "warning": "major",
    "info": "minor",
}

def convert(input_path, output_path):
    tree = ET.parse(input_path)
    project_root = os.getcwd() + os.sep
    issues = []

    for file_elem in tree.findall("file"):
        path = file_elem.get("name", "")
        if path.startswith(project_root):
            path = path[len(project_root):]
        for error in file_elem.findall("error"):
            message = error.get("message", "")
            line = int(error.get("line", "1"))
            source = error.get("source", "")
            severity = SEVERITY_MAP.get(error.get("severity", "warning"), "minor")

            fingerprint = hashlib.md5(
                f"{path}:{source}:{line}".encode()
            ).hexdigest()

            issues.append({
                "type": "issue",
                "check_name": source,
                "description": message,
                "severity": severity,
                "fingerprint": fingerprint,
                "location": {
                    "path": path,
                    "lines": {"begin": line},
                },
            })

    with open(output_path, "w") as f:
        json.dump(issues, f, indent=2)


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
