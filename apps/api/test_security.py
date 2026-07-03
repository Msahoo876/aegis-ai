from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

print("=" * 60)

password = "StrongPassword123"

hashed = hash_password(password)

print("Original :", password)
print("Hashed   :", hashed)

print()

print(
    "Password Valid:",
    verify_password(
        password,
        hashed,
    ),
)

print()

token = create_access_token(
    subject="mahesh@example.com",
)

print("JWT Token:")
print(token)

print()

payload = decode_access_token(token)

print("Decoded Payload:")
print(payload)

print("=" * 60)