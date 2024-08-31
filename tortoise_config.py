TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.models.dbModels", "aerich.models"],
            "default_connection": "default",
        },
    },
}