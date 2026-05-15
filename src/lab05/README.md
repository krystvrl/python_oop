# ЛР-5 — Функции как аргументы. Стратегии и делегаты (вариант 4)

## 1. Цель работы

- Научиться передавать функции как аргументы.
- Использовать `map`, `filter`, `sorted`.
- Реализовать фабрики функций и `lambda`.
- Показать паттерн «Стратегия» через callable-объекты.

## 2. Реализованные функции 


  - сортировка: `by_owner_name`, `by_balance`, `by_balance_then_owner`;
  - фильтры/фабрики: `is_rich`, `is_savings_account`;
  - обработчики: `make_balance_multiplier`, `PercentBonusStrategy`, `owner_to_string`.

  - `add`, `extend`, `to_list`, `print_preview`, `sort_by`, `filter_by`, `apply`, `map`.

  

## 3. Демонстрация работы

### Сценарий 1 — filter → sort → apply

![Картинка 1](/images/lab05/Skript1.jpg)
![Картинка 1](/images/lab05/Skript1_0.jpg)

Что делаем:
- создаём коллекцию из 5 аккаунтов;
- фильтруем `filter_by(is_rich(40000))`;
- сортируем `sort_by(by_balance)`;
- применяем `apply(PercentBonusStrategy(0.05))`.


### Сценарий 2 — три стратегии сортировки

![Картинка 1](/images/lab05/Skript2.jpg)
![Картинка 1](/images/lab05/Skript2_0.jpg)

Что делаем:
- сортируем одну и ту же коллекцию тремя способами:
  - `sort_by(by_owner_name)`;
  - `sort_by(by_balance)`;
  - `sort_by(by_balance_then_owner)`.


### Сценарий 3 — callable-стратегия, map/filter, lambda

![Картинка 1](/images/lab05/Skript3.jpg)
![Картинка 1](/images/lab05/Skript3_0.jpg)

Что делаем:
- применяем `apply(make_balance_multiplier(0.9))`;
- используем `map(owner_to_string)` и `map(lambda ...)`;
- используем `filter(is_rich(100000))`;
- фильтруем по типу через `isinstance` и через `lambda`.

## 4. Вывод

- Функции как аргументы позволяют вынести поведение из коллекции.
- Фабрики дают параметризацию предикатов и обработчиков.
- Callable-объекты реализуют паттерн «Стратегия».
- `map`, `filter`, `lambda` упрощают преобразование и отбор объектов.