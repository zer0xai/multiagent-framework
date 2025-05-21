from scripts.core.create import (
    create_agent_structure,
    update_docker_compose,
    update_main_menu,
    create_alias,
    update_readme,
    update_readme_prompt_for_ia,
    log_agent_creation,
)
from scripts.core.translate import translate
import os


def create_agent():
    print(translate("create_agent.title"))  # Ex: "=== Agent Creator ==="
    agent_name = ""

    while not agent_name:
        agent_name = (
            input(translate("create_agent.prompt_name"))
            .strip()
            .lower()
            .replace(" ", "-")
        )
        if not agent_name:
            print(translate("error.invalid_name"))

    print(translate("create_agent.final_name", agent_name=agent_name))

    # Corrigido: evita criação de src/ interna
    base_path = f"src/agents/{agent_name}"
    os.makedirs(base_path, exist_ok=True)

    # Cria Dockerfile
    with open(os.path.join(base_path, "Dockerfile"), "w") as f:
        f.write(f"FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nCMD [\"python\", \"{agent_name.replace('-', '_')}_agent.py\"]\n")

    # Cria requirements.txt
    with open(os.path.join(base_path, "requirements.txt"), "w") as f:
        f.write("# Add specific dependencies for this agent\n")

    # Cria o script principal do agente
    script_name = agent_name.replace("-", "_") + "_agent.py"
    with open(os.path.join(base_path, script_name), "w") as f:
        f.write(f'def main():\n    print("Running {agent_name} agent...")\n\n\nif __name__ == "__main__":\n    main()\n')

    # Continuação das etapas padrão
    update_docker_compose(agent_name, type_="agent")
    update_main_menu(agent_name)
    create_alias(agent_name)
    update_readme("agent", agent_name)
    update_readme_prompt_for_ia("agent", agent_name)
    log_agent_creation(agent_name)

    print(translate("create_agent.success", agent_name=agent_name))


if __name__ == "__main__":
    create_agent()
