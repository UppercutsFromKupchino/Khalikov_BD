class Config:
    dialect = 'postgresql'
    username = 'rrdeovwjqjhhda'
    password = '02a48529de6ac74049077e4b631afb9a605141027a08d87beb88e56bb0a1c75b'
    host = 'ec2-63-32-30-191.eu-west-1.compute.amazonaws.com'
    db_name = 'df6tk79tjmp5ch'

    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'zxc-pudge'
