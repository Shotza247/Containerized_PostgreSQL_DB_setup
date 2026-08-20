from DB_SetUp import PostgresDB
from models.customer import Customer
from repository import customers_repo


class CustomerService:
    def __init__(self, db: PostgresDB | None = None) -> None:
        self.db = db or PostgresDB()

    def create_customer(
        self,
        customer_code: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str | None = None,
        city: str | None = None,
    ) -> Customer:
        self._validate_customer(customer_code, first_name, last_name, email)

        with self.db.connection() as connection:
            customer_id = customers_repo.create_customer(
                connection,
                customer_code,
                first_name,
                last_name,
                email,
                phone,
                city,
            )
            customer = customers_repo.get_customer_by_id(connection, customer_id)

        return customer

    def get_customer_by_code(self, customer_code: str) -> Customer | None:
        with self.db.connection() as connection:
            return customers_repo.get_customer_by_code(connection, customer_code)

    def list_customers(self) -> list[Customer]:
        with self.db.connection() as connection:
            return customers_repo.list_customers(connection)

    def update_customer(
        self,
        customer_code: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str | None = None,
        city: str | None = None,
    ) -> Customer | None:
        self._validate_customer(customer_code, first_name, last_name, email)

        with self.db.connection() as connection:
            updated = customers_repo.update_customer(
                connection,
                customer_code,
                first_name,
                last_name,
                email,
                phone,
                city,
            )
            if not updated:
                return None

            return customers_repo.get_customer_by_code(connection, customer_code)

    def delete_customer(self, customer_code: str) -> bool:
        with self.db.connection() as connection:
            return customers_repo.delete_customer(connection, customer_code)

    def _validate_customer(
        self,
        customer_code: str,
        first_name: str,
        last_name: str,
        email: str,
    ) -> None:
        if not customer_code.strip():
            raise ValueError("Customer code is required.")
        if not first_name.strip():
            raise ValueError("First name is required.")
        if not last_name.strip():
            raise ValueError("Last name is required.")
        if "@" not in email:
            raise ValueError("A valid customer email is required.")
