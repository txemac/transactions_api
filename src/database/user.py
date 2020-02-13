from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Session

import database
from database.schemas import UserPost


class User(database.Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    dt_created = Column(DateTime, default=func.now(), nullable=False)

    def __init__(
            self,
            name: str,
            email: str,
            age: int,
    ):
        self.name = name
        self.email = email
        self.age = age

    @classmethod
    def create(
            cls,
            db_session: Session,
            data: UserPost,
    ):
        """
        Create a new user.

        :param Session db_session: database session
        :param UserPost data: data
        :return User: user
        """
        user = User(name=data.name, email=data.email, age=data.age)

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        return user

    @classmethod
    def get_users(
            cls,
            db_session: Session,
    ):
        """
        Get all users.

        :param Session db_session: database session
        :return List[User]: list of users
        """
        return db_session.query(User).all()

    @classmethod
    def get_user_by_name(
            cls,
            db_session: Session,
            name: str,
    ):
        """
        Get an user by name.

        :param Session db_session: database session
        :param str name: name of the user
        :return User: user
        """
        return db_session.query(cls).filter(User.name == name).first()

    @classmethod
    def get_user_by_email(
            cls,
            db_session: Session,
            email: str,
    ):
        """
        Get an user by email.

        :param Session db_session: database session
        :param str email: email of the user
        :return User: user
        """
        return db_session.query(cls).filter(User.email == email).first()
