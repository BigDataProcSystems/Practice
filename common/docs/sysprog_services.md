# Создание системных сервисов в Linux

Сергей Ю. Папулин (papulin_bmstu@mail.ru)

### Содержание

- [Запуск сервиса посредством `systemd`](#Запуск-сервиса-посредством-`systemd`)
- [~~Запуск периодических задач посредством `cron`~~](#Запуск-периодических-задач-посредством-`cron`)
- [Источники](#Источники)


## Запуск сервиса посредством `systemd`

### Сервер

Код сервер

sysprog_server.py
```python
import os

from socket import socket, AF_INET, SOCK_STREAM

HOST = ""
PORT = 9998


def server():
    print("Server [{}]".format(os.getpid()))
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        print("received request [{}]".format(data))
        # reverse data
        conn.send(data.decode()[::-1].encode())


if __name__ == "__main__":
    server()
```

### Клиент

Код клиента

service.py
```python
from socket import socket, AF_INET, SOCK_STREAM


HOST = ""
PORT = 9998


def client(data):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(data.encode())
    reply = sock.recv(1024).decode()
    sock.close()
    print("sent [{}] => received: [{}]".format(data, reply))


if __name__ == "__main__":
    while True:
        data = input()
        if not data:
            break
        client(data)
```


### Служба

Описание службы

.service
```ini
[Unit]
Description=Sysprog service
Wants=network-online.target
After=network-online.target

[Service]
Environment=PYTHONUNBUFFERED=1
Type=simple
ExecStart=/home/ubuntu/ML/anaconda3/bin/python3.7 /home/ubuntu/IdeaProjects/c5/sysprog_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Скрип для управления сервисом:

- bash скрипт

```bash
# TODO
```

- python скрипт

service.py
```python
#!/usr/bin/env python

import os
import argparse


def deploy():
    # 1. Copy service from a develop dir to the systemd directory
    # 2. Reload systemd manager configuration
    # 3. Start the sysprog service
    os.system(
        """
        sudo cp .service /etc/systemd/system/sysprog.service \
        && sudo systemctl daemon-reload \
        && sudo systemctl start sysprog
        """
    )


def start():
    os.system("sudo systemctl start sysprog")


def stop():
    os.system("sudo systemctl stop sysprog")


def restart():
    os.system("sudo systemctl restart sysprog")


def show_status():
    os.system("systemctl status sysprog")


def show_logs():
    os.system("journalctl -u sysprog -f")


def run_client():
    os.system("python sysprog_client.py")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-d", "--deploy", action="store_true", help="Deploy the service.")
    parser.add_argument("-q", "--stop", action="store_true", help="Stop the service.")
    parser.add_argument("-r", "--start", action="store_true", help="Start the service.")
    parser.add_argument("-R", "--restart", action="store_true", help="Restart the service.")
    parser.add_argument("-l", "--logs", action="store_true", help="Show service logs.")
    parser.add_argument("-s", "--status", action="store_true", help="Show service status.")
    parser.add_argument("-c", "--client", action="store_true", help="Run the client.")
    args = parser.parse_args()

    if args.deploy:
        print("Deploying...")
        deploy()
    elif args.start:
        print("Starting...")
        start()
    elif args.stop:
        print("Stopping...")
        stop()
    elif args.restart:
        print("Stopping...")
        stop()
    elif args.logs:
        print("Showing logs...")
        show_logs()
    elif args.status:
        print("Showing status...")
        show_status()
    elif args.client:
        print("Running client...")
        run_client()
    print("Done.")

```

Команды `systemctl`

```
systemctl enable|disable|start|stop|...|status service
```

|Команда|Описание|
|-|-|
|`enable`|Запуск службы при загрузке системы|
|`disable`|Отключение запуска службы при загрузке системы|
|`is-enabled`|Проверка запуска при старте системы|
|`start`|Запуск службы|
|`stop`|Остановка службы|
|`restart`|Останавливает и повторно запускает службу|
|`daemon-reload`|Обновление конфигурации|
|`status`|Вывод статуса службы|



Системный события:

```bash
 tail -f /var/log/syslog
```

Журнал событий сервиса:

```bash
journalctl -u sysprog -r
```

## Запуск периодических задач посредством `cron`

```bash
# TODO
```


## Источники

- [systemd - project page](https://systemd.io/)
- [systemd](https://wiki.archlinux.org/title/systemd)