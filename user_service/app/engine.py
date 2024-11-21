
from sqlmodel import create_engine,Session


DATABASE_URL="postgresql://postgres:12345@localhost/postgres"

# DATABASE_URL="postgresql://postgres:12345@PostgresCont:5432/postgres"

connection = (DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)


engine=create_engine(connection)



def get_session():
    with Session(engine) as session:
        yield session