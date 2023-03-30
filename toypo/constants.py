import os
from dotenv import load_dotenv

load_dotenv()

SQL_ALCHEMY_URL = os.environ['SQL_ALCHEMY_URL']
AUTO_MIGRATE = os.getenv('AUTO_MIGRATE', 'False').lower() in ['true', '1']
