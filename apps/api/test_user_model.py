from app.models.user import User

print(User.__tablename__)

print(User.metadata.tables.keys())