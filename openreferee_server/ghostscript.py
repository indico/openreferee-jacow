import subprocess
import sys

gs = "gswin32c" if (sys.platform == "win32") else "gs"

"""
The PDF language, unlike the PostScript language, inherently requires random access to the file.
If you provide PDF to standard input using the special filename '-', Ghostscript
will copy it to a temporary file before interpreting the PDF.
https://www.ghostscript.com/doc/current/Use.htm
"""


def run_file(args):
    return subprocess.check_output([gs, *args], stderr=subprocess.STDOUT)
