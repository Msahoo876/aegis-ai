from app.schemas.user import UserCreate

user = UserCreate(
    email="mahesh@example.com",
    username="mahesh",
    full_name="Mahesh Kumar Sahoo",
    password="StrongPassword123",
)

print(user)