import psycopg2
from django.db import connections


class CustomRouter:
    def db_for_read(self, model, **hints):
        """
        Determines which database to read from.
        """
        # Check if the primary database is accessible, return the secondary if not.
        if not self.is_database_accessible('default'):
            return 'secondary'
        return None  # Use the default database

    def db_for_write(self, model, **hints):
        """
        Determines which database to write to.
        """
        # Check if the primary database is accessible, return the secondary if not.
        if not self.is_database_accessible('default'):
            return 'secondary'
        return None  # Use the default database

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between objects in different databases.
        """
        # Allow relations if both objects are in the same database
        if obj1._state.db != obj2._state.db:
            return False
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Controls if a migration operation is allowed to run on a particular database.
        """
        # Allow migrations on all databases
        return True

    def is_database_accessible(self, db_name):
        """
        Checks if the primary database is accessible.
        """
        try:
            # Attempt to connect to the default database
            # You can use any method you prefer to check the database connection here
            # For example, you can use Django's database connection handler
            # Replace 'default' with the name of your default database
            connections[db_name].ensure_connection()
            return True
        except psycopg2.OperationalError:
            return False
