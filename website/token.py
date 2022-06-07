from itsdangerous import URLSafeTimedSerializer

from main import app


def generate_confirmation_token(email):
    """generates a token using the want-to-be user email, encoded with SECRET_KEY"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email)


def confirm_token(token, expiration=3600):
    """decodes token (if it has not expired) into the email"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            max_age=expiration
        )
    except:
        return False
    return email
