from decouple import config


class Config:
    def __init__(self):
        self.database = DatabaseConfig()
        self.telegram = TelegramConfig()
        self.rabbitmq = RabbitMQConfig()


class DatabaseConfig:
    def __init__(self):
        self.host = config("DB_HOST")
        self.port = config("DB_PORT")
        self.username = config("DB_USERNAME")
        self.password = config("DB_PASSWORD")
        self.db_name = config("DB_NAME")


class TelegramConfig:
    def __init__(self):
        self.token = config("TG_TOKEN")


class RabbitMQConfig:
    def __init__(self):
        self.login = config("RMQ_LOGIN")
        self.password = config("RMQ_PASSWORD")
        self.host = config("RMQ_HOST")
