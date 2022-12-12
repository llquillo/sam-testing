import psycopg2
from os import environ
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database():
    _conn = None
    _cursor = None
    _engine = None
    _session = None

    def __init__(self):
        url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
            environ.get('DB_USER'), environ.get('DB_PASSWORD'),
            environ.get('DB_HOST'), environ.get('DB_PORT', '5432'),
            environ.get('DB_NAME'))

        self._engine = create_engine(url, echo=True)
        self.create_session()

    def create_session(self):
        Session = sessionmaker(self._engine)
        self._session = Session()
