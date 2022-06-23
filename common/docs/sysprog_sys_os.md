# Системные библиотеки в Python

С.Ю. Папулин (papulin.study@yandex.ru)

### Содержание

- [Запуск Python скрипта](#Запуск-Python-скрипта)
- [Модуль sys](#Модуль-sys)
    - [Общие сведения](#Общие-сведения)
    - [Разбор входных параметров](#Разбор-входных-параметров)
    - [Стандартные потоки ввода-вывода](#Стандартные-потоки-ввода-вывода)
    - [Завершение программ]()
- [Модуль os]()
    - [Общие сведения](#Общие-сведения)
    - [Файловая система](#Файловая-система)
    - [Переменные окружения](#Переменные-окружения)
    - [Рабочий каталог](#Рабочий-каталог)
    - [Запуск shell команд](#Запуск-shell-команд)

## Запуск Python скрипта

```python
#!/usr/bin/python3

"""
Running a program as an executable script

Add executable permissions to the file owner:
    chmod u+x sysprog_executable.py

Command to run:
    ./sysprog_executable.py

If a current directory included in the PATH environment variable,
the command can be simplified:
    sysprog_executable.py

Note:
    More portable header: #!/usr/bin/env python
"""

print("Executable script.")
```

## Модуль `sys`

### Общие сведения

```python
import sys

# Вывод справки по модулю
help(sys)
```

```python
# Платформа
sys.platform
```

```python
# Версия python
sys.version
```

```python
# Пути поиска подгружаемых модулей (слева направо)
sys.path
```

```python
# Добавление пути поиска (сохраняется до завершения процесса)
sys.path.append("/home/ubuntu/")
```

### Разбор входных параметров

```python
# Входные параметры (аргументы) программы
sys.argv
```

Создайте файл с именем `sysprog_args.py` и поместите в него следующий код

```python
import sys
import argparse


def main():
    # print(sys.argv)
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", help="Input directory.", required=True)
    parser.add_argument("-o", "--output", help="Output directory.", default="/home/ubuntu/output")
    args = parser.parse_args()
    print("Input directory:\t", args.input)
    print("Output directory:\t", args.output)


if __name__ == "__main__":
    main()
```

Запустите `sysprog_args.py` в командной строке

```bash
python sysprog_args.py --input /home/ubuntu/input --output /home/ubuntu/output
```

```bash
python sysprog_args.py -i /home/ubuntu/input -o /home/ubuntu/output
```

```bash
python sysprog_args.py -i /home/ubuntu/input
```

### Стандартные потоки ввода-вывода

**Ввод-вывод данных**

Создайте файл с именем `sysprog_ioe_inout.py` и поместите в него следующий код

```python
import sys


def inout():
    """Input and output data"""
    
    # Option 1
    print("Enter any string", end=" >> ")
    in_data = input()
    print("Input data:", in_data)

    # Option 2
    # sys.stdout.write("Enter any string >> ")
    # sys.stdout.flush()
    # in_data = sys.stdin.readline()
    # sys.stdout.write("Input data: {}".format(in_data))


inout()
```

Запустите `sysprog_ioe_inout.py` в командной строке

```bash
python sysprog_ioe_inout.py
```

Отключения буфера

```bash
PYTHONUNBUFFERED=1 python sysprog_ioe_inout.py
```

```bash
python -u sysprog_ioe_inout.py
```

**Перенаправление потоков с использованием файлов**

- *Внешнее перенаправление*

Создайте файл с именем `sysprog_ioe_guess.py` и поместите в него следующий код

```python
def main():
    """Guess a random value."""
    import random
    while True:
        try:
            num = random.randint(0, 9)
            print("Enter any number from 0 to 9:")
            your_num = int(input())
            print("Your number is {} and actual one is {}".format(your_num, num))
            if num == your_num:
                print("Well done!")
                break
            else:
                print("Sorry, try again.")
        except:
            print("Bye bye!")
            break


main()
```

Запустите `sysprog_ioe_guess.py` в командной строке

```bash
python sysprog_ioe_inout.py
```

Создайте текстовый файл `sysprog_ioe_guess__input` со следующим содержанием:

```
1
3
6
2
3
5
1
4
```

Запустите `sysprog_ioe_guess.py` в командной строке с перенаправлением

```bash
python sysprog_ioe_inout.py < sysprog_ioe_guess__input
```

и так

```bash
python sysprog_ioe_inout.py < sysprog_ioe_guess__input > sysprog_ioe_guess__output
```

- *Внутреннее перенаправление*

Создайте файл с именем `sysprog_ioe_file.py` и поместите в него следующий код

```python
import sys
import time

# For in-memory in/out streams
# from io import StringIO, BytesIO


OUTPUT_FILE = "sysprog_ioe_file.log"
SCRIPT_NAME = sys.argv[0]

with open(OUTPUT_FILE, "a") as f:
    """Open a file to write output stream"""
    # sys.stdout = f
    # print("{}::{}::Hello".format(time.asctime(), SCRIPT_NAME))
    print("{}::{}::Hello".format(time.asctime(), SCRIPT_NAME), file=f)
```

Запустите `sysprog_ioe_file.py` в командной строке

```bash
python sysprog_ioe_file.py
```

- *Перенаправление ошибки*

Создайте файл с именем `sysprog_ioe_error.py` и поместите в него следующий код

```python
"""
Command to run:
    python sysprog_ioe_error.py 1>sysprog_ioe_error.log 2>sysprog_ioe_error.error.log
"""

import sys

print("Success")
print("Error", file=sys.stderr)
```

Запустите `sysprog_ioe_error.py` в командной строке

```bash
python sysprog_ioe_error.py 1>sysprog_ioe_error.log 2>sysprog_ioe_error.error.log
```

**Перенаправление потоков с использованием каналов**

Создайте файл с именем `sysprog_ioe_word.py` и поместите в него следующий код

```python
try:
    record = input()
    for word in record.split():
        print(word)
except EOFError:
    pass
```

Запустите `sysprog_ioe_word.py` в командной строке

```bash
python sysprog_ioe_word.py
```

Создайте файл с именем `sysprog_ioe_count.py` и поместите в него следующий код

```python
import sys

# Option 1
# for word in sys.stdin:
#     # print(repr(word))
#     print("Count", word.rstrip())

if sys.stdin.isatty():
    print("Count program uses console input")
else:
    print("Count program uses file or pipe")

counter = dict()

# Option 2, 3
while True:
    try:
        word = input()
        # word = sys.stdin.readline()[:-1]
        if not word:
            break
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1
    except EOFError:
        break

for key, value in sorted(counter.items(), key=lambda x: -x[1]):
    print("{}\t{}".format(key, value))
```

Запустите `sysprog_ioe_count.py` в командной строке

```bash
python sysprog_ioe_count.py
```

Создайте последовательность выполнения с использованием канала (pipe)

```bash
python sysprog_ioe_word.py | python sysprog_ioe_count.py 
```

```bash
echo "a s d f a a d" | python sysprog_ioe_word.py | python sysprog_ioe_count.py
```

### Завершение программы

Создайте файл с именем `sysprog_error.py` и поместите в него следующий код

```python
import sys


def main():
    sys.exit(127)   # raise the SystemExit exception


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        print("Something went wrong. Code error:", e)
```

Запустите `sysprog_error.py` в командной строке

```bash
python sysprog_error.py
```

## Модуль `os`

### Общие сведения

```python
import os
```

```python
help(os)
```

```python
# PID текущего процесса
os.getpid()
```

```python
# PID родительского процесса
os.getppid()
```

### Файловая система

**Создание файлов и каталогов**

```python
# TODO
```

**Отображение структуры каталога**

Создайте файл с именем `sysprog_fs_walk.py` и поместите в него следующий код

```python
import os
import sys


def main(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        print("path:", dirpath)
        for dirname in dirnames:
            print("\tdir:", dirname)
        for filename in filenames:
            print("\t\tfile:", filename)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        raise AttributeError("Wrong arguments are provided.")

```

Запустите `sysprog_fs_walk.py` в командной строке

```bash
python sysprog_fs_walk.py /home/ubuntu/assignment
```

**Поиск файла**

Создайте файл с именем `sysprog_fs_find.py` и поместите в него следующий код

```python
import os
import sys


def find(filename, root_path="/"):
    # go over all directories and files from the root to leaves in width
    for dpath, dnames, fnames in os.walk(root_path):
        for fname in fnames:
            if filename.lower() in fname.lower():
                yield os.path.join(dpath, fname)


def main(name, root_path):
    for found_file in find(name, root_path):
        print(found_file)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        raise AttributeError("Wrong arguments are provided.")

```

Запустите `sysprog_fs_find.py` в командной строке

```bash
python sysprog_fs_find.py output /home/ubuntu/assignment
```

**Удаление каталога**

Создайте файл с именем `sysprog_fs_delete.py` и поместите в него следующий код

```python
import os
import sys


def delete(directory):
    # list over all items (subdirectories and files) in a directory
    for name in os.listdir(directory):
        # compose a full path
        path = os.path.join(directory, name)
        # check whether path refers to a directory or not
        if os.path.isdir(path):
            delete(path)        # recursive call
        else:
            os.unlink(path)     # delete a file
    os.rmdir(directory)         # delete a directory


def main(directory):
    delete(directory)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        raise AttributeError("Wrong arguments are provided.")
```

Запустите `sysprog_fs_delete.py` в командной строке

```bash
python sysprog_fs_find.py $YOUR_DIR
```

### Переменные окружения

Создайте файл с именем `sysprog_env.py` и поместите в него следующий код

```python
import os


def main():
    """
    Environment variables example.
    """

    # List all environment variables
    print("All environment variables:\n", os.environ)

    # Check whether some variable exists or not
    print("Whether HELLO exists?\t", "HELLO" in os.environ)

    # Get an environment variable value if exists, otherwise return None
    print("Python process:\t HELLO={}".format(os.environ.get("HELLO")))

    # Assign a new value to the HELLO environment variable
    # Note: This assignment is scoped within current process and its child processes
    print("Reassign value:")
    os.environ["HELLO"] = "welcome"
    print("Python process:\t HELLO={}".format(os.environ.get("HELLO")))
    
    # Run a child process
    os.system('echo "Child process:\t HELLO=$HELLO"')


if __name__ == "__main__":
    main()

```

Запустите `sysprog_env.py` в командной строке

```bash
python sysprog_env.py 
```

```bash
# process-wide variable
HELLO=hello python sysprog_env.py
```

```bash
# shell-wide variable
export HELLO=hello \
    && echo -e "Shell process:\t HELLO=$HELLO" \
    && python sysprog_env.py \
    && echo -e "Shell process:\t HELLO=$HELLO"
```

### Рабочий каталог

Создайте файл с именем `sysprog_cwd.py` и поместите в него следующий код

```python
"""
Note: Run by two commands:
1) python sysprog_cwd.py
2) cd .. && python sysprog/sysprog_cwd.py && cd sysprog
"""

import os


def main():
    print(os.getcwd())


if __name__ == "__main__":
    main()
```

Запустите `sysprog_cwd.py` в командной строке

```bash
python sysprog_cwd.py
```

```bash
cd .. && python sysprog/sysprog_cwd.py && cd sysprog
```

### Запуск shell команд

Создайте файл с именем `sysprog_shell.py` и поместите в него следующий код

```python
import os

CODE = "echo 'hello'"

# Option 1
# run command and wait for it to complete
print(os.system("/bin/bash -c '{}'".format(CODE)))

# Option 2
import subprocess
# run command and continue execution
process = subprocess.Popen(["/bin/bash", "-c", CODE], stdout=subprocess.PIPE)
print(process)
out, err = process.communicate()
print(out.decode("utf-8").strip())

# Option 3
# run command and wait for result
process = subprocess.run(["/bin/bash", "-c", CODE], stdout=subprocess.PIPE)
print(process.stdout.decode("utf-8").strip())

# Option 4
# run command and wait for result
out = subprocess.check_output(["/bin/bash", "-c", CODE])
print(out.decode("utf-8").strip())
```

Запустите `sysprog_shell.py` в командной строке

```bash
python sysprog_shell.py
```

*Пример с подсчетом количества слов*

Создайте файл с именем `sysprog_shell_pipe.py` и поместите в него следующий код

```python
import subprocess


INPUT_FILE = "sysprog_ioe_count.txt"
CODE = "python sysprog_ioe_word.py | python sysprog_ioe_count.py"

with open(INPUT_FILE, "r") as f:
    out = subprocess.check_output(["/bin/bash", "-c", CODE], stdin=f)

# Word count pairs
out_text = out.decode("utf-8")[:-1]
wcount_pairs = out_text.split("\n")
print("Word count pairs:\n{}".format(wcount_pairs))

# Top word
if len(wcount_pairs) > 0:
    word, count = wcount_pairs[0].split("\t")
    print("Top word is {}".format(word))
```

Запустите `sysprog_shell_pipe.py` в командной строке

```bash
python sysprog_shell_pipe.py
```