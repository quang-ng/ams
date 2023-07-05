import os
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

ENV = env('ENV')

print("ENV: ", ENV)
if ENV == 'production':
    from .conf.production.settings import *
else:
    from .conf.development.settings import *
