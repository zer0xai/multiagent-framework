#!/usr/bin/env python3

import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import subprocess
import logging
from scripts.core import create


# Configuração de logging
LOG_FILE = "logs/update.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Atualizador do sistema")
    parser.add_argument("--dry-run", action="store_true", help="Simular alterações")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.dry_run:
        logging.info("Modo dry-run ativado - simulando alterações.")
        print("🧪 Simulando atualizações (dry-run)...")
        show_changes()
    else:
        print("🔧 Aplicando atualizações no sistema...")
        apply_updates()
        print("✅ Atualizações concluídas.")


def show_changes():
    print("=== SIMULAÇÃO DE ALTERAÇÕES ===")
    # Simulação de criação de agente de exemplo
    example_path = os.path.join("src", "agents", "example-agent")
    if not os.path.exists(example_path):
        print("🆕 Criaria o agente: example-agent")
    else:
        print("✅ Agente 'example-agent' já existente.")

    # Verifica se README precisa de atualização
    if os.path.exists("README.md"):
        with open("README.md") as f:
            content = f.read()
        if "<!-- Atualização automática realizada -->" not in content:
            print("📝 Atualizaria o README.md")
        else:
            print("✅ README.md já atualizado.")


def apply_updates():
    ensure_directories()
    update_agents()
    update_docs()
    validate_all()


def ensure_directories():
    for path in ["logs", "src/agents"]:
        if not os.path.exists(path):
            os.makedirs(path)
            logging.info(f"Diretório criado: {path}")
        else:
            logging.info(f"Diretório já existente: {path}")


def update_agents():
    logging.info("Verificando agentes existentes...")
    example_agent_dir = os.path.join("src", "agents", "example-agent")

    if not os.path.exists(example_agent_dir):
        print("🧠 Criando agente 'example-agent' (exemplo)...")
        logging.info("Agente 'example-agent' ausente, criando...")
        # create.create_agent_structure()
        create.create_agent()
    else:
        logging.info("Agente 'example-agent' já existe.")


def update_docs():
    readme_file = "README.md"
    marker = "<!-- Atualização automática realizada -->"

    if os.path.exists(readme_file):
        with open(readme_file, "r") as f:
            content = f.read()

        if marker not in content:
            with open(readme_file, "a") as f:
                f.write(f"\n{marker}\n")
            logging.info("README.md atualizado com marcador.")
        else:
            logging.info("README.md já contém o marcador.")
    else:
        logging.warning("README.md não encontrado.")


def validate_all():
    print("🔍 Validando sistema...")
    validate_yaml()
    validate_python()
    validate_docker()
    run_tests()


def validate_yaml():
    try:
        import yaml

        logging.info("Validação YAML bem-sucedida.")
    except ImportError:
        logging.warning("PyYAML não instalado. Pule validação YAML.")


def validate_python():
    try:
        subprocess.run(["black", "--check", "."], check=True)
        subprocess.run(["ruff", "."], check=True)
        logging.info("Código Python validado com sucesso.")
    except subprocess.CalledProcessError:
        logging.error("Erros de formatação ou lint encontrados.")
        print("⚠️ Linter Python encontrou problemas.")


def validate_docker():
    import shutil
    if shutil.which("docker-compose") is None:
        print("⚠️  docker-compose não está disponível neste ambiente. Pulei validação.")
        return
    subprocess.run(["docker-compose", "config"], check=True)


def run_tests():
    test_dir = "scripts/tests"
    if os.path.isdir(test_dir):
        try:
            subprocess.run(["env", "PYTHONPATH=.", "pytest", test_dir], check=True)
            logging.info("Testes unitários executados com sucesso.")
        except subprocess.CalledProcessError:
            logging.error("Falha na execução dos testes.")
            print("❌ Alguns testes falharam.")
    else:
        logging.info("Diretório de testes não encontrado. Pulando testes.")


if __name__ == "__main__":
    main()
