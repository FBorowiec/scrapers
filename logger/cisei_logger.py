import psycopg2


class LoggerDB:
    HOST = "database_pg"
    PORT = "5432"
    DB_NAME = "database_pg"
    USER = "postgres"
    PASSWORD = "postgres"

    def __init__(
        self, host=HOST, db_name=DB_NAME, port=PORT, user=USER, password=PASSWORD
    ) -> None:
        self.conn = psycopg2.connect(
            host=host, database=db_name, port=port, user=user, password=password
        )
        self.c = self.conn.cursor()

        self.create_person_info_table()

    def create_person_info_table(self):
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS person_info (
            id SERIAL PRIMARY KEY,
            idx TEXT NOT NULL,
            surname TEXT NOT NULL,
            full_name TEXT NOT NULL,
            age INT,
            trip_date DATE,
            registration_place TEXT,
            url TEXT,
            details JSONB);
            """
        )
        self.conn.commit()

    def add_person_info(self, person_info) -> None:
        with self.conn:
            self.c.execute(
                """
            INSERT INTO person_info DATA(
                id,
                idx,
                surname,
                full_name,
                age,
                trip_date,
                registration_place,
                url,
                details
            )
            VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s);
            """,
                (
                    person_info.idx,
                    person_info.surname,
                    person_info.full_name,
                    person_info.age,
                    person_info.trip_date,
                    person_info.registration_place,
                    person_info.url,
                    person_info.person_details,
                ),
            )

    def display_person_info(self, hours: int):
        with self.conn:
            self.c.execute(
                """
                SELECT
                    id,
                    idx,
                    surname,
                    full_name,
                    age,
                    trip_date,
                    registration_place,
                    url,
                    details
                FROM person_info
                ORDER BY registration_place;
                """
            )

            return self.c.fetchall()
