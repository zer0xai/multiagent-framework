from scripts.create.create_agent import create_agent
from scripts.create.create_model import create_model


def dispatch_creation():
    print("O que deseja criar?")
    print("1. Agente")
    print("2. Modelo")

    choice = input("Escolha uma opção: ").strip()

    if choice == "1":
        create_agent()
    elif choice == "2":
        create_model()
    else:
        print("❌ Opção inválida.")
