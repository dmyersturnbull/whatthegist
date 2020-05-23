import sys
import re
from pathlib import Path


def fix(path: Path, accent_file: Path, output_path: Path) -> None:
    """
    Reformat my bib file.
    
    * Remove PMC and DOI URLs because they're listed as IDs anyway.
    * Replace accent-like escape characters with their UTF equivalents. I mean, it's 2020.
    * Remove line breaks in the middle of sections.
    * TODO: Remove abstracts.
    * TODO: Auto-remove duplicates
    
    Args:
        path: Path (or str) to the file to correct.
        accent_file: Path (or str) to a tab-delimited file of (escape sequence \t character), with no header.
        output_path: Path (or str) to write to; will overwrite if it exists.
        
    """
    output_path = Path(output_path)
    path = Path(path)
    dct = {
        s.split("\t")[0]: s.split("\t")[1]
        for s in Path(accent_file).read_text(encoding="utf8").splitlines()
    }
    text = path.read_text(encoding="utf8")
    for key, value in dct.items():
        text = text.replace("{" + key + "}", value).replace(key, value)
        text = text.replace("PLoS", "PLOS")
    text = "\n".join(
        [
            s
            for s in text.splitlines()
            if "pubmedcentral.nih.gov" not in s and "dx.doi.org/" not in s
        ]
    )
    pattern = re.compile('( *[a-z]+  *= *")([^"]+)(" *,)')

    def fix(match):
        inner = re.compile(r"[ \n]+").sub(" ", match.group(2))
        return match.group(1) + inner + match.group(3)

    text = pattern.sub(fix, text)
    output_path.write_text(text, encoding="utf8")


if __name__ == "__main__":
    fix(Path(sys.argv[1]), Path("accents.tsv"), Path(str(path) + ".fixed.bib"))
