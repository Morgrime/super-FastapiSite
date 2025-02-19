# TODO связать данный тест с файлом аут.пу до тех пор пока не напишу автотесты
from utils.auth import create_access_token, verify_token
from datetime import timedelta

# Тестовые данные
data = {"sub": "testuser"}

# Создание JWT-токена
access_token_expires = timedelta(minutes=30)
access_token = create_access_token(data=data,
                                   expires_delta=access_token_expires)
print("Generated Token:", access_token)

# Проверка JWT-токена
payload = verify_token(access_token)
print("Decoded Payload:", payload)
