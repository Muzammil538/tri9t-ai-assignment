import re
import fitz
import hashlib
import uuid


HEADING_PATTERN = re.compile(
    r"^(\d+(?:\.\d+)*)(?:\.)?\s+(.+)$"
)

class PDFParser:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def parse(self):
        doc = fitz.open(self.pdf_path)

        nodes = []
        stack = []

        current = None

        for page in doc:
            lines = page.get_text().splitlines()

            for line in lines:
                line = line.strip()

                if not line:
                    continue

                heading = HEADING_PATTERN.match(line)
                
                if heading:
                  number = heading.group(1)

                  # Ignore numbered lists like "1 Normal..."
                  if "." not in number and ":" in heading.group(2):
                      heading = None

                if heading:

                    if current:
                        nodes.append(current)

                    number = heading.group(1)
                    title = heading.group(2)

                    parts = number.split(".")
                    level = len(parts)

                    while stack and stack[-1]["level"] >= level:
                        stack.pop()

                    parent = stack[-1]["id"] if stack else None

                    current = {
                        "id": str(uuid.uuid4()),
                        "number": number,
                        "title": title,
                        "level": level,
                        "parent": parent,
                        "content": ""
                    }

                    stack.append(current)

                elif current:
                    current.setdefault("content", "")
                    current["content"] += f"{line.strip()}\n"

        if current:
            nodes.append(current)

        for node in nodes:
            node["hash"] = hashlib.sha256(
                node["content"].encode()
            ).hexdigest()

        return nodes