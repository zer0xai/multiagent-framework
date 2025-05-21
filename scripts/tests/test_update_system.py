import os
from scripts.update import update_system


def test_ensure_directories(tmp_path):
    """Testa se os diretórios são criados corretamente"""
    os.chdir(tmp_path)
    update_system.ensure_directories()
    assert os.path.isdir("logs")
    assert os.path.isdir("src/agents")


def test_show_changes(capsys):
    """Verifica a saída do modo dry-run"""
    update_system.show_changes()
    captured = capsys.readouterr()
    assert "SIMULAÇÃO DE ALTERAÇÕES" in captured.out
