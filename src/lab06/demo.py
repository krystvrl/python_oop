#!/usr/bin/env python3
"""Демонстрация ЛР-6 — Generics и Protocols."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Protocol, cast


def _ensure_paths() -> None:
	src_dir = Path(__file__).resolve().parents[1]
	if str(src_dir) not in sys.path:
		sys.path.insert(0, str(src_dir))

	# Для старых локальных импортов в lab03 (from base import ...)
	lab03_dir = src_dir / "lab03"
	if str(lab03_dir) not in sys.path:
		sys.path.insert(0, str(lab03_dir))


_ensure_paths()

from lab03.base import BankAccount
from lab03.models import CreditAccount, SavingsAccount
from lab06.container import Displayable, DisplayableCollection, Scorable, ScorableCollection


class AccountView(Displayable, Scorable, Protocol):
	"""Локальный Protocol для объектов, у которых есть и display(), и score()."""


def print_section(title: str) -> None:
	print("\n" + "=" * 72)
	print(title)
	print("=" * 72)


def attach_display_and_score() -> None:
	"""Добавляет display()/score() к классам из lab03 для demo structural typing."""

	def _display(self) -> str:  # type: ignore[unused-argument]
		return (
			f"{type(self).__name__}: {getattr(self, 'owner_name', '?')} | "
			f"баланс = {getattr(self, 'balance', 0):.2f} {getattr(self, 'currency', '?')}"
		)

	def _score(self) -> float:  # type: ignore[unused-argument]
		if hasattr(self, "calculate_annual_interest"):
			try:
				return float(self.calculate_annual_interest())
			except Exception:
				return 0.0
		return 0.0

	for cls in (BankAccount, SavingsAccount, CreditAccount):
		setattr(cls, "display", _display)
		setattr(cls, "score", _score)


def to_displayable(obj: object) -> Displayable:
	if not hasattr(obj, "display"):
		raise TypeError("Объект не поддерживает display()")
	return cast(Displayable, cast(object, obj))


def to_account_view(obj: object) -> AccountView:
	if not hasattr(obj, "display") or not hasattr(obj, "score"):
		raise TypeError("Объект не поддерживает display()/score()")
	return cast(AccountView, cast(object, obj))


def scenario_1_displayable_collection() -> None:
	print_section("СЦЕНАРИЙ 1 — TypedCollection[Displayable]")
	print("Разные классы из ЛР-3 работают через общий метод display().")

	col = DisplayableCollection[Displayable](validator=lambda x: hasattr(x, "display"))

	raw_items: list[object] = [
		BankAccount("Иванов И.И.", "RUB", 12000),
		SavingsAccount("Петров П.П.", "RUB", 50000, interest_rate=5.0),
		CreditAccount("Сидорова А.А.", "RUB", credit_limit=30000),
	]

	for obj in raw_items:
		col.add(to_displayable(obj))

	print("Содержимое коллекции:")
	for index, item in enumerate(col, start=1):
		print(f"  {index}. {item.display()}")

	found = col.find(lambda x: "Петров" in x.display())
	missing = col.find(lambda x: "Несуществующий" in x.display())

	print("\nfind('Петров'):")
	print("  найдено:", found.display() if found else None)
	print("find('Несуществующий'):")
	print("  найдено:", missing)


def scenario_2_scorable_collection() -> None:
	print_section("СЦЕНАРИЙ 2 — TypedCollection[Scorable]")
	print("Тот же контейнер работает с другим ограничением типа и числовым показателем.")

	col = ScorableCollection[AccountView](validator=lambda x: hasattr(x, "score"))

	raw_items: list[object] = [
		BankAccount("Орлова М.", "USD", 40000),
		SavingsAccount("Кузнецов А.", "RUB", 150000, interest_rate=6.0),
		CreditAccount("Фролов Д.", "EUR", credit_limit=40000),
	]

	for obj in raw_items:
		col.add(to_account_view(obj))

	print("Элементы и их показатель:")
	for index, item in enumerate(col, start=1):
		print(f"  {index}. {item.display()} | показатель = {item.score():+.2f}")

	positive = col.filter(lambda x: x.score() > 0)
	print("\nfilter(показатель > 0):")
	for index, item in enumerate(positive, start=1):
		print(f"  {index}. {item.display()}")

	names: list[str] = col.map(lambda x: x.display().split(": ")[1].split(" |")[0])
	values: list[float] = col.map(lambda x: round(x.score(), 2))

	print("\nmap(имена) -> list[str]:")
	print(" ", names)
	print("map(показатель) -> list[float]:")
	print(" ", values)


def main() -> None:
	print("Лабораторная работа №6 — Generics и typing")
	print("Понятная демонстрация Generic-контейнера и Protocol")

	attach_display_and_score()
	scenario_1_displayable_collection()
	scenario_2_scorable_collection()

	print_section("ИТОГ")
	print("- TypedCollection поддерживает find/filter/map с типами.")
	print("- Protocol работает как структурный интерфейс (без явного наследования).")
	print("- map() показывает разные типы результата: list[str] и list[float].")


if __name__ == "__main__":
	main()
