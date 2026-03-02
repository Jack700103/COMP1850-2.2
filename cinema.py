import sqlite3

def customer_tickets(conn, customer_id):
    """
    Return a list of tuples: (film_title, screen, price)
    Include only tickets purchased by the given customer_id.
    Order results by film title alphabetically.
    """
    query = """
        SELECT 
            f.title AS film_title,
            s.screen,
            t.price
        FROM tickets t
        JOIN screenings s ON t.screening_id = s.screening_id
        JOIN films f ON s.film_id = f.film_id
        JOIN customers c ON t.customer_id = c.customer_id
        WHERE c.customer_id = ?
        ORDER BY film_title ASC;
    """
    cursor = conn.cursor()
    cursor.execute(query, (customer_id,))
    return cursor.fetchall()

def screening_sales(conn):
    """
    Return a list of tuples: (screening_id, film_title, tickets_sold)
    Include all screenings, even if tickets_sold is 0.
    Order results by tickets_sold descending.
    """
    query = """
        SELECT 
            s.screening_id,
            f.title AS film_title,
            COUNT(t.ticket_id) AS tickets_sold
        FROM screenings s
        JOIN films f ON s.film_id = f.film_id
        LEFT JOIN tickets t ON s.screening_id = t.screening_id
        GROUP BY s.screening_id
        ORDER BY tickets_sold DESC;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def top_customers_by_spend(conn, limit):
    """
    Return a list of tuples: (customer_name, total_spent)
    total_spent is the sum of ticket prices per customer.
    Only include customers who have bought at least one ticket.
    Order by total_spent descending.
    Limit the number of rows returned to `limit`.
    """
    query = """
        SELECT 
            c.customer_name,
            COALESCE(SUM(t.price), 0) AS total_spent
        FROM customers c
        LEFT JOIN tickets t ON c.customer_id = t.customer_id
        GROUP BY c.customer_id
        HAVING COUNT(t.ticket_id) > 0
        ORDER BY total_spent DESC
        LIMIT ?;
    """
    cursor = conn.cursor()
    cursor.execute(query, (limit,))
    return cursor.fetchall()
