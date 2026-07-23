from DB_SetUp import connect
from logging_config import logger

def main():
    conn = None

    try:
        conn = connect()

    finally:
        if conn:
            conn.close()
            logger.info("Connection closed.")

if __name__ == "__main__":
    main()