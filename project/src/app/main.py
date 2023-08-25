from sqlalchemy import create_engine
from sqlalchemy.orm import Session

sys.path.append(sys.path[0] + '/..')
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS


#engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}', echo=True)
