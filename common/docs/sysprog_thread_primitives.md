# Примитивы синхронизации потоков

С.Ю. Папулин (papulin_bmstu@mail.ru)

### Содержание

- [Состояние гонки и мьютексы](#Состояние-гонки-и-мьютексы)
- [Взаимная блокировка](#Взаимная-блокировка)
- [Рекурсивный мьютекс](#Рекурсивный-мьютекс)
- [События](#События)
- [Барьеры](#Барьеры)
- [Семафоры](#Семафоры)
- [Условия](#Условия)
- [Очереди](#Очереди)
<!-- - ~~Таймер~~ -->

Исходники всех примеров [здесь](../projects/threading_examples)

## Состояние гонки и мьютексы

- [sysprog_threading_race_condition.py](../projects/threading_examples/sysprog_threading_race_condition.py)
- [sysprog_threading_lock.py](../projects/threading_examples/sysprog_threading_lock.py)

## Взаимная блокировка

- [sysprog_threading_deadlock.py](../projects/threading_examples/sysprog_threading_deadlock.py)

## Рекурсивный мьютекс

- [sysprog_threading_rlock.py](../projects/threading_examples/sysprog_threading_rlock.py)

## События

- [sysprog_threading_event.py](../projects/threading_examples/sysprog_threading_event.py)


## Барьеры

- [sysprog_threading_barrier.py](../projects/threading_examples/sysprog_threading_barrier.py)

## Семафоры

- [sysprog_threading_semaphore.py](../projects/threading_examples/sysprog_threading_semaphore.py)
- [sysprog_threading_semaphore_guess.py](../projects/threading_examples/sysprog_threading_semaphore_guess.py)
- [sysprog_threading_semaphore_decorator.py](../projects/threading_examples/sysprog_threading_semaphore_decorator.py)
- [sysprog_threading_semaphore_with_decorator.py](../projects/threading_examples/sysprog_threading_semaphore_with_decorator.py)

## Условия

- [sysprog_threading_condition.py](../projects/threading_examples/sysprog_threading_condition.py)

## Очереди

- [sysprog_threading_queue.py](../projects/threading_examples/sysprog_threading_queue.py)


## Таймеры

```bash
# TODO
```

## Источники

- [The Python Standard Library. Concurrent Execution](https://docs.python.org/3.7/library/concurrency.html)
