### Описание
Проект «YaMDb». YaMDb — это платформа для сбора отзывов пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.. API предоставляет простой и эффективный способ управления данными, позволяя пользователям создать, отредактировать или удалить собственный отзыв, прокомментировать отзыв другого автора.
### Установка
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Mask763/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Примеры
После запуска проекта примеры запросов к API можно посмотреть по адресу:

```
http://127.0.0.1:8000/redoc/
```
### Основной стек
Проект написан с использованием Python 3.9.10, Django и Django REST Framework.
### Авторы проекта
[AkhtemKurtiev](https://github.com/AkhtemKurtiev)
[YakovlevKir](https://github.com/YakovlevKir)
[Mask763](https://github.com/Mask763)