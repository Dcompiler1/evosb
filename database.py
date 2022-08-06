import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('db.db',check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS "catalog_category"(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES catalog_category(id)
        ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS "catalog_types"(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
        )
        """)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS "catalog_product"(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        description TEXT NOT NULL,
        photo TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        type_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES catalog_category(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (type_id) REFERENCES catalog_types(id)
        ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
        self.conn.commit()
    def add(self):
        categories = [
            (1,'Lavash',None),
            (2,'Shaurma',None),
            (3,'Donar',None),
            (4,'Burger',None),
            (5,'Xot-dog',None),
            (6,'Desertlar',None),
            (7,'Ichimliklar',None),
            (8,'Gazaklar',None)
        ]
        types = [
            (1,'Mini'),
            (2,'Klassik')
        ]
        self.conn.executemany("""
        INSERT INTO "catalog_category"
        VALUES (?,?,?)
        """,categories)
        self.conn.executemany("""
        INSERT INTO "catalog_types"
        VALUES (?,?)
        """,types)
        self.conn.commit()
    def get_menu(self):
        data = self.conn.execute("""
        SELECT id,name FROM catalog_category WHERE parent_id IS NULL
        """).fetchall()
        return data
    def get_menu_child(self,data):
        product = self.conn.execute(f"""
        SELECT id,name FROM catalog_category
        WHERE parent_id = "{data}"
        """).fetchall()
        return product
    def get_type(self,ctg_id):
        types = self.conn.execute("""
        SELECT catalog_types.name,catalog_types.id FROM catalog_types
        INNER JOIN catalog_product
        ON catalog_types.id = catalog_product.type_id
        WHERE catalog_product.category_id = ?
        """,[ctg_id]).fetchall()
        return types
    def get_product(self,category_id,type_id):
        product = self.conn.execute("""
        SELECT * FROM catalog_product
        WHERE category_id = ? and type_id = ?
        """,[category_id,type_id]).fetchone()
        return product
    def get_product_by_id(self,product_id):
        product = self.conn.execute("""
        SELECT * FROM catalog_product 
        WHERE id = ?
        """,product_id).fetchone()
        return product

