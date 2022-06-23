# Многопроцессные приложения

С.Ю. Папулин (papulin_bmstu@mail.ru)

### Содержание

- [Пререквизиты](#Пререквизиты)
- [Модуль `multiprocessing`](#Модуль-`multiprocessing`)
- [Примитивы синхронизации процессов](#Примитивы-синхронизации-процессов)
- [Межпроцессная коммуникация](#Межпроцессная-коммуникация)
- [Сравнение производительности многопоточных и многопроцессных приложений](#Сравнение-производительности-многопоточных-и-многопроцессных-приложений)
- [Асинхронное выполнение с `concurrent.futures`](#Асинхронное-выполнение-с-concurrent.futures)
- [Источники](#Источники)

## Пререквизиты

- [Процессы, потоки и IPC в Python](sysprog_proc_thread.md)
- [Примитивы синхронизации потоков](sysprog_thread_primitives.md)

## Проект

Все примеры находятся здесь: [multiprocessing_examples](../projects/multiprocessing_examples)

## Модуль `multiprocessing`

Запуск множества процессов с одной задачей:

- Исходный код: [sysprog_multiprocessing.py](../projects/multiprocessing_examples/sysprog_multiprocessing.py)

Запустите команду отображения дерева процессов с указанием PID родительского процесса:

```bash
pstree -p $PID
```

Использование собственного класса с наследованием от `Process`:

- [sysprog_multiprocessing_class.py](../projects/multiprocessing_examples/sysprog_multiprocessing_class.py)

Область видимости глобальных переменных:

- [sysprog_multiprocessing_global.py](../projects/multiprocessing_examples/sysprog_multiprocessing_global.py)

## Примитивы синхронизации процессов

- lock
- condition
- event
- semaphore synchronization


## Межпроцессная коммуникация

Средства коммуникации:
- Сокеты
- Именованная каналы
- Анонимных каналы:
    - Общение двух дочерних процессов: 
        - [sysprog_multiprocessing_pipe.py](../projects/multiprocessing_examples/sysprog_multiprocessing_pipe.py)
    - Мастер передает данные одному из рабочих узлов: 
        - [sysprog_multiprocessing_pipe_multiple_workers.py](../projects/multiprocessing_examples/sysprog_multiprocessing_pipe_multiple_workers.py)
- Общие переменные:
    - Переменная Value:
        - Демонстрация состояния гонки: 
            - [sysprog_multiprocessing_value_race.py](../projects/multiprocessing_examples/sysprog_multiprocessing_value_race.py)
        - Использование взаимоисключающей блокировки (мьютекса): 
            - [sysprog_multiprocessing_value.py](../projects/multiprocessing_examples/sysprog_multiprocessing_value.py)
    - Массива Array: 
        - [sysprog_multiprocessing_array.py](../projects/multiprocessing_examples/sysprog_multiprocessing_array.py)
    - Очередь Queue: 
        - [sysprog_multiprocessing_queue.py](../projects/multiprocessing_examples/sysprog_multiprocessing_queue.py)

## Запуск однотипных задач на множестве исполнителей (Pool)

Исходный код:
- [sysprog_multiprocessing_pool.py](../projects/multiprocessing_examples/sysprog_multiprocessing_pool.py)

Аргументы запуска программы:

- `--map`: запускает задачи на заданном количестве исполнителей и ожидает их выполнение, результат возвращается в том же порядке, как запускались задачи

- `--imap`: то же, что и `map`, но выдает результат по мере готовности в соответствии с порядком запуска

- `--imap_unordered`: то же, что и `imap`, но порядок не соблюдается

- `--map_async`: не блокирует основной поток


## Сравнение производительности многопоточных и многопроцессных приложений

Исходный код:

- [sysprog_multiprocessing_performance.py](../projects/multiprocessing_examples/sysprog_multiprocessing_performance.py)


## Асинхронное выполнение с `concurrent.futures`

### Потоки

Исходный код:

- [sysprog_futures_thread.py](../projects/futures_examples/sysprog_futures_thread.py)
- [sysprog_futures_thread_pool.py](../projects/futures_examples/sysprog_futures_thread_pool.py)

### Процессы

Исходный код:

- [sysprog_futures_process_pool.py](../projects/futures_examples/sysprog_futures_process_pool.py)


## Источники

- [The Python Standard Library. Concurrent Execution](https://docs.python.org/3.7/library/concurrency.html)