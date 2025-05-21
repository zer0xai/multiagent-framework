#!/bin/bash

set -e

echo "🛠️  Iniciando Bootstrap..."

# Criar diretórios principais
mkdir -p src/{agents,models,interfaces,core}
mkdir -p scripts/{create,delete,start,update,tests,core}
mkdir -p locales logs

# Criar arquivos __init__.py para facilitar imports
touch scripts/__init__.py
touch scripts/core/__init__.py

# Criar Dockerfile.base
cat <<EOF > Dockerfile.base
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["tail", "-f", "/dev/null"]
EOF

# Criar requirements.txt
cat <<EOF > requirements.txt
# Dependências padrão do ambiente base
pytest
pyyaml
docker
black
ruff
EOF

# Criar docker-compose.yaml
cat <<EOF > docker-compose.yaml
services:
  python-base:
    build:
      context: .
      dockerfile: Dockerfile.base
    volumes:
      - .:/app
    env_file:
      - .env
    tty: true
EOF

# Criar .env e .env.example
echo "PYTHON_ENV=development
LANGUAGE=en" > .env
cp .env .env.example

# Criar main.py
cat <<EOF > main.py
def main():
    print("Welcome to your Modular AI System!")

if __name__ == "__main__":
    main()
EOF

# Criar README.md
cat <<EOF > README.md
# Modular AI Automation System

## Como começar

1. Configure seu ambiente:

\`\`\`bash
source ~/.bashrc  # ou ~/.zshrc
\`\`\`

2. Inicie o ambiente:

\`\`\`bash
start-env
\`\`\`

3. Crie um agente:

\`\`\`bash
create-agent video-editor
\`\`\`

## Estrutura de Pastas

- \`src/\`: Código-fonte (agentes, modelos, interfaces, núcleo)
- \`scripts/\`: Scripts de manutenção
- \`locales/\`: Mensagens traduzidas
- \`logs/\`: Registro de atualizações
EOF

# Corrigir automaticamente scripts/core/create.py para importar 'translate'
CREATE_CORE_PATH="scripts/core/create.py"
if [ -f "$CREATE_CORE_PATH" ]; then
  if ! grep -q "from scripts.core.translate import translate" "$CREATE_CORE_PATH"; then
    echo "Corrigindo importação de 'translate' em $CREATE_CORE_PATH..."
    sed -i '1s/^/from scripts.core.translate import translate\n/' "$CREATE_CORE_PATH"
  fi
fi

# Criar .gitignore padrão
cat <<EOF > .gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.env.*
.venv/
venv/
build/
dist/
*.egg-info/
.DS_Store
.idea/
.vscode/
EOF

# Criar .dockerignore padrão
cat <<EOF > .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.git
.gitignore
.env
.env.*
venv
build
dist
*.egg-info
.DS_Store
.idea
.vscode
EOF

# Função para adicionar alias se não existir
add_alias_if_not_exists() {
  local alias_line="$1"
  local rc_file="$2"
  if ! grep -Fxq "$alias_line" "$rc_file" 2>/dev/null; then
    echo "$alias_line" >> "$rc_file"
    echo "Adicionado alias em $rc_file: $alias_line"
  else
    echo "Alias já existe em $rc_file: $alias_line"
  fi
}

# Lista de aliases
ALIASES=(
  "alias start-env='docker compose up --build -d'"
  "alias update-system='docker compose exec python-base python scripts/update/update_system.py'"
  "alias create-agent='docker compose exec python-base python scripts/create/create_agent.py'"
  "alias create-model='docker compose exec python-base python scripts/create/create_model.py'"
  "alias create-interface='docker compose exec python-base python scripts/create/create_interface.py'"
  "alias format-code='docker compose exec python-base black .'"
)

# Adicionar aliases ao ~/.bashrc e ~/.zshrc
for rc in ~/.bashrc ~/.zshrc; do
  [ -f "$rc" ] || continue
  for alias_line in "${ALIASES[@]}"; do
    add_alias_if_not_exists "$alias_line" "$rc"
  done
done

# Recarregar arquivos de configuração do shell
if [ -f ~/.bashrc ]; then
  source ~/.bashrc
fi
if [ -f ~/.zshrc ]; then
  source ~/.zshrc
fi

echo "✅ Bootstrap finalizado com sucesso!"
