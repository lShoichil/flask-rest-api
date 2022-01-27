flast-rest-api
---

## Предводирельно необходимо создать db в папке с проектом с помощью следующих команд:
+ python3
+ from app import db
+ db.create_all()
+ exit().

## Необходимые библиотеки для работы проекта
(Запускал в PyCharm, устанавливал библиотеки через pip). 

Как только создадите окружение и пропишите source "ваш venv"/bin/activate, то для корректной работы нужно сделать следующие pip-ы:
+ pip install flask
+ pip install Flask-SQLAlchemy
+ pip install pyjwt
+ pip install python-dotenv

## В .env лежит вариант prod или dev версии:
```
SERVER_ENV=prod
```
## В config.py лежал ключ и путь до папки с проектом:
```
import os
class Configuration(object):
    file_path = os.path.abspath(os.getcwd()) + "/todo.db"
    SECRET_KEY = '...'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
```
## Работа с пользователями
### Авторизация пользователя
Токен авторизованного пользователя действителей 1 час

В случае неверного токена авторизованного пользователя
![image](https://user-images.githubusercontent.com/78679833/149453545-ba5db68d-dcc1-4844-a2e5-eb55125e1c8f.png)
В случае отсутствия токена авторизованного пользователя
![image](https://user-images.githubusercontent.com/78679833/149453568-03f4057c-dd72-4410-aba0-b326186b0c4d.png)
Получение верного токена
![image](https://user-images.githubusercontent.com/78679833/149453607-79975d85-6e36-41f8-bf2a-84ebfc6cd023.png)
В случае запроса токена для не существующего пользователя
![image](https://user-images.githubusercontent.com/78679833/149453687-33674fd4-6771-4a2b-b711-afd40be44883.png)
### Создание пользователя
![image](https://user-images.githubusercontent.com/78679833/149453745-c008a681-de30-40ce-8685-468412818855.png)
### Вывод всех пользователей
![image](https://user-images.githubusercontent.com/78679833/149453784-9ea18c61-a1fb-4eb6-983b-dbcf010440cf.png)
### Повышение прав пользователя
![image](https://user-images.githubusercontent.com/78679833/149453815-f6b7fb8c-b9f9-40b0-861c-ae2a46951155.png)
![image](https://user-images.githubusercontent.com/78679833/149453817-0c2ad50d-6b0e-4338-9be9-f07de1160c53.png)
![image](https://user-images.githubusercontent.com/78679833/149453832-be473238-5ea8-4bfd-bddd-ba108809ac76.png)
### Удаление пользователя
![image](https://user-images.githubusercontent.com/78679833/149453858-8e0850be-faee-403b-863b-b050f76577e0.png)
![image](https://user-images.githubusercontent.com/78679833/149453872-ea286aaf-630d-4804-b0c2-14db8eba98b7.png)
![image](https://user-images.githubusercontent.com/78679833/149453888-b5b6c683-e4ae-43b7-b684-65db239506a1.png)
### Поиск конкретного пользователя по его public_id
![image](https://user-images.githubusercontent.com/78679833/149453948-44106ab5-47b7-47ba-9e3b-ae93aeba706d.png)

## Работа с задачами для todo листа
### Создание задачи
Определение пользователя, создающего задачу происходит по токену
![image](https://user-images.githubusercontent.com/78679833/149639171-371054d8-0d42-495d-88fe-27e63ba24f4b.png)
### Вывод всех задач
Вывод всех задач для пользователя “Admin” по его токену
![image](https://user-images.githubusercontent.com/78679833/149454083-58d1a930-6ed1-45cd-a4e8-c5f0edd4d96f.png)
Вывод всех задач (предварительно создал 2) для пользователя “Boba” по его токену
![image](https://user-images.githubusercontent.com/78679833/149454146-b9957dfe-f609-4104-bc11-de8291ec1401.png)
### Вывести задачу по её id
![image](https://user-images.githubusercontent.com/78679833/149454216-4a59f1b2-d0b5-42ef-a46b-de8b28be30c0.png)
Если запросить не существующую задачу
![image](https://user-images.githubusercontent.com/78679833/149454283-d1c8f259-7c1e-4558-adec-720326829495.png)
### Изменение статуса задачи
![image](https://user-images.githubusercontent.com/78679833/149454325-6d113904-2f9a-418c-a404-1530e8933574.png)
Было:
![image](https://user-images.githubusercontent.com/78679833/149454349-ef071274-5d27-4573-9aaf-3fa4924d8936.png)
Стало:
![image](https://user-images.githubusercontent.com/78679833/149454370-d9b306ca-a83c-41be-be9c-37c08ba21a9f.png)
### Удаление задач по её id
![image](https://user-images.githubusercontent.com/78679833/149454400-513cbc7a-4f9a-43c0-ba7a-6923e58c2e26.png)
Теперь у нас одна задача
![image](https://user-images.githubusercontent.com/78679833/149454429-aa486c06-fc0f-4197-bf2c-777f6e7fde56.png)
В случае попытки удаление не сущестующей задачи
![image](https://user-images.githubusercontent.com/78679833/149454471-c02bf2ee-72c1-41be-b2a6-8d88e29639b5.png)
