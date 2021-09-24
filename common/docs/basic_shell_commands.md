# Основные команды в Ubuntu
Сергей Папулин (papulin_bmstu@mail.ru)

Содержание

- [Образ Ubuntu](#Образ-Ubuntu)
- [Файловая система](#Файловая-система)
    - [Отображение содержимого каталогов](#Отображение-содержимого-каталога)
    - [Управление файлами и каталогами](#Управление-файлами-и-каталогами)
    - [Управление пользователями и группами](#Управление-пользователями-и-группами)
    - [Права доступа](#Права-доступа)
    - [Монтирование устройства хранения данных](#Монтирование-устройства-хранения-данных)
- [Процессы](#Процессы)
- [Менеджер пакетов `apt`](#Менеджер-пакетов-apt)
- [Загрузка файлов посредством `wget`](#Загрузка-файлов-посредством-wget)
- [Архиватор](#Архиватор)
    - [`tar`](#tar)
    - [`zip`/`unzip`](#zip/unzip)
- [Управление сетью](#Управление-сетью)
    - [Настройка сети посредством `netplan`](#Настройка-сети-посредством-netplan)
    - [Отслеживание состояния сети](#Отслеживание-состояния-сети)
        - [`ip addr`](#ip-addr)
        - [`ip link`](#ip-link)
        - [`ip neighbor`](#ip-neighbor)
        - [`ip route`](#ip-route)
    - [Контроль трафика](#Контроль-трафика)
        - [`iptables`](#iptables)
        - [`ufw`](#ufw)
    - [Мониторинг соединений](#Мониторинг-соединений)
        - [`ss`](#ss)
        - [`lsof`](#lsof)
        - [`nc`](#nc)
    - [Удаленный доступ](#Удаленный-доступ)
        - [`ssh`](#ssh)
        - [`scp`](#scp)


## Образ Ubuntu

[Ссылка на образ](https://disk.yandex.ru/d/0Hd92rzNB0_IHg)

Установленное ПО:
- Ubuntu 18
- Java (JDK) 8
- Hadoop 3.1.2
- Spark 2.4.7
- Zookeeper 3.6.1
- Kafka 2.5.1
- Anaconda3-2020.02 (`python 3.7`). Note: `python 3.8` is not supported by Spark 2.4.7

Пароль: `ubuntu`

Для доступа к общим каталогам на виртуалке необходимо добавить пользователя `ubuntu` в группу `vboxsf`:

```bash
sudo adduser $USER vboxsf
```

## Справка

```bash
man ls
```

## Файловая система

### Отображение содержимого каталога

Путь к файлу/каталогу:


- `/home/ubuntu` - абсолютный путь
- `BigData/Spark` - относительный путь
- `~` - домашняя директория пользователя (например, `/home/ubuntu` для пользователя c именем `ubuntu`)
- `..` - родительская директория текущего каталога

Выбор текущей рабочей директории

```bash
cd /home/ubuntu
```

```bash
cd ~
```

```bash
cd ~/BigData
```

```bash
cd BigData
```

```bash
cd ..
```

Просмотр содержимого каталога

```bash
ls /
```

```bash
ls
```

```bash
ls -lha
```

```bash
ls -Rlha
```

Установка утилиты отображения дерева каталогов

```bash
sudo apt install tree
```

Просмотр содержимого каталога

```bash
tree -L 2 /home/ubuntu
```


## Управление файлами и каталогами


Создание каталога

```bash
mkdir class
```

```bash
cd class
```

Создание файла

```bash
touch welcome.md
ls -l
```

Добавление содержания

```bash
echo "Hello World!" > welcome.md
```

Отображение содержимого файла

```bash
cat welcome.md
```

```bash
echo "second line" >> welcome.md
cat welcome.md
```

Редактор

```bash
nano welcome.md
```

Копирование

```
cd ..
cp -R class class_copy
tree -L 2 ~
```

Перемещение

```
mkdir class_move
mv class/welcome.md class_move/
tree -L 2 ~
```

Переименование каталога и файла

```
mv class_move class_rename
mv class_rename/welcome.md class_rename/hello.md
tree -L 2 ~
```

Удаление

```
rm -R class class_rename
tree -L 2 ~
```
```
mv class_copy class
```

Ссылки

*Hard link* (только на файлы)

```bash
cd class
ln welcome.md hello.md
ls -l welcome.md hello.md

# изменение содержания welcome.md
echo "content" >> welcome.md
cat hello.md 

# изменение содержания hello.md
echo "more" >> hello.md 
cat welcome.md

rm welcome.md
ls -l
rm hello.md
```

*Soft link*

```bash
# создание soft link
echo "Hello World 1.0" >> welcome_1.0.md
ln -s welcome_1.0.md welcome.md
cat welcome.md
ls -l

# замена ссылки на файл
echo "Hello World 1.1" >> welcome_1.1.md
ln -sfn welcome_1.1.md welcome.md
cat welcome.md
ls -l

echo "updated" >> welcome.md
cat welcome_1.1.md

rm welcome_1.1.md
ls -l

rm welcome.md welcome_1.0.md
```


## Управление пользователями и группами

Вывод пользователей

```bash
cat /etc/passwd
```

```bash
less /etc/passwd
```

1. Имя пользователя
2. Пароль 
3. UID
4. GID (первичная группа)
5. Полное имя
6. Домашний каталог
7. Вход в shell

Текущие пользователи в системе

```bash
users
```

Вывод групп
```bash
cat /etc/group
```

1. Имя группы
2. Пароль
3. GID
4. Пользователи группы


Группы текущего пользователя

```bash
groups $USER
```

Идентификаторы пользователя

```bash
id $USER
```

Создание пользователя

```bash
sudo adduser anotheruser
```

```bash
getent passwd anotheruser
```

```bash
id anotheruser
```

Вход под новым пользователем

```
su -l anotheruser
```

Выход

```bash
exit
```

Создание группы

```bash
sudo addgroup anothergroup
```

```bash
getent group anothergroup
```

Добавление пользователя в группу

```bash
sudo adduser ubuntu anothergroup
```

или

```bash
usermod -aG anothergroup ubuntu
```

```bash
groups ubuntu
```

Удаление группы

```bash
sudo delgroup anothergroup
```

Удаление пользователя

```bash
sudo deluser anotheruser
```

```
ls /home
```

Для удаления пользовательских данных можно использовать следующие параметры: 

`--remove-home` или `--remove-all-files`

```
sudo rm -R /home/anotheruser/
```

## Права доступа

Создание файла

```bash
echo "Hello World" >> welcome.md
ls -l
```

Создание пользователей

```
sudo adduser alex
sudo adduser kate
```


```bash
# Откройте новую терминальную вкладку для пользователя alex

su -l alex
cat /home/ubuntu/class/welcome.md
echo "alex" >> /home/ubuntu/class/welcome.md
# exit
```

#### Права на запись всем пользователям

```bash
chmod o+w welcome.md
```

```bash
chmod 646 welcome.md
```

- `1` - выполнение (`x`)
- `2` - запись (`w`)
- `4` - чтение (`r`)

- Например: `x` + `w` + `r` = `7`

Параметр `-R` для рекурсивного применения команды

```bash
# Вкладка пользователя alex

echo "alex" >> /home/ubuntu/class/welcome.md
cat /home/ubuntu/class/welcome.md
```

```bash
chmod o-w welcome.md
```

или

```bash
chmod 644 welcome.md
```

#### Создание общей группы пользователей

```bash
sudo addgroup student
sudo adduser ubuntu student
sudo adduser alex student
```

```bash
# Пользователь ubuntu
chmod g+w welcome.md
sudo chown ubuntu:student welcome.md
ls -l welcome.md
```


```bash
# Вкладка пользователя alex
echo "alex" >> /home/ubuntu/class/welcome.md
```


```bash
# Вкладка пользователя kate
echo "kate" >> /home/ubuntu/class/welcome.md
```


```bash
chgrp ubuntu welcome.md 
```

```bash
rm welcome.md
delgroup student
deluser alex
deluser kate
```

Исполняемые файлы

```bash
echo 'echo "User name: $USER"' > script.sh
chmod u+x script.sh
ls -l script.sh 
./script.sh
```

## Монтирование устройства хранения данных

Список подключенных блочных устройств

```
lsblk
```

Отображение списка устройств (для определения типа файловой системы внешнего USB носителя)

```
sudo lshw | less
```

Создаем каталог, к которому будет подключено содержания носителя

```
sudo mkdir /media/pendrive
```

Монтируем к каталогу

```
sudo mount -t ntfs -o umask=0022,gid=1000,uid=1000 /dev/sdb1 /media/pendrive
```

Чтобы отменить монтирования, используется следующая команда

```
sudo umount /media/pendrive
```


## Процессы

Отслеживание выполнения процессов и потребляемых ими ресурсов

```
top
```


Список процессов

```
ps aux
```

Дерево процессов

```
pstree -p
```

Дерево процессов для текущего пользователя

```
pstree -p $USER
```

Java процессы

```bash
jps
```


```
sudo ls /proc
```

```
sudo kill $PID
```

## Менеджер пакетов `apt`

Получение обновленной актуальной информации о пакетах в репозиториях

```
sudo apt update
```

Установка пакетов

```
sudo apt install tree 
```

```bash
sudo apt install ${FILE.deb}
```

Обновление пакетов (не надо сейчас запускать)

```
sudo apt upgrade
```

```
sudo apt install --only-upgrade PACKAGE_NAME
```

Список установленных пакетов

```
dpkg --list
```

Удаление пакета

```
sudo apt remove tree 
```

Удаление пакета со всеми конфигурационными файлами

```
sudo apt purge tree 
```

Очистка кэша локального репозитория от ранее полученных файлов (`/var/cache/apt/archives/`)

```
ls /var/cache/apt/archives/
```

```
sudo du -h /var/cache/apt/archives/
```

```
sudo apt clean
```

```
sudo du -h /var/cache/apt/archives/
```

Удаление невостребованных системой пакетов

```
sudo apt autoremove
```


## Загрузка файлов посредством `wget`

```
wget -P ~/Downloads https://mail.ru 
```

```
cat ~/Downloads/index.html | less
```


## Архиватор

### `tar`

Создание архива

```bash
tar -cvJ -f ${ARCHIVE.tar.xz} $SOURCE
```

Распаковка архива

```bash
tar -xv -f ${ARCHIVE.tar.xz} --directory $DESTINATION --strip-components 1
```

### `zip`/`unzip`

Создание архива

```bash
zip ${ARCHIVE.zip} -r $SOURCE
```

Распаковка архива

```bash
unzip ${PATH_TO_ZIP.zip} -d $DESTINATION
```


## Управление сетью

### Настройка сети посредством `netplan`

```bash
cat /etc/network/interfaces

# ifupdown has been replaced by netplan(5) on this system.  See
# /etc/netplan for current configuration.
# To re-enable ifupdown on this system, you can run:
#    sudo apt install ifupdown
```

Конфигурация сети

```bash
ls -l /etc/netplan/
cat /etc/netplan/01-netcfg.yaml 
```


Параметры сети, полученные от DHCP сервера:

```
netplan ip leases eth0
```

или


```bash
ls -l /var/lib/NetworkManager

cat /var/lib/NetworkManager/${DHCP_CLIENT.lease}
```

```bash
# TODO: change dns server
```

### Отслеживание состояния сети

#### `ip addr`

IP адреса по всем интерфейсам

```bash
ip addr
```

IP адрес на интерфейсе `eth0`

```bash
ip addr show eth0
```

#### `ip link`

Интерфейсы (MAC адреса)

```bash
ip link
```

Отключение/включение интерфейса `eth0`

```bash
sudo ip link set eth0 down
```

```bash
sudo ip link set eth0 up
```

#### `ip neighbour`


ARP таблица

```
ip neighbour
```

#### `ip route`

Таблица маршрутизации

```
ip route
```

### Контроль трафика

#### `iptables`

Перенаправление запроса

```
sudo iptables -t nat -A OUTPUT -d 217.69.139.200 -j DNAT --to-destination 173.194.73.94
```

```bash
sudo iptables -t nat -S
```

```bash
sudo iptables -t nat -L OUTPUT -n
```

```bash
sudo iptables  -t nat -D OUTPUT 1
```

#### `ufw`


```bash
# TODO: ufw
```

### Мониторинг соединений

#### `ss`

Отображение информации о сокетах

```
sudo ss -tuan
```
- `a` - все сокеты
- `l` - только сокеты в состоянии прослушивания (listening)
- `t` - tcp
- `u` - udp
- `n` - числовые значения хостов и портов
- `p` - показывать процессы
- `e` - подробная информация по сокетам

```
sudo ss -tuln
```

#### `lsof`

IP соединения

```
sudo lsof -i -P -n
```

```
sudo ss -tulnp
```

#### `nc`

```bash
nc -zv localhost 1-1000
```

```bash
nc -zv localhost 22
```

```bash
nc -l -p 23
```

```bash
nc localhost 23
```

### Удаленный доступ

#### `ssh`

```
ssh USERNAME@HOST -p 22
```

```
ssh-keygen -t rsa -P '' -f $HOME/.ssh/id_rsa
```

```
ssh-copy-id -i $HOME/.ssh/id_rsa_alex.pub USERNAME@HOST
```

```
ssh -i ~/.ssh/id_rsa USERNAME@HOST
```

#### `scp`

Копирование файла на удаленный узел

```bash
scp -P 22 -i $HOME/.ssh/id_rsa_alex $FILE USERNAME@HOST:$REMOTE_DIR
```

Копирование файла на локальный узел

```bash
scp -i $HOME/.ssh/id_rsa_alex USERNAME@HOST:$FILE $LOCAL_DIR
```

Копирование каталога на удаленный узел 

```bash
scp -r -i $HOME/.ssh/id_rsa_alex $LOCAL_DIR USERNAME@HOST:$REMOTE_DIR
```


