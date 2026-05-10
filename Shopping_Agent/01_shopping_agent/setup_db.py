import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "store.db")


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            description TEXT,
            is_organic INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            rating REAL,
            reviewer_name TEXT,
            review_text TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    products = [
        (1, "Organic Raw Honey",       "honey", 14.99, "Pure organic raw honey, unfiltered and cold-pressed",       1),
        (2, "Wildflower Honey",        "honey", 12.99, "Natural wildflower honey from local beekeepers",            0),
        (3, "Organic Manuka Honey",    "honey", 29.99, "Premium organic Manuka honey from New Zealand",             1),
        (4, "Clover Honey",            "honey",  8.99, "Classic clover honey, smooth and sweet",                    0),
        (5, "Organic Buckwheat Honey", "honey", 18.99, "Dark and robust organic buckwheat honey, antioxidant-rich", 1),
        (6, "Orange Blossom Honey",    "honey", 15.99, "Light and floral orange blossom honey",                     0),
        (7, "Organic Acacia Honey",    "honey", 17.99, "Light and mild organic acacia honey, low glycemic index",   1),
        (8, "Creamed Honey",           "honey", 11.99, "Smooth creamed honey with spreadable texture",              0),
    ]
    cursor.executemany("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?, ?)", products)

    # Avg ratings per product after insert:
    # 1 -> (5+4+5+4.5) / 4 = 4.625   organic $14.99  ✓
    # 2 -> (4+3.5+4)   / 3 = 3.833   non-organic     ✗
    # 3 -> (5+4.5+5)   / 3 = 4.833   organic $29.99  (over budget)
    # 4 -> (3.5+3.5+3.5)/3 = 3.5     non-organic     ✗
    # 5 -> (5+4+5+4.5) / 4 = 4.625   organic $18.99  ✓
    # 6 -> (4+4.5+4)   / 3 = 4.167   non-organic     ✗
    # 7 -> (5+4.5+4.5+5)/4 = 4.75    organic $17.99  ✓
    # 8 -> (4+4+4)     / 3 = 4.0     non-organic     ✗
    reviews = [
        (1, 5.0, "Alice",  "Amazing honey! Best I've ever tried."),
        (1, 4.0, "Bob",    "Good quality, will buy again."),
        (1, 5.0, "Carol",  "Excellent raw flavor, very pure."),
        (1, 4.5, "Dave",   "Very good, love that it's unfiltered."),
        (2, 4.0, "Eve",    "Decent honey for the price."),
        (2, 3.5, "Frank",  "Average, nothing special."),
        (2, 4.0, "Grace",  "Good everyday honey."),
        (3, 5.0, "Henry",  "Worth every penny, incredible quality."),
        (3, 4.5, "Iris",   "Excellent antibacterial properties."),
        (3, 5.0, "Jack",   "Best honey I have ever tasted."),
        (4, 3.5, "Kate",   "Okay for cooking, nothing fancy."),
        (4, 3.5, "Leo",    "Nothing special, pretty generic."),
        (4, 3.5, "Mia",    "Average clover honey."),
        (5, 5.0, "Noah",   "Rich bold flavor, great in tea."),
        (5, 4.0, "Olivia", "Good strong honey, unique taste."),
        (5, 5.0, "Paul",   "Love the dark color and depth."),
        (5, 4.5, "Quinn",  "Great organic option at this price."),
        (6, 4.0, "Rachel", "Nice floral flavor."),
        (6, 4.5, "Sam",    "Lovely and delicate."),
        (6, 4.0, "Tina",   "Good for baking."),
        (7, 5.0, "Uma",    "Perfect mild flavor, love it!"),
        (7, 4.5, "Victor", "Excellent light honey."),
        (7, 4.5, "Wendy",  "Great product, very pure taste."),
        (7, 5.0, "Xavier", "Wonderful, highly recommend."),
        (8, 4.0, "Yvonne", "Nice spreadable texture."),
        (8, 4.0, "Zack",   "Good on toast."),
        (8, 4.0, "Amy",    "Decent creamed honey."),
    ]
    cursor.execute("DELETE FROM reviews")
    cursor.executemany(
        "INSERT INTO reviews (product_id, rating, reviewer_name, review_text) VALUES (?, ?, ?, ?)",
        reviews,
    )

    conn.commit()
    conn.close()
    print(f"Database created at: {DB_PATH}")


if __name__ == "__main__":
    create_database()
