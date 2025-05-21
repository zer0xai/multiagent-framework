import os
import json


def validate_translations(base_lang="en", locales_path="locales"):
    base_file = os.path.join(locales_path, f"{base_lang}.json")

    if not os.path.exists(base_file):
        print(f"❌ Base language file '{base_file}' not found.")
        return

    with open(base_file, "r", encoding="utf-8") as f:
        base_translations = json.load(f)

    all_keys = set(base_translations.keys())

    success = True

    for file_name in os.listdir(locales_path):
        if not file_name.endswith(".json") or file_name == f"{base_lang}.json":
            continue

        lang_code = file_name.replace(".json", "")
        file_path = os.path.join(locales_path, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            translations = json.load(f)

        keys = set(translations.keys())

        missing = all_keys - keys
        extra = keys - all_keys

        if missing:
            print(f"⚠️  [{lang_code}] Missing keys: {sorted(missing)}")
            success = False
        if extra:
            print(f"🔸 [{lang_code}] Extra keys not in base: {sorted(extra)}")
            success = False
        if not missing and not extra:
            print(f"✅ [{lang_code}] OK")

    if success:
        print("✅ All translation files are valid and consistent.")
    else:
        print("❗ Please fix the inconsistencies above.")


if __name__ == "__main__":
    validate_translations()
