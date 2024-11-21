from sqlmodel import Field, SQLModel, create_engine, Session, select


class user_data(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    department: str
    Semester: str
    section: str
    password: str
    email: str
