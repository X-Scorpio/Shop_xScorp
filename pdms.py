import sqlite3

DB_NAME = 'myshop.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def init_tables():
    init_product_table()
    init_user_table()

def init_product_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    sql = """
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            qty INTEGER NOT NULL
        )
    """
    c.execute(sql)
    conn.commit()
    conn.close()

def add_product(conn, name, price, qty):
    c = conn.cursor()
    sql = """
        INSERT INTO products (name, price, qty)
        VALUES (?, ?, ?)
    """
    c.execute(sql, (name, price, qty))
    conn.commit()

def get_product(conn, id):
    c = conn.cursor()
    sql = """
        SELECT id, name, price, qty FROM products WHERE id = ?
    """
    c.execute(sql, (id,))
    return c.fetchone()

def get_products(conn):
    c = conn.cursor()
    sql = """
        SELECT id, name, price, qty FROM products
    """
    c.execute(sql)
    return c.fetchall()

def remove_product(conn, id):
    c = conn.cursor()
    sql = """
        DELETE FROM products WHERE id = ?
    """
    c.execute(sql, (id,))
    conn.commit()

def update_product(conn, id, name, price, qty):
    c = conn.cursor()
    sql = """
    UPDATE products
        SET name = ?,
            price = ?,
            qty = ?
        WHERE id = ?
    """
    c.execute(sql, (name, price, qty, id))
    conn.commit()


def init_user_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    sql = """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            email REAL UNIQUE NOT NULL,
            password INTEGER NOT NULL
        )
    """
    c.execute(sql)
    conn.commit()
    conn.close()

def add_user(conn, name, email, password):
    c = conn.cursor()
    sql = """
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
    """
    c.execute(sql, (name, email, password))
    conn.commit()

def get_user(conn, id):
    c = conn.cursor()
    sql = """
        SELECT id, name, email, password FROM users WHERE id = ?
    """
    c.execute(sql, (id,))
    return c.fetchone()

def user_login(conn, email, password):
    c = conn.cursor()
    sql = """
        SELECT id, name, password, email FROM users
        WHERE email = ? AND password = ?
    """
    c.execute(sql, (email, password))
    user = c.fetchone()
    return user

def remove_user(conn, id):
    c = conn.cursor()
    sql = """
        DELETE FROM users WHERE id = ?
    """
    c.execute(sql, (id,))
    conn.commit()

def update_user(conn, id, name, email, password):
    c = conn.cursor()
    sql = """
    UPDATE users
        SET name = ?,
            email = ?,
            password = ?
        WHERE id = ?
    """
    c.execute(sql, (name, email, password, id))
    conn.commit()
