class DatabasesRouter:
    """
    Un router para controlar en qué base de datos se almacenan los modelos específicos.
    """

    def db_for_read(self, model, **hints):
        """
        Intenta leer modelos particulares desde una base de datos específica.
        """
        if model._meta.app_label == "vote":
            return "mongo_db"
        return "default"

    def db_for_write(self, model, **hints):
        """
        Intenta escribir modelos particulares en una base de datos específica.
        """
        if model._meta.app_label == "vote":
            return "mongo_db"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Determina si se permite una relación entre dos objetos.
        """
        if obj1._state.db in ("mongo_db", "default") and obj2._state.db in (
            "mongo_db",
            "default",
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Asegura que los modelos de una aplicación específica solo se migren a una base de datos.
        """
        if app_label == "vote":
            return db == "mongo_db"
        return db == "default"
