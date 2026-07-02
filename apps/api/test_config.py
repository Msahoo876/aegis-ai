from app.core.config import settings

print("=" * 60)
print("Aegis AI Configuration")
print("=" * 60)

print(f"App Name          : {settings.APP_NAME}")
print(f"Version           : {settings.APP_VERSION}")
print(f"Environment       : {settings.ENVIRONMENT.value}")
print(f"Debug             : {settings.DEBUG}")

print()

print(f"Database          : {settings.DATABASE_URL}")
print(f"Redis             : {settings.REDIS_URL}")

print()

print(f"LLM Provider      : {settings.LLM_PROVIDER.value}")
print(f"Default Model     : {settings.DEFAULT_MODEL}")
print(f"Embedding Model   : {settings.EMBEDDING_MODEL}")

print()

print(f"OpenAI Key        : {'Loaded' if settings.OPENAI_API_KEY else 'Missing'}")
print(f"Claude Key        : {'Loaded' if settings.ANTHROPIC_API_KEY else 'Missing'}")
print(f"Gemini Key        : {'Loaded' if settings.GEMINI_API_KEY else 'Missing'}")

print("=" * 60)