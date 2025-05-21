# tests/test_create.py
import os
import pytest
from scripts.core.create import create_agent_structure, create_model_structure


@pytest.mark.parametrize("name", ["test-agent", "example-model"])
def test_structure_creation(tmp_path, name):
    os.chdir(tmp_path)
    os.makedirs("src", exist_ok=True)

    if "agent" in name:
        create_agent_structure(name)
        expected_files = [
            f"src/agents/{name}/src/{name}-agent.py",
            f"src/agents/{name}/Dockerfile",
            f"src/agents/{name}/requirements.txt",
        ]
    else:
        create_model_structure(name)
        expected_files = [
            f"src/models/{name}/src/{name}-model.py",
            f"src/models/{name}/Dockerfile",
            f"src/models/{name}/requirements.txt",
        ]

    for file_path in expected_files:
        assert os.path.exists(file_path), f"❌ Missing: {file_path}"
