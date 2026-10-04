import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

try:
    cur.execute("ALTER TABLE orders_orderitem ADD COLUMN variant_label varchar(100) NOT NULL DEFAULT ''")
    con.commit()
    print("variant_label column added successfully!")
except Exception as e:
    print("Notice:", e)

con.close()