import pymysql


def get_connection():
    """
    Creates and returns a MySQL database connection.
    """
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1505",
        database="entity_service_provider"
    )
