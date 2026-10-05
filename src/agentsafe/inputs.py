"""Bounded regular-file snapshots; no directory walking or URL inputs."""

import os
from pathlib import Path
import stat

from .models import ScanError


def read_snapshot(path: Path, limit: int) -> bytes:
    fd = None
    try:
        # Reject explicit symlinks, including ancestors, before opening. O_NOFOLLOW
        # also closes the final-component race on systems that provide it.
        absolute = path.absolute()
        if any(p.is_symlink() for p in (absolute, *absolute.parents)):
            raise ScanError("Symlink inputs are not supported; select a regular file directly.")
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode):
            raise ScanError("Input must be a regular file, not a directory, pipe or device.")
        if before.st_size > limit:
            raise ScanError("Input exceeds the byte limit; nothing was truncated or inspected.")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        flags |= getattr(os, "O_BINARY", 0)
        fd = os.open(path, flags)
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode) or (before.st_dev, before.st_ino) != (
            opened.st_dev, opened.st_ino
        ):
            raise ScanError("Input changed before it could be read; scan again.")
        with os.fdopen(fd, "rb") as stream:
            fd = None
            data = stream.read(limit + 1)
            after = os.fstat(stream.fileno())
        if len(data) > limit:
            raise ScanError("Input exceeds the byte limit; nothing was truncated or inspected.")
        signature = lambda s: (s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        if signature(before) != signature(opened) or signature(opened) != signature(after):
            raise ScanError("Input changed while being read; scan again.")
        return data
    except FileNotFoundError:
        raise ScanError("File was not found; check the supplied path.") from None
    except (OSError, ValueError):
        raise ScanError("File could not be read as a regular local file; check access and path.") from None
    finally:
        if fd is not None:
            os.close(fd)
