import socket

import pytest


@pytest.fixture(autouse=True)
def no_python_network(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Python network access is forbidden during scans/tests")

    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(socket.socket, "connect", forbidden)
