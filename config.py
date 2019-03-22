import os
basedir = os.path.abspath(os.path.dirname(__file__))
secret_key = "~Xl\x84A\x95\xec\xca\x0c\x18\x86`%\\\xef\xa0\xd8\tV\xd8\xc3\xf2\x1dd"
                                                                               
class Config(object):                                                         
    SECRET_KEY = os.environ.get('SECRET_KEY') or secret_key
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False