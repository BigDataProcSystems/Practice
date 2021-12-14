# Создание системных сервисов в Linux

C.Ю. Папулин (papulin_bmstu@mail.ru)

### Содержание

- [Запуск сервиса посредством `systemd`](#Запуск-сервиса-посредством-`systemd`)
- [~~Запуск периодических задач посредством `cron`~~](#Запуск-периодических-задач-посредством-`cron`)
- [Источники](#Источники)


## Запуск сервиса посредством `systemd`

### Создание собственного сервиса 

Проект: [system_service_examples](../projects/system_service_examples)

Напишите код сервера:
- [sysprog_server.py](../projects/system_service_examples/sysprog_server.py)

Напишите код клиента:
- [sysprog_client.py](../projects/system_service_examples/sysprog_client.py)

Создайте описание службы:
- [.service](../projects/system_service_examples/.service)

Скопируйте `.service` в директорию сервисов:

```bash
sudo cp .service /etc/systemd/system/sysprog.service
```

Перезагрузите менеджер конфигурации:

```bash
sudo systemctl daemon-reload
```

Запустите службу:

```
sudo systemctl start sysprog
```

Проверьте, что сервис успешно запустился:

```
systemctl status sysprog
```

Запустите клиента:

```
python sysprog_client.py
```

Завершите процесс сервера:

```
sudo kill $SERVER_PID
```

Убедитесь, что сервер автоматически запустился после принудительного завершения:

```
systemctl status sysprog
```

Выведите журнал сервиса:

```bash
journalctl -u sysprog -r
```


⚠️ **Замечание.** Состояние сервиса также можно отслеживать через журнал системных событий: `tail -f /var/log/syslog`


Напишите `bash` скрипт для управления сервисом:

- [service.sh](../projects/system_service_examples/service.sh)

Напишите `python` скрипт для управления сервисом:

- [service.py](../projects/system_service_examples/service.py)



### Команды `systemctl`

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


## Запуск периодических задач посредством `cron`

```bash
# TODO
```


## Источники

- [systemd - project page](https://systemd.io/)
- [systemd](https://wiki.archlinux.org/title/systemd)