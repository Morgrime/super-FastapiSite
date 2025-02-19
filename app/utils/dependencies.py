from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from utils.auth import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# проверка на вшивость (авторизован чел или нет)
def get_current_user(token: str = Security(oauth2_scheme)):
    # получение текущего пользователя на основе JWT
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return payload
