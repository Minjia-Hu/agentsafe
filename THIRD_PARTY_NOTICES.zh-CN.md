# 第三方声明

[English](THIRD_PARTY_NOTICES.md)

AgentSafe 自身代码、原创几何图标和虚构样本采用 MIT。依赖保留各自版权与条款。本源码发行不内置 Python 解释器、Tesseract 可执行文件或 OCR 模型，Alpha 安装步骤单独安装这些依赖。

直接运行依赖及其上游许可证：

| 依赖 | 许可证 | 来源 |
| --- | --- | --- |
| Pillow | MIT-CMU / HPND 及所带组件声明 | [Pillow](https://github.com/python-pillow/Pillow/blob/main/LICENSE) |
| Rich | MIT | [Rich](https://github.com/Textualize/rich/blob/master/LICENSE) |
| Typer | MIT | [Typer](https://github.com/fastapi/typer/blob/master/LICENSE) |
| Tesseract（单独安装） | Apache-2.0 | [Tesseract](https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE) |
| 英语 OCR 数据（单独安装） | Apache-2.0 | [tessdata](https://github.com/tesseract-ocr/tessdata/blob/main/LICENSE) |

虚构图片使用 Pillow 所带字体绘制，测试采用虚构值和保留示例域名。图标由项目原创的几何 SVG/Pillow 绘图指令生成，不使用外部字体或图标库。

Python wheel 可能包含其他原生库，包管理器也可能引入更多依赖。再分发二进制文件时应检查确切安装的包及其声明。未来独立安装包需要另外完成完整的依赖/许可清单，本文不替代该清单。
