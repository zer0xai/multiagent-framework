import sys
from scripts.core.create import (
    create_model_structure,
    update_docker_compose,
    create_alias,
    update_readme,
    update_readme_prompt_for_ia,
    log_model_creation,
)

from scripts.core.translate import (
    translate,
)


def create_model():
    print(translate("create_model.title"))  # === Model Creator ===

    model_name = (
        input(translate("create_model.prompt_name")).strip().lower().replace(" ", "-")
    )

    try:
        if not model_name:
            print(translate("error.invalid_name"))
            sys.exit(1)

        create_model_structure(model_name)
        update_docker_compose(model_name, type_="model")
        create_alias(model_name)
        update_readme("model", model_name)
        update_readme_prompt_for_ia("model", model_name)
        log_model_creation(model_name)

        print(translate("create_model.success", model_name=model_name))

    except KeyboardInterrupt:
        print(translate("error.user_cancelled"))
    except Exception as e:
        print(translate("error.creation_failed", error=str(e)))


if __name__ == "__main__":
    create_model()
