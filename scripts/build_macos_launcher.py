"""Build the small native development launcher using existing Apple clang."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import sysconfig
import tempfile

if sys.platform != "darwin":
    raise SystemExit("The development app launcher is macOS-only.")
root = Path(__file__).resolve().parents[1]
if Path(sys.prefix).resolve() != (root / ".venv").resolve():
    raise SystemExit("Use this checkout's .venv/bin/python to build the prepared development launcher.")
target = root / "AgentSafe.app/Contents/MacOS/AgentSafe"
target.parent.mkdir(parents=True, exist_ok=True)
# A LaunchServices app should not need permission to read the whole Desktop
# merely to import its development code. Prepare a private snapshot of code and
# installed dependencies, with no source artifacts or runtime downloads.
runtime = Path(tempfile.mkdtemp(prefix="agentsafe-dev-runtime-"))
site = Path(sysconfig.get_path("purelib"))
shutil.copytree(site, runtime, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "agentsafe"))
shutil.copytree(root / "src/agentsafe", runtime / "agentsafe", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
python = str(Path(sys._base_executable).resolve())
subprocess.run([
    "/usr/bin/clang", "-fobjc-arc", "-framework", "AppKit",
    "-DAGENTSAFE_RUNTIME=" + json.dumps(str(runtime)),
    "-DAGENTSAFE_PYTHON=" + json.dumps(python),
    str(root / "scripts/macos_launcher.m"), "-o", str(target),
], check=True, timeout=60)
target.chmod(0o755)
print("Built AgentSafe.app from the prepared environment. Double-click it in Finder.")
