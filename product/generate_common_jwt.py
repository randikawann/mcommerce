import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'RanSecretKey_forAll10915'

def generate_common_token():
    payload = {
        'role': 'user',  # Static role for common users
        'exp': datetime.utcnow() + timedelta(days=7),  # Expiry in 7 days
        'iat': datetime.utcnow(),  # Issued at
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Print and store the token
COMMON_TOKEN = generate_common_token()
print(f"Common JWT Token: {COMMON_TOKEN}")