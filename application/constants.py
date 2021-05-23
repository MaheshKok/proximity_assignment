from pathlib import Path

SQLALCHEMY_DATABASE_URI = (
    "postgresql://nuffsaid_usr:nuffsaid_pwd@127.0.0.1:5432/nuffsaid_db"
)
PROJECT_ROOT_PATH = Path(__file__).parent.parent.parent.parent
