from pathlib import Path

SQLALCHEMY_DATABASE_URI = "postgresql://usr:pwd@127.0.0.1:5432/proximity_db"
PROJECT_ROOT_PATH = Path(__file__).parent.parent.parent.parent
