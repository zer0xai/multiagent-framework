import os
import subprocess


def list_running_services():
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True
    )
    services = result.stdout.strip().split("\n")
    return [s for s in services if s]


def select_services_to_stop(services):
    print("\n📦 Containers em execução:")
    for idx, service in enumerate(services, 1):
        print(f"{idx}. {service}")
    print("0. Todos")

    selected = input(
        "Digite os números dos containers que deseja parar (separados por vírgula): "
    ).strip()

    if selected == "0":
        return services

    indices = [int(i) for i in selected.split(",") if i.strip().isdigit()]
    selected_services = [services[i - 1] for i in indices if 0 < i <= len(services)]
    return selected_services


def stop_selected_services(selected_services):
    for service in selected_services:
        print(f"🛑 Parando: {service}")
        result = os.system(f"docker stop {service}")
        if result != 0:
            print(f"⚠️ Erro ao parar o container: {service}")


def main():
    services = list_running_services()
    if not services:
        print("ℹ️ Nenhum container em execução.")
        return

    selected = select_services_to_stop(services)
    stop_selected_services(selected)


if __name__ == "__main__":
    main()
