import sqlite3

def init_db():
    conn = sqlite3.connect("clean_impact.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cleanup(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            volunteers INTEGER,
            bags INTEGER,
            waste REAL
        )
    """)
    conn.commit()
    conn.close()

def save_cleanup(volunteers, bags, waste):
    conn = sqlite3.connect("clean_impact.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO cleanup(volunteers, bags, waste)
        VALUES(?,?,?)
    """, (volunteers, bags, waste))
    conn.commit()
    conn.close()

# New: Read all cleanups
def get_all_cleanups():
    conn = sqlite3.connect("clean_impact.db")
    c = conn.cursor()
    c.execute("SELECT id, volunteers, bags, waste FROM cleanup ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows  # Returns list of tuples: [(id, volunteers, bags, waste), ...]

# New: Update a cleanup by ID
def update_cleanup(cleanup_id, volunteers, bags, waste):
    conn = sqlite3.connect("clean_impact.db")
    c = conn.cursor()
    c.execute("""
        UPDATE cleanup
        SET volunteers = ?, bags = ?, waste = ?
        WHERE id = ?
    """, (volunteers, bags, waste, cleanup_id))
    conn.commit()
    conn.close()

# New: Delete a cleanup by ID
def delete_cleanup(cleanup_id):
    conn = sqlite3.connect("clean_impact.db")
    c = conn.cursor()
    c.execute("DELETE FROM cleanup WHERE id = ?", (cleanup_id,))
    conn.commit()
    conn.close()