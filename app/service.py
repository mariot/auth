from app.abstract_model_service import AbstractModelService
from app.models import User


class UserService(AbstractModelService):
    _model = User
