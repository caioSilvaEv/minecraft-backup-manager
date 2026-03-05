import json
from pathlib import Path
from datetime import datetime
import shutil


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_backup_name() -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return f"world_{timestamp}.zip"


def zip_world_folder(world_path: Path, backup_dir: Path, backup_name: str) -> Path:
    # Garantir que a pasta do mundo existe
    if not world_path.exists() or not world_path.is_dir():
        raise FileNotFoundError(f"world_path inválido: {world_path}")

    # Garantir que a pasta de backups existe
    backup_dir.mkdir(parents=True, exist_ok=True)

    # O shutil.make_archive cria o zip usando um "base_name" sem .zip
    zip_path = backup_dir / backup_name
    base_name = zip_path.with_suffix("")  # tira .zip

    # Faz o zip da pasta world
    # root_dir = pasta "pai" do world
    # base_dir = nome da pasta a compactar (world)
    created = shutil.make_archive(
        base_name=str(base_name),
        format="zip",
        root_dir=str(world_path.parent),
        base_dir=world_path.name
    )

    return Path(created)


def main():
    config = load_config("config.json")

    world_path = Path(config["world_path"])
    backup_dir = Path(config["local_archive_dir"])

    backup_name = generate_backup_name()
    zip_file = zip_world_folder(world_path, backup_dir, backup_name)

    print("✅ Backup criado:", zip_file)


if __name__ == "__main__":
    main()
