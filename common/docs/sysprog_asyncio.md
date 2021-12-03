# Асинхронное выполнение

Сергей Ю. Папулин (papulin_bmstu@mail.ru)

### Содержание

- [Асинхронное выполнение с `asyncio`](#Асинхронное-выполнение-с-asyncio)
- [Источники](#Источники)

## Пререквизиты

- [Процессы, потоки и IPC в Python](sysprog_proc_thread.md)
- [Примитивы синхронизации потоков](sysprog_thread_primitives.md)



## Асинхронное выполнение с `asyncio`


Модуль `asyncio` преимущественно предназначен для асинхронного выполнения I/O нагруженных задач и позволяет выполнять:

- сопрограммы (coroutines) с полным контролем над ходом выполнения
- сетевые IO и IPC
- управление подпроцессами
- распределенные задачи с использованием очередей
- синхронизацию кода с параллельными задачами

Для асинхронного выполнения в `asyncio` используется цикл событий (even loop), который предназначен для запуска и ожидания задач. Все задачи выполняются в одном потоке.

## Сопрограммы и задачи

В `asyncio` три типа объектов с возможность ожидания выполнения посредством `await`:
- Coroutines
- Tasks
- Futures

Task позволяют выполнять задачи Coroutine одновременно (фактически это будет попеременно без блокировки, т.е. без ожидания завершения выполнения задачи)

Future - объект результата асинхронного выполнения.

|Команда|Описание|
|-|-|
|`run()`|Создает цикл событий, выполняет сопрограмму, закрывает цикл событий|
|`create_task()`|Создает и запускает `Task`|
|`await sleep()`|Ожидает указанное количество секунд|
|`await gather()`|Запускает и ожидает выполнение всех задач|
|`await wait_for()`|Запускает сопрограмму и ждет указанное количество секунд. Если сопрограмма не завершается в отведенное время, то возникает исключение|
|`await shield()`|Не допускает отмены выполнения|
|`await wait()`|Ожидает завершение выполнения|
|`current_task()`|Возвращает текущую задачу|
|`all_tasks()`|Возвращает все задачи цикла событий|
|`Task`|Объекта задачи |
|`for in as_completed()`|Ожидает завершения выполнения с использованием цикла `for`|



## Выполнение множества задач

sysprog_asyncio.py
```python
import asyncio
import random


async def run_task(i):
    await asyncio.sleep(random.randint(0,2))
    print("Task [{}] is completed.".format(i))
    return i


async def run_job():
    tasks = list()
    for i in range(10):
        # Run sequentially
        task = run_task(i)
        tasks.append(task)
    done_tasks, pending_tasks = await asyncio.wait(tasks)
    for future in done_tasks:
        print(future.result())


async def run_job_():
    tasks = list()
    for i in range(10):
        # Run sequentially
        task = run_task(i)
        tasks.append(task)
    done_tasks = await asyncio.gather(*tasks)
    print(done_tasks)
    # for future in done_tasks:
    #     print(future.result())


# Create event loop, run a coroutine, close the loop.
asyncio.run(run_job())

# Low-level alternative
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(run_job_())
# finally:
#     loop.close()

```

## Stream

`Stream` предназначен для работы с сетевыми соединениями и позволяет обмениваться данными в асинхронном режиме.

```python
import asyncio
import argparse


HOST = "127.0.0.1"
PORT = 9996


async def client(message):
    reader, writer = await asyncio.open_connection(HOST, PORT)
    writer.write(message.encode())
    reply = await reader.read(1024)
    print("sent [{}] => received: [{}]".format(message, reply.decode()))
    writer.close()


async def handle_client(reader, writer):
    data = await reader.read(1024)
    message = data.decode()[::-1]
    addr = writer.get_extra_info("peername")
    print("client: {}".format(addr))
    writer.write(message.encode())
    await writer.drain()
    writer.close()


async def server():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print("serving on {}".format(addr))
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-s", "--server", action="store_true", help="Start the server.")
    parser.add_argument("-c", "--client", type=str, help="Start the client.")

    args = parser.parse_args()

    if args.server:
        print("Starting the server...")
        asyncio.run(server())
    elif args.client is not None:
        print("Starting the client...")
        asyncio.run(client(args.client))
```

Запуск сервера:

```bash
python sysprog_asyncio_stream.py --server
```

Запуск клиента:

```bash
python sysprog_asyncio_stream.py --client hello
```