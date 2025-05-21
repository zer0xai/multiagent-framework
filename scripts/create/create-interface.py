from scripts.core.create import (
    update_docker_compose,
    update_main_menu,
    create_alias,
    update_readme,
    update_readme_prompt_for_ia,
    log_interface_creation,
)
from scripts.core.translate import translate
import os


def create_interface():
    print(translate("create_interface.title"))  # Ex: "=== Interface Creator ==="
    interface_name = ""

    while not interface_name:
        interface_name = (
            input(translate("create_interface.prompt_name"))
            .strip()
            .lower()
            .replace(" ", "-")
        )
        if not interface_name:
            print(translate("error.invalid_name"))

    print(translate("create_interface.final_name", interface_name=interface_name))

    # Corrigido: evita criação de src/ interna
    base_path = f"src/interfaces/{interface_name}"
    os.makedirs(base_path, exist_ok=True)

    # Cria Dockerfile
    with open(os.path.join(base_path, "Dockerfile"), "w") as f:
        f.write(
            f"FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nCMD [\"python\", \"{interface_name.replace('-', '_')}_interface.py\"]\n"
        )

    # Cria requirements.txt
    with open(os.path.join(base_path, "requirements.txt"), "w") as f:
        f.write("# Add specific dependencies for this interface\n")

    # Cria script principal da interface
    script_name = interface_name.replace("-", "_") + "_interface.py"
    with open(os.path.join(base_path, script_name), "w") as f:
        f.write(
            f'def main():\n    print("Running {interface_name} interface...")\n\n\nif __name__ == "__main__":\n    main()\n'
        )

    # Continuação das etapas padrão
    update_docker_compose(interface_name, type_="interface")
    update_main_menu(interface_name)
    create_alias(interface_name)
    update_readme("interface", interface_name)
    update_readme_prompt_for_ia("interface", interface_name)
    log_interface_creation(interface_name)

    print(translate("create_interface.success", interface_name=interface_name))


if __name__ == "__main__":
    create_interface()
