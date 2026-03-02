import sqlite3

def customer_tickets(conn, customer_id):
    """Return film_title, screen, price for specific customer ordered by film title"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            f.title AS film_title,
            s.screen,
            t.price
        FROM tickets t
        JOIN customers c ON t.customer_id = c.customer_id
        JOIN screenings s ON t.screening_id = s.screening_id
        JOIN films f ON s.film_id = f.film_id
        WHERE c.customer_id = ?
        ORDER BY film_title ASC
    ''', (customer_id,))
    return cursor.fetchall()

def screening_sales(conn):
    """Return screening_id, film_title, tickets_sold ordered by tickets_sold DESC"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            s.screening_id,
            f.title AS film_title,
            COUNT(t.ticket_id) AS tickets_sold
        FROM screenings s
        JOIN films f ON s.film_id = f.film_id
        LEFT JOIN tickets t ON s.screening_id = t.screening_id
        GROUP BY s.screening_id
        ORDER BY tickets_sold DESC
    ''')
    return cursor.fetchall()

def top_customers_by_spend(conn, limit):
    """Return customer_name, total_spent for top spenders limited by specified number"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            c.customer_name,
            COALESCE(SUM(t.price), 0) AS total_spent
        FROM customers c
        LEFT JOIN tickets t ON c.customer_id = t.customer_id
        GROUP BY c.customer_id
        HAVING COUNT(t.ticket_id) > 0
        ORDER BY total_spent DESC
        LIMIT ?
    ''', (limit,))
    return cursor.fetchall()
