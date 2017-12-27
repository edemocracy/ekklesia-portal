from passlib.context import CryptContext

password_context = CryptContext(
    # use plaintext only for tests!!!
    schemes=['bcrypt', 'plaintext'],
    deprecated="auto"
)