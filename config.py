from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))

SECRET_KEY = 'flask-session-insecure-secret-key'
HEROKU_POSTGRESQL_BRONZE_URL: postgres://hifkqqwroxekcq:6n7nk8jcTBabEa-iafiRt66af-@ec2-54-235-193-41.compute-1.amazonaws.com:5432/ddo318ms4vifff
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'keeper.db')
# SQLALCHEMY_ECHO = True