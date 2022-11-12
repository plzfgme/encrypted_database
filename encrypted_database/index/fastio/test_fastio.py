import os

import pytest
from rocksdict import Rdict

from . import FASTIOClientPart, FASTIOServerPart, Opterator


def test_fastio(tmp_path_factory: pytest.TempPathFactory):
    dir = tmp_path_factory.mktemp("data")
    client_dict = Rdict(str(dir / "client_dict"))
    Sigma = client_dict.create_column_family("Sigma")
    server_dict = Rdict(str(dir / "server_dict"))
    T_e = server_dict.create_column_family("T_e")
    T_c = server_dict.create_column_family("T_c")

    k_s = os.urandom(16)
    client = FASTIOClientPart(Sigma, k_s)
    server = FASTIOServerPart(T_e, T_c)

    u, e = client.update_client_part(b"111", b"hello", Opterator.ADD)
    server.update_server_part(u, e)

    scp = client.search_client_part(b"hello")
    assert scp is not None
    t_w, k_w, c = scp
    result = server.search_server_part(t_w, k_w, c)
    assert result == {b"111"}

    scp = client.search_client_part(b"hello")
    assert scp is not None
    t_w, k_w, c = scp
    result = server.search_server_part(t_w, k_w, c)
    assert result == {b"111"}

    scp = client.search_client_part(b"warn")
    assert scp is None

    client_dict.close()
    Sigma.close()
    server_dict.close()
    T_e.close()
    T_c.close()

    client_dict = Rdict(str(dir / "client_dict"))
    Sigma = client_dict.get_column_family("Sigma")
    server_dict = Rdict(str(dir / "server_dict"))
    T_e = server_dict.get_column_family("T_e")
    T_c = server_dict.get_column_family("T_c")

    client = FASTIOClientPart(Sigma, k_s)
    server = FASTIOServerPart(T_e, T_c)

    scp = client.search_client_part(b"hello")
    assert scp is not None
    t_w, k_w, c = scp
    result = server.search_server_part(t_w, k_w, c)
    assert result == {b"111"}

    scp = client.search_client_part(b"hello")
    assert scp is not None
    t_w, k_w, c = scp
    result = server.search_server_part(t_w, k_w, c)
    assert result == {b"111"}

    scp = client.search_client_part(b"warn")
    assert scp is None

    u, e = client.update_client_part(b"111", b"hello", Opterator.DEL)
    server.update_server_part(u, e)

    scp = client.search_client_part(b"hello")
    assert scp is not None
    t_w, k_w, c = scp
    result = server.search_server_part(t_w, k_w, c)
    assert result == set()
