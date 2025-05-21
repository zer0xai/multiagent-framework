from scripts.core.create import (
    create_agent_structure,
    update_docker_compose,
    update_main_menu,
    create_alias,
    update_readme,
    update_readme_prompt_for_ia,
    log_agent_creation,
)

from scripts.core.translate import (
    translate,
)


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

    create_agent_structure(agent_name)
    update_docker_compose(agent_name, type_="agent")
    update_main_menu(agent_name)
    create_alias(agent_name)
    update_readme("agent", agent_name)
    update_readme_prompt_for_ia("agent", agent_name)
    log_agent_creation(agent_name)

    print(translate("create_agent.success", agent_name=agent_name))


if __name__ == "__main__":
    create_agent()
