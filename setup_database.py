import psycopg2
import os

def connect_db():
    """Connect to the specified PostgreSQL database."""
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def create_tables():
    """Create tables in the PostgreSQL database."""
    command = (
        """
        CREATE TABLE IF NOT EXISTS trips (
            id SERIAL PRIMARY KEY,
            destination VARCHAR(255),
            departure_date DATE,
            return_date DATE,
            activities TEXT,
            accommodation VARCHAR(255),
            plan_details TEXT
        )
        """
    )
    conn = connect_db()
    try:
        cur = conn.cursor()
        cur.execute(command)
        conn.commit()  # Commit the transaction
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"An error occurred: {error}")
    finally:
        if conn is not None:
            conn.close()

def insert_trip(destination, departure_date, return_date, activities, accommodation, plan_details):
    """Insert a new trip into the trips table."""
    sql = """INSERT INTO trips(destination, departure_date, return_date, activities, accommodation, plan_details)
             VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;"""
    conn = connect_db()
    try:
        cur = conn.cursor()
        cur.execute(sql, (destination, departure_date, return_date, activities, accommodation, plan_details))
        trip_id = cur.fetchone()[0]
        conn.commit()
        print(f"Trip added with ID: {trip_id}")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"An error occurred: {error}")
        if conn:
            conn.rollback()  # Rollback transaction on error
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_tables

