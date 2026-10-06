"""Bundled fictional cases; works without a checkout or implicit user policy."""

from contextlib import ExitStack
from importlib.resources import as_file, files

from .config import load_policy
from .models import ScanError
from .preview import ReviewGroup, tr
from .scan import scan_files


def demo_groups(lang: str = "en") -> list[ReviewGroup]:
    assets = files("agentsafe").joinpath("demo_assets")
    specs = [
        (tr(lang, "Before review", "修改前"), tr(lang, "Fictional sensitive domains and authentication fields. Select a finding to highlight its image region.", "虚构的敏感域名与认证字段。点击检测条目，可高亮图片中的对应位置。"), ["dashboard.png", "session.log"]),
        (tr(lang, "After review", "修改后"), tr(lang, "Separately prepared edits, not automatic redaction. A preference cookie still warrants human review.", "预先制作的修改后对照，并非自动打码。普通偏好 Cookie 仍需要人工判断。"), ["dashboard-reviewed.png", "session-reviewed.log"]),
        (tr(lang, "Known limitation", "已知漏检"), tr(lang, "This tiny blurred image contains a configured sensitive domain. On the tested machine OCR misses it: no finding does not mean safe.", "这张小而模糊的图片含有已配置的敏感域名。在已测试机器上 OCR 未能识别：没有命中不代表安全。"), ["small-blurred.png"]),
    ]
    try:
        with ExitStack() as stack:
            policy = load_policy(stack.enter_context(as_file(assets.joinpath("policy.toml"))))
            groups = []
            for title, subtitle, names in specs:
                paths = [str(stack.enter_context(as_file(assets.joinpath(name)))) for name in names]
                report = scan_files(paths, policy, config_loaded=True, capture_previews=True)
                groups.append(ReviewGroup(title, subtitle, report))
            return groups
    except OSError:
        raise ScanError("Bundled demo assets could not be read; reinstall from the local checkout.") from None
