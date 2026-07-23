

def create_test_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );
    """)

    connection.commit()

    cursor.close()
    
def insert_test_user(connection, name):
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO test_users(name)
        VALUES (%s)
        RETURNING id;
        """,
        (name,)
    )

    user_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()

    return user_id