from scripts.core.create import (
    update_docker_compose,
    update_main_menu,
    create_alias,
    update_readme,
    update_readme_prompt_for_ia,
    log_model_creation,
)
from scripts.core.translate import translate
import os


def create_model():
    print(translate("create_model.title"))  # Ex: "=== Model Creator ==="
    model_name = ""

    while not model_name:
        model_name = (
            input(translate("create_model.prompt_name"))
            .strip()
            .lower()
            .replace(" ", "-")
        )
        if not model_name:
            print(translate("error.invalid_name"))

    print(translate("create_model.final_name", model_name=model_name))

    # Corrigido: evitar src/ desnecessária
    base_path = f"src/models/{model_name}"
    os.makedirs(base_path, exist_ok=True)

    # Cria Dockerfile
    with open(os.path.join(base_path, "Dockerfile"), "w") as f:
        f.write(
            f"FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nCMD [\"python\", \"{model_name.replace('-', '_')}_model.py\"]\n"
        )

    # Cria requirements.txt
    with open(os.path.join(base_path, "requirements.txt"), "w") as f:
        f.write("# Add specific dependencies for this model\n")

    # Cria script principal do modelo
    script_name = model_name.replace("-", "_") + "_model.py"
    with open(os.path.join(base_path, script_name), "w") as f:
        f.write(
            f'def main():\n    print("Running {model_name} model...")\n\n\nif __name__ == "__main__":\n    main()\n'
        )

    # Continuação das etapas padrão
    update_docker_compose(model_name, type_="model")
    update_main_menu(model_name)
    create_alias(model_name)
    update_readme("model", model_name)
    update_readme_prompt_for_ia("model", model_name)
    log_model_creation(model_name)

    print(translate("create_model.success", model_name=model_name))


if __name__ == "__main__":
    create_model()
