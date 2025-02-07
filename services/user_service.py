from models.user import User


class UserService:

    @staticmethod
    def create_user(first_name, last_name, email, password):
        if User.query.filter_by(email=email).first():
            return None

        new_user = User(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        new_user.save()

        return new_user

    @staticmethod
    def get_user_by_id(user_id):
        return User.get_active().filter_by(id=user_id).first()

    @staticmethod
    def get_user_by_email(email):
        return User.get_active().filter_by(email=email).first()

    @staticmethod
    def authenticate_user(email, password):
        user = User.get_active().filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def update_user(user_id, first_name=None, last_name=None, email=None):
        user = User.get_active().filter_by(id=user_id).first()
        if not user:
            return None

        update_data = {}
        if first_name:
            update_data["first_name"] = first_name
        if last_name:
            update_data["last_name"] = last_name
        if email and not User.query.filter_by(email=email).first():
            update_data["email"] = email

        user.update(update_data)
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.get_active().filter_by(id=user_id).first()
        if not user:
            return None

        user.soft_delete()
        return user

    @staticmethod
    def get_all_users():

        return User.get_active().all()
