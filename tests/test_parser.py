from app.parser.pdf_parser import PDFParser


def test_pdf_parser():

    parser = PDFParser("data/ct200_manual.pdf")

    nodes = parser.parse()

    assert len(nodes) > 0

    assert nodes[0]["title"] == "Device Overview"