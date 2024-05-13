import sqlite3
import psycopg2
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, date


# Датаклассы для таблиц
@dataclass
class Filmwork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: date
    file_path: str
    rating: float
    type: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Person:
    id: uuid.UUID
    full_name: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class GenreFilmwork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PersonFilmwork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime = field(default_factory=datetime.now)


# Подключение к sqlite
sqlite_db = 'C:\\Users\\vanya\\Desktop\\sprint1\\sqlite_to_postgres\\db.sqlite'
conn1 = sqlite3.connect(sqlite_db)
curs1 = conn1.cursor()
curs1.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = curs1.fetchall()

# Запросы на взятие данных
curs1.execute(f"SELECT * FROM {tables[0][0]}")
data = curs1.fetchall()
data_genre = [Genre(*row) for row in data]

curs1.execute(f"SELECT * FROM {tables[1][0]}")
data = curs1.fetchall()
data_genre_fm = [GenreFilmwork(*row) for row in data]

curs1.execute(f"SELECT * FROM {tables[2][0]}")
data = curs1.fetchall()
data_person_fm = [PersonFilmwork(*row) for row in data]

curs1.execute(f"SELECT * FROM {tables[3][0]}")
data = curs1.fetchall()
data_person = [Person(*row) for row in data]

curs1.execute(f"SELECT * FROM {tables[4][0]}")
data = curs1.fetchall()
data_fm = [Filmwork(*row) for row in data]

curs1.close()
conn1.close()
# Подключение к postgresql
conn2 = psycopg2.connect(
    dbname='movies_db',
    user='Ivan',
    password='123qwe',
    host='localhost',
    port=5435
)
curs2 = conn2.cursor()


# Вставка данных в постгрес
def generator1(fw):
    yield (fw.id, fw.title,
           fw.description, fw.creation_date,
           fw.rating, fw.type, fw.created_at,
           fw.updated_at, fw.file_path)


def generator2(g):
    yield (g.id, g.name,
           g.created_at, g.updated_at)


def generator3(gf):
    yield (gf.id, gf.genre_id,
           gf.film_work_id, gf.created_at)


def generator4(p):
    yield (p.id, p.full_name,
           p.created_at, p.updated_at)


def generator5(pf):
    yield (pf.id, pf.person_id,
           pf.film_work_id, pf.role,
           pf.created_at)


insert_queries = ["INSERT INTO content.film_work VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                  "INSERT INTO content.genre VALUES (%s, %s, %s, %s)",
                  "INSERT INTO content.genre_film_work VALUES (%s, %s, %s, %s)",
                  "INSERT INTO content.person VALUES (%s, %s, %s, %s)",
                  "INSERT INTO content.person_film_work VALUES (%s, %s, %s, %s, %s)"
                  ]
if __name__ == '__main__':
    for fm in data_fm:
        try:
            curs2.executemany(insert_queries[0], generator1(fm))
        except:
            continue
    conn2.commit()
    for g in data_genre:
        try:
            curs2.executemany(insert_queries[1], generator2(g))
        except:
            continue
    conn2.commit()
    for gf in data_genre_fm:
        try:
            curs2.executemany(insert_queries[2], generator3(gf))
        except:
            continue
    conn2.commit()
    for p in data_person:
        try:
            curs2.executemany(insert_queries[3], generator4(p))
        except:
            continue
    conn2.commit()
    for pf in data_person_fm:
        try:
            curs2.executemany(insert_queries[4], generator5(pf))
        except:
            continue
conn2.commit()
curs2.close()
conn2.close()
