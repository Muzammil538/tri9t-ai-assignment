from app.parser.pdf_parser import PDFParser

parser = PDFParser("data/ct200_manual.pdf")

nodes = parser.parse()

for node in nodes:
    print(
        node["number"],
        node["title"],
        "Parent:",
        node["parent"]
    )