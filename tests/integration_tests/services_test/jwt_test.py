from src.config import Settings, settings
from src.services.jwt_token_services import JWTService


def test_jwt_services():
    jwt_service = JWTService(config=settings)
    user_id = 1
    token = jwt_service.create_jwt(user_id)
    validated_user_id = jwt_service.check_jwt(token)
    assert user_id == validated_user_id


