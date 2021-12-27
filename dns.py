from general import *

class Record:
    """Инициализация записи"""
    def __init__(self):
        self.name = None
        self.address = None

    """Задание имени записи"""
    def set_name(self, name):
        self.name = name

    """Задание адреса записи"""
    def set_address(self, address):
        self.address = address

    """Получение имени записи"""
    def get_name(self):
        return self.name

    """Получение адреса записи"""
    def get_address(self):
        return self.address

class Database:
    """Инициализация базы данных записей"""
    def __init__(self):
        self.records = {}

    """Проверка наличия записи в базе"""
    def check_record(self, name):
        if name in self.records:
            return True
        return False

    """Добавление записи в базу"""
    def add_record(self, record : Record):
        if self.check_record(record):
            self.delete_record(record.get_name())
        self.records[record.get_name()] = record.get_address()

    """Удаление записи из базы"""
    def delete_record(self, name):
        if self.check_record(name):
            self.records.pop(name)
        else:
            return "No record"

    """Проверка количества записей в базе"""
    def num_records(self):
        return len(self.records)

    """Резолв из базы данных по имени"""
    def resolve(self, name):
        if self.check_record(name):
            return self.records[name]
        return False

    """Формирование записи и запись записи в запись (запись)"""
    def form_record(self, name, address):
        record = Record()
        record.set_name(name)
        record.set_address(address)
        self.add_record(record)

class DnsRecursive(Service):
    """Инициализация рекурсивного DNS"""
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.dns = None
        self.set_name("DNS")

    """Задание DNS адреса сервису"""
    def set_dns(self, address):
        self.dns = address

    """Резолв записи из базы данных и рекурсивный поиск"""
    def resolve(self, name):
        if not self.db.resolve(name):
            return self.find(name)
        return self.db.resolve(name)

    """Рекурсивный поиск записи"""
    def find(self, name):
        if not self.dns:
            return "Unknown host"
        return self.get_host().get_interface().net.hosts[self.dns].services["DNS"].resolve(name)

    """Получение кода поиска (0 - нашел, 1 - не нашел)"""
    def get_code(self, name):
        return 0

class DnsNonRecursive(Service):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.dns = None
        self.set_name("DNS")

    """Задание DNS адреса сервису"""
    def set_dns(self, address):
        self.dns = address

    """Некурсивный поиск записи"""
    def resolve(self, name):
        if self.db.resolve(name):
            return self.db.resolve(name)
        return self.dns

    """Получение кода поиска (0 - нашел, 1 - не нашел)"""
    def get_code(self, name):
        if self.db.resolve(name):
            return 0
        return 1
