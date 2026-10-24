# Third-party notices

[中文](THIRD_PARTY_NOTICES.zh-CN.md)

AgentSafe's own code, original geometric icons and fictional fixtures are MIT-licensed. Dependencies retain their own copyrights and license terms. This source distribution does not vendor a Python interpreter, Tesseract executable or OCR model files. Installing dependencies separately is part of the Alpha setup.

Direct runtime dependencies and their upstream licensing sources:

| Dependency | License | Source |
| --- | --- | --- |
| Pillow | MIT-CMU / HPND and notices for bundled components | [Pillow license](https://github.com/python-pillow/Pillow/blob/main/LICENSE) |
| Rich | MIT | [Rich license](https://github.com/Textualize/rich/blob/master/LICENSE) |
| Typer | MIT | [Typer license](https://github.com/fastapi/typer/blob/master/LICENSE) |
| Tesseract (separately installed) | Apache-2.0 | [Tesseract license](https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE) |
| English OCR data (separately installed) | Apache-2.0 | [tessdata license](https://github.com/tesseract-ocr/tessdata/blob/main/LICENSE) |

Pillow supplies the font used to draw fictional sample images. Test reports use synthetic values and reserved example domains. Logos are generated from project-owned geometric SVG/Pillow drawing instructions, without external fonts or icon sets.

Python wheels may contain additional native libraries, and package managers may add other dependencies. Inspect the exact installed distributions and their bundled notices when redistributing binaries. A future standalone installer needs a separate full dependency/license inventory; this file is not that inventory.
