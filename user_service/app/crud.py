from sqlmodel import Field, SQLModel, create_engine, Session, select
from models import user_data


def get_all_users(session: Session):
        users = session.exec(select(user_data)).all()
        return users
    

def get_user_by_id(session: Session, user_id: int):
    user = session.exec(select(user).where(user.id == user_id)).first()
    return user
    

def create_user(session: Session, user: user_data):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def check_user_credentials(session: Session, username: str, password: str):
    user = session.exec(select(user_data).where(user_data.username == username)).first()
    if user is None:
        return False
    if user.password != password:
        return False
    return user