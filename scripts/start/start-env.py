import os
import subprocess


def stop_all_containers():
    print("🛑 Parando todos os containers existentes...")
    os.system("docker compose down")


def list_services():
    result = subprocess.run(
        ["docker", "compose", "config", "--services"], capture_output=True, text=True
    )
    services = result.stdout.strip().split("\n")
    return services


def select_containers_to_start(services):
    print("\n📦 Serviços disponíveis:")
    for idx, service in enumerate(services, 1):
        print(f"{idx}. {service}")
    print("0. Todos")

    selected = input(
        "Digite os números dos serviços que deseja iniciar (separados por vírgula): "
    ).strip()

    if selected == "0":
        return services

    indices = [int(i) for i in selected.split(",") if i.strip().isdigit()]
    selected_services = [services[i - 1] for i in indices if 0 < i <= len(services)]
    return selected_services


def start_selected_containers(selected_services):
    for service in selected_services:
        print(f"🚀 Iniciando: {service}")
        os.system(f"docker compose up -d {service}")


def main():
    stop_all_containers()
    services = list_services()
    selected = select_containers_to_start(services)
    start_selected_containers(selected)


if __name__ == "__main__":
    main()
