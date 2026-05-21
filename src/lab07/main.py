#!/usr/bin/env python3
"""
Точка входа приложения управления банковскими счетами.
Лабораторная работа №7 — Консольное приложение на OOP.
"""

import sys
from pathlib import Path

# Настройка путей
def _ensure_paths() -> None:
    src_dir = Path(__file__).resolve().parents[1]
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    lab03_dir = src_dir / "lab03"
    if str(lab03_dir) not in sys.path:
        sys.path.insert(0, str(lab03_dir))

_ensure_paths()

from app import BankApp
from cli import BankCLI
from storage import save_accounts, load_accounts
from exceptions import StorageError


def main() -> None:
    """Главная функция приложения."""

    # Инициализируем приложение
    app = BankApp()

    # Путь к файлу данных
    data_file = Path(__file__).parent / "accounts.json"

    # Пытаемся загрузить данные
    try:
        accounts = load_accounts(str(data_file))
        if accounts:
            app.set_loaded_accounts(accounts)
            print(f"✅ Загружено {len(accounts)} счет(ов) из {data_file.name}")
    except StorageError as e:
        print(f"⚠️  Ошибка при загрузке данных: {e}")
        print("   Начинаем с пустой коллекции")

    # Запускаем CLI
    cli = BankCLI(app)

    try:
        cli.run()
    finally:
        # Сохраняем данные при выходе
        try:
            accounts = app.get_all_accounts()
            if accounts:
                save_accounts(accounts, str(data_file))
                print(f"💾 Данные сохранены в {data_file.name}")
        except StorageError as e:
            print(f"❌ Ошибка при сохранении данных: {e}")


if __name__ == "__main__":
    main()

