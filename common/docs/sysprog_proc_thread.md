# Процессы, потоки и IPC в Python

С.Ю. Папулин (papulin_bmstu@mail.ru)

### Содержание

- [Процессы и потоки](#Процессы-и-потоки)
    - Создание дочерних процессов посредством `fork` и `exec`
    - Создание потоков посредством модулей `_thread` и `threading`
- [Межпроцессное взаимодействие (IPC)](#Межпроцессное-взаимодействие-(IPC))
    - Анонимные каналы
    - Именованные каналы
    - Сокеты
    - Сигналы

## Процессы и потоки

Исходники примеров [здесь](../projects/fork_examples)

### Создание дочерних процессов посредством `fork` и `exec`

**Создание дочернего процесса**


sysprog_fork.py
```python
import os


def child():
    print("Hello from child", os.getpid())
    os._exit(0)


def parent():
    while True:
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            print("Hello from parent", os.getpid(), newpid)
        if input() == "q": 
            break


parent()
```

**Ожидание завершения дочернего процесса**

sysprog_fork_wait.py
```python
import os


exitstat = 0


def child():
    global exitstat
    exitstat += 1
    print("Hello from child", os.getpid(), exitstat)
    os._exit(exitstat)
    print("Never reached")


def parent():
    while True:
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            pid, status = os.wait()
            print("Parent got", pid, status)
        if input() == 'q': 
            break


parent()
```

**Проверка поведения файловых дескрипторов**

sysprog_fork_fd.py
```python
import os
import time

fin = open("sharedfile", "r")

pid = os.getpid()
print("Program:\t{}".format(pid))

fd = fin.fileno()
print("File Descriptor:", fd)

child_pid = os.fork()
if child_pid == 0:
    # Child process
    for _ in range(100):
        fin.seek(fin.tell()+1)
        print("Child: {}".format(fin.tell()))
        time.sleep(1)
        # fin.close()
else:
    # Parent process
    print("Child Process:\t{}".format(child_pid))
    for _ in range(100):
        print("Parent: {}".format(fin.tell()))
        time.sleep(1)
    fin.close()
```


```bash
lsof -a -p $YOUR_PID
```

```bash
sudo ls -la /proc/$YOUR_PID/fd
```

```bash
ps aux | grep -e $YOUR_PARENT_PID -e $YOUR_CHILD_PID
```

**Создание дочернего процесса и замена его выполняемого кода**


sysprog_exec_child.py
```python
import sys, os
print("Hello from child", os.getpid(), sys.argv[1])
```

sysprog_exec.py
```python
import os

count = 0
while True:
    count += 1
    pid = os.fork()
    if pid == 0:
        os.execlp("python", "-c", "sysprog_exec_child.py", str(count))
    else:
        print("Child is", pid)
    if input() == "q":
        break
```

### Создание потоков посредством модулей `_thread` и `threading`

**_thread**


Создание потока

sysprog_thread.py
```python
import _thread as thread


def child(tid):
    print("Hello from thread", tid)


def parent():
    i = 0
    while True:
        i += 1
        thread.start_new_thread(child, (i,))
        if input() == "q": 
            break


parent()
```

Ожидание завершения всех потоков

sysprog_thread_join.py
```python
import _thread as thread
import time


def counter(tid, count):
    for i in range(count):
        time.sleep(1)
        print("[{}] => {}".format(tid, i))
    # exitmutexes[tid] = True


# exitmutexes = [False] * 5  # [False, False, ..., False]

for i in range(5):
    thread.start_new_thread(counter, (i, 10))

# while False in exitmutexes:
#     pass

print("Main thread exiting.")
```

Блокировка доступа

sysprog_thread_lock.py
```python
import _thread as thread


# stdoutmutex = thread.allocate_lock()
exitmutexes = [False] * 5


def counter(tid, count):
    for i in range(count):
        # stdoutmutex.acquire()
        print("[{}] => {}".format(tid, i))
        # stdoutmutex.release()
    exitmutexes[tid] = True


for i in range(5):
    thread.start_new_thread(counter, (i, 10))

while False in exitmutexes:
    pass

print("Main thread exiting.")
```


**threading**

Создание потоков, эксклюзивного доступа (блокировки) и ожидание завершения выполнения всех потоков

sysprog_threading.py
```python
import threading


class CounterThread(threading.Thread):
    def __init__(self, my_id, count, mutex):
        self.my_id = my_id
        self.count = count
        self.mutex = mutex
        threading.Thread.__init__(self)

    def run(self):
        for i in range(self.count):
            with self.mutex:
                print("[{}] => {}".format(self.my_id, i))


stdoutmutex = threading.Lock()
threads = []

for i in range(10):
    thread = CounterThread(i, 10, stdoutmutex)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("Main thread exiting.")
```

Альтернативный способ создания потока

```python
def action():
    pass


thread = threading.Thread(target=(action), args=())
thread.start()
```

Проблема использования общих ресурсов

sysprog_threading_balance.py
```python
import threading


def write_balance(value):
    with open("value", "w") as f:
        f.write(str(value))


def read_balance():
    with open("value", "r") as f:
        return int(f.readline())


def pay():
    total = read_balance()
    total -= 1
    write_balance(total)


balance = 100

write_balance(balance)

threads = []
for i in range(100):
    thread = threading.Thread(target=pay, args=())
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(read_balance())
```

Решение

```python
import threading, time
count = 0


def write(value):
    with open("value", "w") as f:
        f.write(value)


def read():
    with open("value", "r") as f:
        return f.readline()


def pay(lock):
    with lock:
        total = int(read())
        total -= 1
        write(str(total))


balance = 100

write(str(balance))

lock = threading.Lock()

threads = []
for i in range(100):
    thread = threading.Thread(target=pay, args=(lock,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(read())
```


## Межпроцессное взаимодействие (IPC)

Исходники примеров [здесь](../projects/ipc_examples)

### Анонимные каналы

sysprog_apipe.py
```python
import os, time


def child(pipeout):
    zzz = 0
    while True:
        time.sleep(zzz)
        msg = ("Spam {:03d}\n".format(zzz)).encode()
        os.write(pipeout, msg)
        zzz = (zzz+1) % 5 # 0, 1, 2, 3, 4, 0, 1,


def parent():
    pipein, pipeout = os.pipe()
    if os.fork() == 0:
        os.close(pipein)
        child(pipeout)
    else:
        os.close(pipeout)
        pipein = os.fdopen(pipein)
        while True:
            line = pipein.readline()[:-1]
            print("Parent {} got [{}] at {}".format(os.getpid(), line, time.time()))


parent()
```

Двунаправленная коммуникация

```python
# TODO
```

### Именованные каналы

sysprog_npipe.py
```python
import os, time, sys

fifoname = "/tmp/pipefifo"


def child():
    print("Child Pid:", os.getpid())
    pipeout = os.open(fifoname, os.O_WRONLY)
    zzz = 0
    while True:
        time.sleep(zzz)
        msg = ("Spam {:03d}\n".format(zzz)).encode()
        os.write(pipeout, msg)
        zzz = (zzz+1) % 5


def parent():
    pipein = open(fifoname, "r")
    while True:
        line = pipein.readline()[:-1]
        print("Parent {} got [{}] at {}".format(os.getpid(), line, time.time()))


if __name__ == "__main__":
    if not os.path.exists(fifoname):
        os.mkfifo(fifoname)
    if len(sys.argv) == 1:
        parent()
    else:
        child()
```

### Сокеты


sysprog_socket.py
```python
from socket import socket, AF_INET, SOCK_STREAM
import time


port = 50008
host = "localhost"


def server():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        reply = "server got: [{}]".format(data)
        conn.send(reply.encode())


def client(name):
    time.sleep(1)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    sock.send(name.encode())
    reply = sock.recv(1024)
    sock.close()
    print("client got: [{}]".format(reply))


if __name__ == "__main__":
    from threading import Thread
    sthread = Thread(target=server)
    sthread.daemon = True
    # don't wait for server thread
    sthread.start()
    # do wait for children to exit
    for i in range(5):
        cthread = Thread(target=client, args=("client{}".format(i),))
        cthread.start()
```


sysprog_socket_.py
```python
import sys, os
from threading import Thread

from sysprog_socket import server, client


mode = int(sys.argv[1])

if mode == 1:
    # run server in this process
    print("Server")
    server()
elif mode == 2:
    print("Client")
    # run client in this process
    client("client:process={}".format(os.getpid()))
else:
    # run 5 client threads in process
    for i in range(5):
        Thread(target=client, args=("client:process={}:thread={}".format(os.getpid(), i),)).start()
```

### Сигналы

```python
# TODO
```

## Источники

- Lutz M. Part II. System Programming / Programming Python - 4th edition