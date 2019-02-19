class Config:
    DATABASE_USER = ''
    DATABASE_PASSWORD = ''
    DATABASE_DB = ''
    DATABASE_HOST = ''
    DATABASE_PORT = 3306

    SECRET_KEY = ''

    BLIZZARD_CLIENT_KEY = ''
    BLIZZARD_SECRET_KEY = ''

key = Config.SECRET_KEY
blz_client_key = Config.BLIZZARD_CLIENT_KEY
blz_secret_key = Config.BLIZZARD_SECRET_KEY