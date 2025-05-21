import os
import json

_translation_cache = {}

# Caminho absoluto da pasta raiz do projeto dentro do container (onde está a pasta locales)
BASE_DIR = "/app"  # Ajuste aqui conforme o root do seu projeto no container


def translate(key: str, **kwargs) -> str:
    lang = os.environ.get("LANGUAGE", "en")

    if lang not in _translation_cache:
        try:
            locale_path = os.path.join(BASE_DIR, "locales", f"{lang}.json")
            with open(locale_path, "r", encoding="utf-8") as f:
                _translation_cache[lang] = json.load(f)
        except FileNotFoundError:
            _translation_cache[lang] = {}

    message = (
        _translation_cache[lang].get(key)
        or _translation_cache.get("en", {}).get(key)
        or key
    )
    return message.format(**kwargs)


def t(key: str, **kwargs) -> str:
    """
    Traduz a chave para o idioma definido pela variável de ambiente LANGUAGE.
    """
    lang = os.environ.get("LANGUAGE", "en")

    if lang not in _translation_cache:
        try:
            locale_path = os.path.join(BASE_DIR, "locales", f"{lang}.json")
            with open(locale_path, "r", encoding="utf-8") as f:
                _translation_cache[lang] = json.load(f)
        except FileNotFoundError:
            _translation_cache[lang] = {}

    message = (
        _translation_cache[lang].get(key)
        or _translation_cache.get("en", {}).get(key)
        or key
    )

    return message.format(**kwargs)
