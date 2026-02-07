import subprocess
from pathlib import Path

def ppt_to_pdf(ppt_path: str, output_dir: str):
    ppt_path = Path(ppt_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_dir),
        str(ppt_path)
    ]

    subprocess.run(cmd, check=True)

    pdf_path = output_dir / (ppt_path.stem + ".pdf")
    return pdf_path


if __name__=="__main__":
    ppt_to_pdf('../pptOriginalData/新中特.pptx','../pptOriginalData')