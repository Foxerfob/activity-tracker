# Activity Tracker

Activity Tracker - это приложение для записи вашей активности в базу данных и последующего создания статистики. Это поможет вам отслеживать, анализировать и управлять своим временем и задачами.

## Функционал

- Запись активностей с указанием времени начала и окончания.
- Группировка активностей по категориям.
- Подсчет и отображение суммарного времени для каждой категории.

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Foxerfob/activity-tracker.git 
```

2. Перейдите в директорию проекта:
```bash
cd activity-tracker
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Настройка базы данных

1. Установите postgresql:

Arch:
```bash
sudo pacman -S postgresql
```

Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql
```

2. Запустите службу postgresql:
```bash
sudo systemctl enable --now postgresql
```

3. Создайте базу данных:
```bash
psql -U postgres
```
```SQL
CREATE DATABASE activitytracker;
\q
```

4. Создайте таблицы:
```bash
psql -U postgres -b activitytracker
```
```SQL
CREATE TABLE Categories (
    CategoryID SERIAL PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL
    );
CREATE TABLE Logs (
    LogID SERIAL PRIMARY KEY,
    CategoryID INT REFERENCES Categories(CategoryID),
    LogDescription TEXT,
    LogStartTime TIMESTAMP NOT NULL,
    LogEndTime TIMESTAMP NOT NULL
    );
```

5. Создайте категории:
Например
```SQL
INSERT INTO categories(categoryname) VALUES ('Sleep');
INSERT INTO categories(categoryname) VALUES ('Coding');
INSERT INTO categories(categoryname) VALUES ('Chill');
\q
```

## Использование

1. Запустите приложение:
```bash
python main.py
```
