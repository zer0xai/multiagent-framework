import os
import yaml
from datetime import datetime
from scripts.core.translate import translate


def create_agent(name="example-agent", dry_run=False):
    if dry_run:
        print(f"🆕 Criaria o agente: {name}")
        return

    print(f"🧠 Criando agente '{name}' (exemplo)...")
    create_agent_structure(name)
    update_docker_compose(name, type_="agent")
    update_main_menu(name)
    create_alias(name, type_="agent")
    update_readme("agent", name)
    update_readme_prompt_for_ia("agent", name)
    log_agent_creation(name)


def create_agent_structure(agent_name: str):
    agent_name = agent_name.lower().replace(" ", "-")  # normalize nome
    agent_dir = f"src/agents/{agent_name}"
    src_dir = os.path.join(agent_dir, "src")
    os.makedirs(src_dir, exist_ok=True)

    # Arquivo principal do agente
    agent_file = os.path.join(src_dir, f"{agent_name}-agent.py")
    with open(agent_file, "w") as f:
        # Use title case substituindo "-" por espaço para ficar mais legível
        f.write(f"# {agent_name.replace('-', ' ').title()} Agent\n")

    # Dockerfile do agente
    dockerfile_path = os.path.join(agent_dir, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(
            f"""FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/{agent_name}-agent.py"]
"""
        )

    # Arquivo requirements.txt vazio para dependências futuras
    requirements_path = os.path.join(agent_dir, "requirements.txt")
    with open(requirements_path, "w") as f:
        f.write("# Add your dependencies here\n")


def create_model_structure(model_name: str):
    model_name = model_name.lower().replace(" ", "-")
    model_dir = f"src/models/{model_name}"
    src_dir = os.path.join(model_dir, "src")
    os.makedirs(src_dir, exist_ok=True)

    main_file = os.path.join(src_dir, f"{model_name}-model.py")
    with open(main_file, "w") as f:
        f.write(f"# {model_name.capitalize()} Model\n\nprint('hello_world')\n")

    dockerfile_path = os.path.join(model_dir, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(
            f"""FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "src/{model_name}-model.py"]
"""
        )

    requirements_path = os.path.join(model_dir, "requirements.txt")
    with open(requirements_path, "w") as f:
        f.write("# Add model requirements here\n")

    # Retorno e mensagem indicam sucesso
    print(f"Model structure created at {model_dir}")
    return model_name


def update_docker_compose(name, type_="agent"):
    compose_file = "docker-compose.yaml"

    if os.path.exists(compose_file):
        with open(compose_file, "r") as f:
            compose_data = yaml.safe_load(f)
    else:
        compose_data = {"version": "3", "services": {}}

    services = compose_data.get("services", {})
    service_name = f"{type_}-{name}".replace("_", "-")

    if service_name in services:
        print(f"Serviço '{service_name}' já existe no docker-compose.yaml")
        return

    services[service_name] = {
        "build": {"context": f"./src/{type_}s/{name}", "dockerfile": "Dockerfile"},
        "volumes": [f"./src/{type_}s/{name}:/app"],
        "tty": True,
    }

    compose_data["services"] = services

    with open(compose_file, "w") as f:
        yaml.dump(compose_data, f, sort_keys=False)

    print(f"✅ Serviço '{service_name}' adicionado ao docker-compose.yaml")


def update_main_menu(agent_name: str):
    path = "main.py"
    if not os.path.exists(path):
        print("⚠️  main.py not found. Skipping menu update.")
        return

    with open(path, "r") as f:
        lines = f.readlines()

    pretty_name = agent_name.replace("-", " ").title()
    last_id = 0
    for line in lines:
        if match := __import__("re").search(r'"(\d+)":\s*{', line):
            last_id = max(last_id, int(match.group(1)))

    new_id = last_id + 1
    entry = f'    "{new_id}": {{\n        "name": "{pretty_name}",\n        "dir": "{agent_name}"\n    }},\n'

    updated = []
    inserted = False
    for line in lines:
        if not inserted and line.strip() == "}":
            updated.append(entry)
            inserted = True
        updated.append(line)

    with open(path, "w") as f:
        f.writelines(updated)


def create_alias(name: str, type_: str = "agent"):
    alias_name = f"run-{name}"
    alias_cmd = f"python {type_}s/{name}/src/{name}-{type_}.py"
    alias = f"alias {alias_name}='{alias_cmd}'"
    for shell in ["~/.bashrc", "~/.zshrc"]:
        expanded = os.path.expanduser(shell)
        with open(expanded, "a") as f:
            f.write(f"\n{alias}\n")
    print(translate("alias_added", alias=alias_name))


def update_readme(agent_or_model: str, name: str):
    readme_path = "README.md"
    name_display = name.replace("-", " ").title()
    entry = f"- [{name_display}](./{agent_or_model}s/{name})\n"

    if not os.path.exists(readme_path):
        with open(readme_path, "w") as f:
            f.write("# Projeto Modular de IA\n\n## Componentes\n")

    with open(readme_path, "r+") as f:
        content = f.read()
        if entry not in content:
            f.seek(0, os.SEEK_END)
            f.write(f"\n{entry}")
            print(translate("readme_updated", name=name_display))
        else:
            print(translate("already_registered", name=name_display))


def update_readme_prompt_for_ia(agent_or_model: str, name: str):
    readme_prompt_path = "README-IA.md"
    prompt_block = (
        f"""\n### {name.replace("-", " ").title()} ({agent_or_model}) ###\n"""
    )

    if not os.path.exists(readme_prompt_path):
        with open(readme_prompt_path, "w") as f:
            f.write("# Prompt para Integração com IA\n\n")

    with open(readme_prompt_path, "a") as f:
        f.write(prompt_block)
        print(translate("readme_ia_updated", name=name))


def write_log(message: str):
    os.makedirs("logs", exist_ok=True)
    log_path = "logs/system.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")


def log_entity_creation(entity_type: str, name: str):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "creation.log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a") as log_file:
        log_file.write(f"[{timestamp}] ✅ {entity_type} criado: {name}\n")


def log_agent_creation(agent_name: str):
    log_entity_creation("Agente", agent_name)


def log_model_creation(model_name: str):
    log_entity_creation("Modelo", model_name)


def log_interface_creation(interface_name: str):
    log_entity_creation("Interface", interface_name)
