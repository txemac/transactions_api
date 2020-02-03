from database import User
from database.schemas import UserPost


def test_user_create_ok(session, data_user):
    count1 = session.query(User).count()
    data = UserPost(
        name=data_user['name'],
        email=data_user['email'],
        age=data_user['age'],
    )
    User.create(
        db_session=session,
        data=data
    )
    count2 = session.query(User).count()
    assert count1 + 1 == count2


def test_user_get_users_empty(session):
    assert len(User.get_users(db_session=session)) == 0


def test_user_get_users_ok(session, new_user):
    assert len(User.get_users(db_session=session)) == 1


def test_user_get_user_by_name_empty(session):
    assert User.get_user_by_name(db_session=session, name='not_exists') is None


def test_user_get_user_by_name_ok(session, new_user):
    assert User.get_user_by_name(db_session=session, name=new_user.name) is not None


def test_user_get_user_by_email_empty(session):
    assert User.get_user_by_email(db_session=session, email='not_exists') is None


def test_user_get_user_by_email_ok(session, new_user):
    assert User.get_user_by_email(db_session=session, email=new_user.email) is not None
