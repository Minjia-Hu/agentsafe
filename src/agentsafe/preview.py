"""Explicit, self-contained local review pages. Never modify or reread inputs."""

import base64
from dataclasses import dataclass
import hashlib
from html import escape
from importlib.resources import files
from io import BytesIO
import os
from pathlib import Path
import re
import stat
import tempfile
import time
import uuid

from PIL import Image

from .models import FileResult, Finding, Limits, ScanError, ScanResult
from .output import safe_path

MARKER = "agentsafe-local-preview-v1\n"
TTL_SECONDS = 24 * 60 * 60


@dataclass
class ReviewGroup:
    title: str
    subtitle: str
    report: ScanResult


def tr(lang: str, en: str, zh: str) -> str:
    return zh if lang == "zh" else en


def label(finding: Finding, lang: str) -> str:
    if lang != "zh":
        return finding.explanation
    if finding.rule == "sensitive-domain":
        return "邮箱使用了配置为敏感的域名" if finding.explanation.startswith("Email") else "命中已配置的敏感域名"
    return {
        "authorization": "认证字段有值，需要检查是否适合分享",
        "session-cookie": "包含配置为敏感的会话 Cookie",
        "cookie": "普通 Cookie，敏感性需要你判断",
        "email": "可能的邮箱地址，敏感性尚不确定",
    }.get(finding.rule, "需要人工检查的内容")


def _e(value: str) -> str:
    return escape(safe_path(value), quote=True)


def no_readable_text(file: FileResult) -> bool:
    return file.coverage == "inspected" and any(n.startswith("No readable text extracted;") for n in file.notes)


def note_label(note: str, lang: str) -> str:
    if note == "OCR: English, rendered pixels only; small/blurred text may be missed.":
        return tr(lang, note, "OCR：仅识别可见像素中的英文文字；小字或模糊文字可能漏检。")
    return note


def _file_card(file: FileResult, index: str, lang: str) -> str:
    failed = file.coverage != "inspected"
    unreadable = no_readable_text(file)
    level = "ERROR" if failed else "HIGH" if any(f.severity == "HIGH" for f in file.findings) else "WARN" if file.findings else "REVIEW" if unreadable else "CHECKED"
    status = tr(lang, "NO READABLE TEXT", "未识别出文字") if level == "REVIEW" else level
    name = _e(Path(file.path).name)
    entries, boxes = [], []
    dimensions = None
    if file.preview_png is not None and not failed:
        with Image.open(BytesIO(file.preview_png)) as image:
            dimensions = image.size
    for number, finding in enumerate(file.findings, 1):
        finding_id = f"{index}-finding-{number}"
        region = ""
        if finding.box and dimensions:
            b = finding.box
            w, h = dimensions
            if b.x < 0 or b.y < 0 or b.width <= 0 or b.height <= 0 or b.x + b.width > w or b.y + b.height > h:
                raise ScanError("A finding region is outside its image; preview was not generated.")
            boxes.append(f'<rect id="{finding_id}" class="region {finding.severity.lower()}" x="{b.x}" y="{b.y}" width="{b.width}" height="{b.height}" vector-effect="non-scaling-stroke"><title>{number}. {_e(label(finding, lang))}</title></rect>')
            region = f' data-target="{finding_id}"'
        location = tr(lang, "Click to locate in image", "点击定位到图片") if region else tr(lang, f"Line {finding.line}", f"第 {finding.line} 行") if finding.line is not None else tr(lang, "Image region unavailable", "图片定位不可用")
        uncertainty = f'<span class="uncertainty">{tr(lang, "OCR is uncertain. Check the marked region.", "文字识别不确定，请检查框选位置。")}</span>' if finding.uncertain else ""
        if dimensions:
            tag = "button" if region else "div"
            attributes = f' type="button"{region} aria-pressed="false"' if region else ""
            entries.append(f'<{tag} class="finding {finding.severity.lower()}"{attributes}><span class="finding-top"><span class="number">{number:02}</span><span class="pill {finding.severity.lower()}">{finding.severity}</span></span><strong>{_e(label(finding, lang))}</strong><span class="finding-location">{location}</span>{uncertainty}</{tag}>')
        else:
            entries.append(f'<li class="text-finding"><span class="line-number">{location}</span><span class="pill {finding.severity.lower()}">{finding.severity}</span><div class="text-reason"><strong>{_e(label(finding, lang))}</strong>{uncertainty}</div></li>')
    if not entries and not failed and not unreadable:
        entries.append(f'<div class="quiet"><span class="quiet-symbol">—</span><strong>{tr(lang, "No supported rule matched", "未命中已支持的规则")}</strong><p>{tr(lang, "This is not a guarantee that all content is safe to share.", "这不保证其中的全部内容都适合分享。")}</p></div>')
    # Present extraction limitations before findings. Avoid repeating the same
    # no-text warning as a note or showing a reassuring no-match state beside it.
    notes = "".join(f'<p class="note">{_e(note_label(n, lang))}</p>' for n in dict.fromkeys(file.notes) if not n.startswith("No readable text extracted;"))
    limitation = ""
    if unreadable:
        limitation = f'<div class="coverage-note"><strong>{tr(lang, "No readable text — review the image manually", "未识别出文字，需人工检查图片")}</strong><p>{tr(lang, "OCR completed but extracted no readable text. Sensitive content may have been missed; zero findings does not mean safe.", "OCR 已运行，但未提取出可读文字，可能漏掉敏感内容。0 条发现不代表安全。")}</p></div>'
    controls = ""
    if dimensions:
        w, h = dimensions
        encoded = base64.b64encode(file.preview_png).decode("ascii")
        image_label = tr(lang, "Local image with finding regions", "带检测标记的本地图片") if boxes else tr(lang, "Local image for review", "待审阅的本地图片")
        visual = f'<div class="image-wrap"><svg class="image-stage" viewBox="0 0 {w} {h}" role="img" aria-label="{image_label}"><image width="{w}" height="{h}" href="data:image/png;base64,{encoded}"/>{"".join(boxes)}</svg></div>'
        if boxes:
            controls = f'<label class="overlay-toggle"><input class="overlay-control" type="checkbox" checked> {tr(lang, "Show regions", "显示标记框")}</label>'
        heading = tr(lang, "Inspection limits", "检查限制") if unreadable else tr(lang, "What to review", "需要检查什么")
        content = f'<div class="review-grid">{visual}<aside class="findings"><h3>{heading}</h3>{limitation}{"".join(entries)}{notes}</aside></div>'
    else:
        heading = tr(lang, "Inspection incomplete", "检查未完成") if failed else tr(lang, "Text findings · use line numbers to review the original", "文本检测结果 · 按行号检查原文件")
        rows = f'<ul class="text-findings">{"".join(entries)}</ul>' if file.findings else "".join(entries)
        content = f'<div class="text-review"><h3>{heading}</h3><p class="text-review-hint">{tr(lang, "Only masked reasons and line numbers are shown. Raw log content is not saved in this page.", "仅显示隐藏敏感值的问题说明和行号；页面不保存日志原文。")}</p>{rows}{notes}</div>'
    return f'<article class="file-card"><header class="file-heading"><div><span class="pill {level.lower()}">{status}</span><h2>{name}</h2></div>{controls}</header>{content}</article>'


def render_page(groups: list[ReviewGroup], *, lang: str = "en", synthetic: bool = False) -> str:
    if lang not in {"en", "zh"}:
        raise ScanError("Preview language must be en or zh.")
    total = sum(len(f.preview_png or b"") for g in groups for f in g.report.files)
    if total > Limits().preview_bytes:
        raise ScanError("Preview image budget exceeded; select fewer images.")
    css = files("agentsafe").joinpath("ui/preview.css").read_text(encoding="utf-8")
    script = files("agentsafe").joinpath("ui/preview.js").read_text(encoding="utf-8")
    script_hash = base64.b64encode(hashlib.sha256(script.encode("utf-8")).digest()).decode("ascii")
    csp = f"default-src 'none'; img-src data:; style-src 'unsafe-inline'; script-src 'sha256-{script_hash}'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"
    tabs, panels = [], []
    for i, group in enumerate(groups):
        high = sum(f.severity == "HIGH" for item in group.report.files for f in item.findings)
        warn = sum(f.severity == "WARN" for item in group.report.files for f in item.findings)
        incomplete = sum(item.coverage != "inspected" for item in group.report.files)
        unreadable = sum(no_readable_text(item) for item in group.report.files)
        limits_summary = (f' · {unreadable} ' + tr(lang, "OCR review", "张图片需人工检查")) if unreadable else ""
        tabs.append(f'<button id="tab-{i}" class="tab" role="tab" aria-controls="panel-{i}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}" data-panel="panel-{i}">{_e(group.title)}<span>{high} HIGH · {warn} WARN' + (f' · {incomplete} ERROR' if incomplete else '') + limits_summary + '</span></button>')
        cards = "".join(_file_card(f, f"g{i}-f{j}", lang) for j, f in enumerate(group.report.files))
        panels.append(f'<section id="panel-{i}" role="tabpanel" aria-labelledby="tab-{i}"{ " hidden" if i else ""}><div class="section-intro"><p>{_e(group.subtitle)}</p><span>{len(group.report.files)} {tr(lang,"files", "个文件")} · {incomplete} {tr(lang,"incomplete", "未完成")}</span></div>{cards}</section>')
    title = tr(lang, "See it before you share it.", "先看清楚，再分享。")
    subtitle = tr(lang, "Click image findings to locate them; review text findings by line number. Edit the original if needed, then scan again.", "图片条目可点击定位；文本问题按行号查看原件。审阅并修改后，重新扫描。")
    privacy = tr(lang, "LOCAL PREVIEW · Contains visible image content, not redacted. Keep this page private. Original files are unchanged.", "本地预览 · 含图片可见内容，未打码。请勿直接分享此页面，原文件没有被修改。")
    badge = tr(lang, "FICTIONAL DEMO", "虚构素材演示") if synthetic else tr(lang, "LOCAL FILE REVIEW", "本地文件审阅")
    steps = tr(lang, "01  Locate the finding     /     02  Review & edit the original     /     03  Scan again", "01  找到问题位置     /     02  审阅并修改原件     /     03  重新扫描")
    footer = tr(lang, "A completed scan is not a privacy guarantee. No upload or Git push was intercepted. This local file is eligible for cleanup after 24 hours, when another preview is generated; there is no background deletion.", "检查完成不代表隐私保证，也没有拦截上传或 Git 推送。本地页面超过 24 小时后，在下次生成预览时按清理规则处理；没有后台自动删除。")
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="{escape(csp, quote=True)}"><meta name="referrer" content="no-referrer"><meta name="viewport" content="width=device-width, initial-scale=1"><title>AgentSafe · {title}</title><style>{css}</style></head><body><div class="shell"><header class="masthead"><div class="brand"><span class="brand-mark">A</span>AgentSafe<span class="edition">LOCAL REVIEW / 01</span></div><span class="local"><i></i>{tr(lang, "On your device", "仅在本机")}</span></header><main><div class="hero"><div><span class="eyebrow">{badge}</span><h1>{title}</h1><p>{subtitle}</p></div><div class="hero-note"><span>→</span><p>{tr(lang, "A clear location.\nA human decision.", "位置看得见，\n判断由你做。")}</p></div></div><div class="privacy">{privacy}</div><div class="tabs" role="tablist" aria-label="{tr(lang, "Review groups", "审阅分组")}">{"".join(tabs)}</div>{"".join(panels)}<div class="steps">{steps}</div></main><footer><strong>AgentSafe</strong><p>{footer}</p></footer></div><script>{script}</script></body></html>'''


def _inside_repository(path: Path) -> bool:
    return any((p / ".git").exists() for p in (path, *path.parents))


def _cleanup(root: Path, now: float) -> None:
    # Only delete the two known files from old owned sessions. Preserve sessions
    # with added files or an unrecognized marker; never recurse through links.
    for directory in root.iterdir():
        if not re.fullmatch(r"[a-f0-9]{32}", directory.name) or directory.is_symlink() or not directory.is_dir():
            continue
        try:
            if now - directory.stat().st_mtime < TTL_SECONDS:
                continue
            entries = {p.name: p for p in directory.iterdir()}
            if set(entries) != {"index.html", ".owner"} or any(p.is_symlink() or not p.is_file() for p in entries.values()):
                continue
            with entries[".owner"].open("rb") as marker:
                if marker.read(len(MARKER) + 1) != MARKER.encode():
                    continue
            for path in entries.values():
                path.unlink()
            directory.rmdir()
        except OSError:
            continue


def save_preview(groups: list[ReviewGroup], *, lang: str = "en", synthetic: bool = False) -> Path:
    html = render_page(groups, lang=lang, synthetic=synthetic)
    try:
        root = Path(tempfile.gettempdir()).resolve() / f"agentsafe-previews-{os.getuid() if hasattr(os, 'getuid') else 'local'}"
        if _inside_repository(root):
            raise ScanError("Temporary directory is inside a repository; choose an external OS temp directory for previews.")
        root.mkdir(mode=0o700, exist_ok=True)
        metadata = root.lstat()
        if not stat.S_ISDIR(metadata.st_mode) or (hasattr(os, "getuid") and metadata.st_uid != os.getuid()):
            raise ScanError("Preview storage is not an owned regular directory; preview was not saved.")
        root.chmod(0o700)
        _cleanup(root, time.time())
        directory = root / uuid.uuid4().hex
        directory.mkdir(mode=0o700)
        path = directory / "index.html"
        for target, content in ((directory / ".owner", MARKER), (path, html)):
            fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(content)
        return path
    except OSError:
        raise ScanError("Could not save a private local preview; original files were not modified.") from None
