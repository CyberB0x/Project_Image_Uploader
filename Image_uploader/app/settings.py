import os

import dotenv

dotenv.load_dotenv('.env')
SERVER_ADDRESS = ('0.0.0.0', 8000)
STATIC_PATH = 'static/'
IMAGES_PATH = 'images/'
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
MAX_FILE_SIZE = 5 * 1024 * 1024
LOG_PATH = 'logs/'
LOG_FILE = 'app.log'
ERROR_FILE = 'upload_failed.html'

DB_NAME = os.getenv('DB_NAME') or 'postgres'
DB_USER = os.getenv('DB_USER') or 'postgres'
DB_PASSWORD = os.getenv('DB_PASSWORD') or 'postgres'
DB_HOST = os.getenv('DB_HOST') or 'db'
DB_PORT = os.getenv('DB_PORT') or '5432'


PAGE_LIMIT = 10