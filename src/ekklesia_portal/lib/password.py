from passlib.context import CryptContext

password_context = CryptContext(
    # use plaintext only for tests!!!
    schemes=['pbkdf2_sha256', 'plaintext'],
    deprecated="auto"
)
