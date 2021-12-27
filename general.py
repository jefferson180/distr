class Message:
    """Инициализация сообщения"""
    def __init__(self):
        self.dst = None
        self.service = None
        self.data = None
    """Получить данные сообщения"""
    def get_data(self):
        return self.data

class Service:
    """Инициализация сервиса"""
    def __init__(self):
        self.host = None
        self.name = None

    """Задание имени сервиса"""
    def set_name(self, name):
        self.name = name

    """Получение имени сервиса"""
    def get_name(self):
        return self.name

    """Задание компьютера, на котором крутится сервис"""
    def set_host(self, host):
        self.host = host

    """Получение компьютера, на котором крутится сервис"""
    def get_host(self):
        return self.host

class NetworkInterface:
    """Инициализация сетевого интерфейса"""
    def __init__(self):
        self.net = None
        self.address = None
        self.dns = None

    """Резолв имени компьютера"""
    def local_resolve(self, address):
        return self.net.net_resolve(address)

    """Настройка сети для сетевого интерфейса и опрос сервера на сообщения"""
    def setNet(self, net, address):
        if self.net:
            self.disconnect()
        self.net = net
        self.address = address
        self.net.find_msg(self.address)

    """Установить DNS сервер"""
    def setDns(self, address):
        self.dns = address

    """Отключиться от сети"""
    def disconnect(self):
        if not self.net:
            return "No network"
        self.net.delete_host(self.address)
        self.net = None
        self.address = None

    """Получить адрес DNS сервера из сети"""
    def get_dns(self):
        if not self.net:
            return "No network"
        self.dns = self.net.pull_dns()

    """Пинг"""
    def ping(self, dst):
        if not self.net:
            return "No network"
        return self.net.ping(self.address, dst)

    """Отправить сообщение"""
    def send_msg(self, message : Message):
        if not self.net:
            return "No network"
        self.net.get_msg(message)

    """Найти сообщение в сети"""
    def find_msg(self):
        if not self.net:
            return "No network"
        return self.net.find_msg(self.address)

    """Резолв имени через DNS"""
    def resolve(self, name):
        if not self.dns:
            self.get_dns()
        return self.net.resolve(name, self.dns)

class Computer:
    """Инициализация компьютера"""
    def __init__(self, name):
        self.interface = NetworkInterface()
        self.name = name
        self.services = {}
        self.all_data = []

    """Получить сетевой интерфейс компьютера"""
    def get_interface(self):
        return self.interface

    """Получить имя компьютера"""
    def get_name(self):
        return self.name

    """Резолв имени компьютера в сети"""
    def local_resolve(self, address):
        return self.interface.local_resolve(address)

    """Пинг"""
    def ping(self, address):
        return self.interface.ping(address)

    """Установить сервис на компьютер"""
    def get_service(self, service : Service):
        self.services[service.get_name()] = service

    """Отправить сообщение"""
    def send_msg(self, message : Message):
        self.interface.send_msg(message)

    """Получить сообщение и записать его в хранилище"""
    def get_msg(self, message : Message):
        self.all_data.append(message)

    """Поиск сообщений в сети"""
    def find_msg(self):
        return self.interface.find_msg()

    """Сформировать сообщение и отправить его"""
    def form_msg(self, dst, service, data):
        msg = Message()
        msg.dst = dst
        msg.service = service
        msg.data = data
        self.send_msg(msg)

    """Резолв имени через DNS"""
    def resolve(self, name):
        return self.interface.resolve(name)

class Network:
    """Инициализация сети"""
    def __init__(self):
        self.hosts = {}
        self.dns = None
        self.msgs : dict[str, Message] = {}

    """Установить праймори DNS сервер для сети"""
    def set_dns(self, address):
        self.dns = address

    """Отдать адрес праймори DNS сервера интерфейсу"""
    def pull_dns(self):
        if not self.dns:
            return "No DNS"
        return self.dns

    """Добавить хост в сеть"""
    def add_host(self, computer : Computer, address):
        if address in self.hosts:
            return "Busy address"
        self.hosts[address] = computer
        computer.get_interface().setNet(self, address)

    """Удалить хост из сети"""
    def delete_host(self, address):
        self.hosts.pop(address)

    """Пинг"""
    def ping(self, src_address, dst_address):
        if dst_address in self.hosts:
            return f"Success ping from {src_address} to {dst_address}"
        return "Unknown host"

    """Получить количество хостов в сети"""
    def get_hosts_num(self):
        return len(self.hosts)

    """Резолв имени компьютера в сети"""
    def net_resolve(self, address):
        if address in self.hosts:
            return self.hosts[address].get_name()
        return "Unknown host"

    """Принять сообщение и передать его или запомнить"""
    def get_msg(self, message : Message):
        if message.dst in self.hosts:
            self.hosts[message.dst].get_msg(message)
            return
        self.msgs[message.dst] = message

    """Найти сообщение по запросу"""
    def find_msg(self, address):
        if address in self.msgs:
            self.hosts[address].get_msg(self.msgs[address])
            self.msgs.pop(address)
            return
        return "No messages"

    """Получить количество сохраненных в сети сообщений"""
    def num_msgs(self):
        return len(self.msgs)

    """Резолв имени через DNS"""
    def resolve(self, name, dns):
        if not dns:
            return "Unknown host"
        status = self.hosts[dns].services["DNS"].get_code(name)
        if (status == 1):
            return self.resolve(name, self.hosts[dns].services["DNS"].resolve(name))
        return self.hosts[dns].services["DNS"].resolve(name)
