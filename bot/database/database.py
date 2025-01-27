import asyncio
import psycopg2

from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD


def connected_to_db(func):
    async def wrapper(*args, **kwargs):
        cursor, connection = await connected()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    username VARCHAR(256),
                    first_name VARCHAR(256),
                    last_name VARCHAR(256)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(256),
                    start_date TIMESTAMPTZ,
                    end_date TIMESTAMPTZ,
                    user_id BIGINT,
                    complete BOOL DEFAULT false,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id SERIAL PRIMARY KEY,
                    status BOOL DEFAULT false,
                    datetime TIMESTAMPTZ,
                    task_id INT NOT NULL UNIQUE,
                    FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
                );
            """)

            return await func(cursor, *args, **kwargs)
        except Exception as ex:
            print(ex)
        finally:
            cursor.close()
            connection.commit()
            connection.close()

    return wrapper


@connected_to_db
async def complete_task(curs, task_id):
    curs.execute(f"""
        UPDATE tasks
        SET complete = true
        WHERE id = {task_id}
    """)

    curs.execute(f"""
        UPDATE reminders
        SET status = true
        WHERE task_id = {task_id}
    """)


@connected_to_db
async def get_tasks_by_user_id(curs, user_id, status=False) -> list:
    curs.execute(f"""
        SELECT tasks.id, tasks.title, tasks.start_date, tasks.end_date, tasks.user_id, users.username, tasks.complete FROM tasks
        JOIN users ON users.id = tasks.user_id
        WHERE tasks.user_id = {user_id} AND tasks.complete = {status}
        ORDER BY start_date;
    """)
    rows = curs.fetchall()

    answer = []

    for row in rows:
        answer.append(
            {
                'task_id': row[0],
                'task_title': row[1],
                'task_start_date': row[2],
                'task_end_date': row[3],
                'user_id': row[4],
                'user_name': row[5],
                'status': row[6],
            }
        )

    return answer


@connected_to_db
async def add_task(curs, title, start, end, reminder, user_id):
    curs.execute(f"""
        INSERT INTO tasks (title, start_date, end_date, user_id)
        VALUES ('{title}', '{start}', '{end}', {user_id}) RETURNING id;
    """)
    task_id = curs.fetchall()[0][0]

    curs.execute(f"""
        INSERT INTO reminders (status, datetime, task_id)
        VALUES (false, '{reminder}', {task_id});
    """)


@connected_to_db
async def add_user(curs, user_id, username, first_name, last_name):
    curs.execute(f"""SELECT DISTINCT * FROM users WHERE id = {user_id}""")
    if not curs.fetchall():
        curs.execute(f"""
            INSERT INTO users (id, username, first_name, last_name)
            VALUES ({user_id}, '{username}', '{first_name}', '{last_name}');
        """)
    else:
        return "All ready exists"


@connected_to_db
async def check_time_complete(curs, time_now):
    curs.execute(f"""
        SELECT tasks.id, tasks.title, tasks.start_date, tasks.end_date, tasks.user_id, tasks.complete FROM tasks
        JOIN reminders ON reminders.task_id = tasks.id
        WHERE reminders.status = false AND reminders.datetime <= '{time_now}';
    """)

    rows = curs.fetchall()

    answer = []

    for row in rows:
        answer.append(
            {
                'task_id': row[0],
                'task_title': row[1],
                'task_start_date': row[2],
                'task_end_date': row[3],
                'user_id': row[4],
                'status': row[5],
            }
        )

        curs.execute(f"""
            UPDATE reminders
            SET status = true
            WHERE task_id = {row[0]};
        """)

    return answer


async def connected():
    connect = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    return connect.cursor(), connect


async def main():
    await add_task("Read the book", "2025-01-12 10:11:11", "2025-01-12 11:11:01", 5461886782)
    await get_tasks_by_user_id(5461886782)


if __name__ == "__main__":
    asyncio.run(main())
