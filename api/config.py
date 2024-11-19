class Config:
    pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/tallercompu'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Debug:bool = True

config = {
    'development': DevelopmentConfig,
}