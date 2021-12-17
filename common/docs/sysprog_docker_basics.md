# Контейнеризация приложений посредством Docker

С.Ю. Папулин (papulin.study@yandex.ru)

### Содержание

- [Основные команды Docker CLI](#Основные-команды-Docker-CLI)
- [Запуск сервера](#Запуск-сервера)
- [Запуск клиента](#Запуск-клиента)
- [Запуск сервера и клиента в собственной сети](#Запуск-сервера-и-клиента-в-собственной-сети)
- [Использование постоянного хранилища данных](#Использование-постоянного-хранилища-данных)
- [Взаимодействие с Redis](#Взаимодействие-с-Redis)


### Основные команды Docker CLI

Добавьте в локальный репозиторий образ `python 3.7`:

```
docker pull python:3.7-slim-buster
```

Создайте `base.Dockerfile` для описания нового образа:

- исходный код: [base.Dockerfile](../projects/docker_examples/simple_server/base.Dockerfile)

Постройте образ на основе вашего описания:

```
docker build --tag python:3.7-base --file base.Dockerfile .
```

⚠️ **Замечание.**  Для удаления образом используется команда `docker rmi $IMAGE_NAME`.

Убедитесь, что образ создан:

```
docker image ls
```

Запустите образ в контейнере:

```
docker run --interactive --tty --name simpleapp python:3.7-base
```

Параметры:

- `--interactive (-i)` - доступ к stdin контейнера
- `--tty (-t)` - псевдо-терминал (создает bash оболочку в контейнере)
- `--name` - наименование контейнера

В терминале введите `exit()`.


Отобразите список контейнеров:

```
docker container ls -a
```

или

```
docker ps -a
```

Просмотрите журнал контейнера:

```
docker logs simpleapp
```

Выведите конфигурацию контейнера:

```
docker inspect simpleapp
```

Вся информация по Docker объектам находится в директории `/var/lib/docker`.


Удалите контейнер:

```
docker rm simpleapp
```

Создайте и запустите контейнер в фоновом режиме посредством опции `detach`:

```
docker run -it --detach --name simpleapp python:3.7-base
```

Проверьте, что контейнер запущен и выполняется:

```
docker container ls -a
```

Переведите выполнение на передний план:

```
docker attach simpleapp
```

И обратно в фоновый режим:

```
Ctrl+p + Ctrl+q
```

### Запуск команд в контейнере

Отобразите наименование ОС:

```
docker exec -it simpleapp uname -a
```

Выведите версию `python`:

```
docker exec -it simpleapp python --version
```

Запустите bash оболочку:

```
docker exec -it simpleapp bash
```

Создайте файл:

```
docker exec -it simpleapp bash -c "echo "welcome" >> /home/myfile && cat /home/myfile"
```

### Остановка и повторный запуск контейнера

Остановите контейнер:

```
docker stop simpleapp
```

Проверьте, что контейнер остановлен:

```
docker container ls -a
```

Повторно запустите контейнер:

```
docker start simpleapp
```

Убедитесь, что ранее созданный файл остался в системе:

```
docker exec -it simpleapp cat /home/myfile
```

### Удаление контейнера

Остановите и удалите контейнер:

```
docker stop simpleapp && docker rm simpleapp
```

Убедитесь, что контейнер удален:

```
docker container ls -a
```

⚠️ **Замечание.**  После удаления контейнера все изменения будут потеряны. Таким образом при следующем выполнении `run` в контейнере не будет файла `myfile`. Для сохранения результата необходимо использовать постоянные хранилища.


## Запуск сервера

### Пробный запуск сервера

Напишите программу сервера:

- исходный код: [sysprog_server.py](../projects/docker_examples/simple_server/app/sysprog_server.py)

Создайте описание Docker образа для развертывания сервера:

- исходный код: [server-1.0.Dockerfile](../projects/docker_examples/simple_server/server-1.0.Dockerfile)

Постройте образ сервера:

```
docker build --tag server:1.0 --file server-1.0.Dockerfile .
```

Запустите контейнер с сервером в фоном режиме:

```
docker run -d --name server server:1.0
```

Запустите `netcat` внутри контейнера и выполните обращение к серверу:

```
docker exec -it server nc 0.0.0.0 9998
```

Остановите и удалите контейнер:

```
docker stop server && docker rm server
```

### Внешний доступ к серверу

Запустите контейнер с открытым портом:

```
docker run -d --publish 9999:9998 --name server server:1.0
```

Проверьте работоспособность сервер из терминала хоста:

```
nc localhost 9999
```

Остановите и удалите контейнер:

```
docker stop server && docker rm server
```

## Запуск клиента

### Доступ к серверу через хост

Выведите список сетей:

```
docker network ls
```

Отобразите информацию о `bridge` сети, которая используется как сеть по умолчанию при запуске контейнера:

```
docker network inspect bridge
```

Шлюз этой сети можно определить через команду:

```
ip addr show docker0
```

⚠️ **Замечание.**  В сети `bridge`, которая используется по умолчанию, нет возможности обращаться по наименованию контейнера, только по IP адресу.

Запустите сервер в сети по умолчанию:

```
docker run -d -p 9999:9998 --name server server:1.0 python3 /app/sysprog_server.py --server --host 172.17.0.2
```

В качестве параметра `host` указан адрес, который будет назначен контейнеру.


Запустите клиента в той же сети:

```
docker run -itd --name client server:1.0 python3 /app/sysprog_server.py --client --host 172.17.0.2
```

Теперь клиент может напрямую обратиться к серверу:

```
docker attach client
```

```
Ctrl+p + Ctrl+q
```


Остановите и удалите контейнеры клиента и сервер.

```
docker stop client server && docker rm client server
```


⚠️ **Замечание.**  Если указать в качестве host шлюз сети и внешний порт сервера, то клиент так же сможет получить доступ к серверу, но через хост. Пример команды: 

```
docker run -itd --name client server:1.0 python3 /app/sysprog_server.py --client --host 172.17.0.1 --port 9999
```

### Запуск клиента в режиме хоста

Запустите сервер:

```
docker run -d --publish 9999:9998 --name server server:1.0
```

Запустите клиента в режиме хоста:

```
docker run -itd --network=host --name client server:1.0 python3 /app/sysprog_server.py --client --port 9999
```

Клиент теперь работает как отдельный процесс хоста и может обращаться к серверу с использованием порта 9999:

```
docker attach client
```

```
Ctrl+p + Ctrl+q
```

Остановите и удалите контейнеры клиента и сервер.

```
docker stop client server && docker rm client server
```

## Запуск сервера и клиента в собственной сети


### Создание сети

Создайте собственную `bridge` сеть:

```
docker network create --driver=bridge --subnet=10.0.1.0/16 sysprog-network
```

Отобразите список сетей:

```
docker network ls
```

Выведите настройки сети:

```
docker network inspect sysprog-network
```

### Запуск сервера и клиента

Измените исходное описание так, чтобы использовать `ENTRYPOINT` вместо `CMD`:

- исходный код: [server-1.1.Dockerfile](../projects/docker_examples/simple_server/server-1.1.Dockerfile)

Постройте новый образ:

```
docker build --tag server:1.1 --file server-1.1.Dockerfile .
```

Запустите сервер и в качестве параметра `host` укажите имя контейнера сервера:

```
docker run -d --network=sysprog-network --name server server:1.1 --server --host server
```

Запустите клиента и в качестве параметра `host` укажите имя контейнера сервера:

```
docker run -d --network=sysprog-network --name client server:1.1 --client --host server
```

⚠️ **Замечание.**  В собственной сети `bridge` можно обращаться по наименованию контейнера.

Проверьте, что контейнеры запущены:

```
docker container ls --no-trunc
```

Или можно через команды

```
docker exec server ps aux
```

и

```
docker exec client ps aux
```

Проверьте, что запущенные контейнеры принадлежат созданной сети:

```
docker network inspect sysprog-network
```

Подключите терминал клиента:

```
docker attach client
```

После ввода слов переведите клиента в фоновый режим работы:

```
Ctrl+p + Ctrl+q
```

Проверьте логи сервера и клиента:

```
docker exec server cat /app/server.log
```

```
docker exec client cat /app/client.log
```

Остановите и удалите контейнеры клиента и сервер:

```
docker stop client server && docker rm client server
```

## Использование постоянного хранилища данных

### Монтирование посредством `volume`

⚠️ **Замечание.** Создаваемые тома можно найти в директории `/var/lib/docker/volumes`

#### Именованный том

Создайте новый локальный том:

```
docker volume create --driver local sysprog-volume
```

Выведите список томов:

```
docker volume ls
```

Отобразите конфигурацию созданного тома:

```
docker volume inspect sysprog-volume
```

Создайте и запустите контейнер сервера с локальным томом:

```
docker run -d --volume sysprog-volume:/app --network=sysprog-network --name server server:1.1 --server --host server
```

⚠️ **Замечание.** Если том ещё не существует, то он будет создан при запуске контейнера

Создайте и запустите контейнер клиента:

```
docker run -d --network=sysprog-network --name client server:1.1 --client --host server
```

Выведите на передний план запущенный процесс клиента:

```
docker attach client
```

Переведите контейнер в фоновый режим работы:

```
Ctrl+p + Ctrl+q
```

Отобразите события обработки запросов сервером:

```
docker exec server cat /app/logs/server.log
```

Остановите и удалите контейнеры клиента и сервера:

```
docker stop client server && docker rm client server
```

Повторно создайте и запустите контейнер сервера:

```
docker run -d --volume sysprog-volume:/app --network=sysprog-network --name server server:1.1 --server --host server
```

Проверьте, что логи не были удалены вместе с контейнером:

```
docker exec server cat /app/logs/server.log
```

#### Анонимный том

```
--volume $HOST_PATH:$CONTAINER_PATH
```


### Монтирование посредством `bind mound`

Монтирование директории с логами:

- сервер

```
docker run -d --volume $(pwd)/server:/app/logs --network=sysprog-network --name server server:1.1 --server --host server
```

- клиент

```
docker run -itd --volume $(pwd)/client:/app/logs --network=sysprog-network --name client server:1.1 --client --host server
```

Остановите и удалите контейнер клиента:

```
docker stop client && docker rm client
```

Изменение кода программы без повторного построения образа:

- подключите к контейнеру клиента директорию с приложением

```
docker run -itd --volume $(pwd)/app:/app --network=sysprog-network --name client server:1.1 --client --host server
```

- остановите контейнер клиента:

```
docker stop client
```

- измените формат вывода запроса

- повторно запустите контейнер клиента:

```
docker start client
```

- проверьте изменился ли формат вывода

Остановите и удалите контейнеры клиента и сервер:

```
docker stop client server && docker rm client server
```

## Взаимодействие с Redis

### Запуск контейнера с Redis

Запуск контейнера с Redis:

```
docker run -d --name redis -p 6379:6379 -v redis-data:/data redis:6.0.16-alpine redis-server --save 60 1
```

### Запись и чтение данных посредством Redis CLI

Запустите Redis CLI:

```
docker exec -it redis redis-cli
```

Введите команды:

```
SET requests 0
```

```
INCR requests
```

```
GET requests
```

### Запись и чтение данных посредством Python модуля redis-py

Создайте файл `requirements.txt` и добавьте требуемые модулю:

- исходный код: [requirements.txt](../projects/db_examples/requirements.txt)

Запустите установщик модулей:

```
pip install -r requirements.txt
```

Создайте python программу для взаимодействия с Redis:

- исходный код: [sysprog_redis_client.py](../projects/db_examples/sysprog_redis_client.py)

Запустите программу:

- увеличение переменной `requests` на 1:

```
python sysprog_redis_client.py --increment
```

- отображения значения переменной `requests`:

```
python sysprog_redis_client.py --show
```

### Завершение работы

```
docker stop redis && docker rm redis && docker volume rm redis-data
```