import sqlite3


class Database:
    def __init__(self, path_to_database):
        self.connection = sqlite3.connect(path_to_database)
        self.cursor = self.connection.cursor()

    async def add_admin(self, tg_id, secret_key, state):
        self.cursor.execute(
            "INSERT INTO admins (tg_id, secret_key, state) VALUES (?, ?, ?)",
            (tg_id, secret_key, state)
        )
        self.connection.commit()
        return True

    async def get_admin(self, tg_id):
        self.cursor.execute(
            "SELECT * FROM admins WHERE tg_id = ?", (tg_id,)
        )
        return self.cursor.fetchone()

    async def get_admins(self):
        self.cursor.execute(
            "SELECT * FROM admins"
        )
        return self.cursor.fetchall()

    async def update_admin(self, tg_id, phone_number, state):
        self.cursor.execute(
            'UPDATE admins SET phone_number = ?, state = ? WHERE tg_id = ?',
            (phone_number, state, tg_id)
        )
        self.connection.commit()
        return True

    async def delete_admin(self, tg_id):
        self.cursor.execute(
            "DELETE FROM admins WHERE tg_id = ?", (tg_id,)
        )
        self.connection.commit()
        return True

    async def update_secret_key(self, secret_key):
        self.cursor.execute(
            "UPDATE admins SET secret_key = ? WHERE state='phone_number'",
            (secret_key,)
        )
        self.connection.commit()
        return True

    async def add_catalog(self, state):
        async with state.proxy() as data:
            self.cursor.execute(
                "INSERT INTO catalogs (name) VALUES (?)", (data['name'],)
            )
            self.connection.commit()

    async def get_catalogs(self):
        self.cursor.execute(
            "SELECT * FROM catalogs"
        )
        return self.cursor.fetchall()

    async def delete_catalog(self, id_catalog):
        self.cursor.execute(
            "DELETE FROM catalogs WHERE id = ?", (id_catalog,)
        )
        self.connection.commit()
        return True

    async def update_catalog(self, state):
        async with state.proxy() as data:
            self.cursor.execute(
                "UPDATE catalogs SET name = ? WHERE id = ?", (data['name'],  data['id_'],)
            )
            self.connection.commit()
        return True

    async def get_catalog(self, id_catalog):
        self.cursor.execute(
            "SELECT * FROM catalogs WHERE id = ?", (id_catalog,)
        )
        return self.cursor.fetchone()[0]

    async def add_product(self, state):
        async with state.proxy() as data:
            self.cursor.execute(
                "INSERT INTO products (name, about, price, img, count) VALUES (?, ?, ?, ?, ?)",
                (data['name'], data['about'], data['price'], data['image'], data['count'],)
            )
        id_product = self.cursor.lastrowid
        self.connection.commit()
        return id_product

    async def update_product(self, state):
        async with state.proxy() as data:
            self.cursor.execute(
                "UPDATE products SET name = ?, about = ?, price = ?, img = ?, count = ? WHERE id = ?",
                (data['name'], data['about'], data['price'], data['image'], data['count'], data['id_'])
            )
        self.connection.commit()
        return True

    async def update_count_product(self, id_product, count):
        self.cursor.execute(
            "UPDATE products SET count = ? WHERE id = ?", (count, id_product,)
        )
        self.connection.commit()
        return True

    async def get_products(self):
        self.cursor.execute(
            "SELECT * FROM products"
        )
        return self.cursor.fetchall()

    async def get_products_available(self):
        self.cursor.execute(
            "SELECT * FROM products WHERE count > 0"
        )
        return self.cursor.fetchall()

    async def get_product(self, id_product):
        self.cursor.execute(
            "SELECT * FROM products WHERE id = ?", (id_product,)
        )
        self.connection.commit()
        return self.cursor.fetchone()

    async def delete_product(self, id_product):
        self.cursor.execute(
            "DELETE FROM products WHERE id = ?", (id_product,)
        )
        self.connection.commit()
        self.cursor.execute(
            "DELETE FROM catalogs_products WHERE product = ?", (id_product,)
        )
        self.connection.commit()
        return True

    async def add_product_into_catalog(self, id_catalog, id_product):
        self.cursor.execute(
            "INSERT INTO catalogs_products (catalog, product) VALUES (?, ?)",
            (id_catalog, id_product)
        )
        self.connection.commit()
        return True

    async def add_orders(self, state):
        async with state.proxy() as data:
            self.cursor.execute(
                "INSERT INTO orders (id_product, tg_id, phone_number, address, count_product) "
                "VALUES (?, ?, ?, ?, ?)",
                (data['id_product'], data['tg_id'],
                 data['phone_number'], data['address'], data['count_product'])
            )
        id_order = self.cursor.lastrowid
        self.connection.commit()
        return id_order

    async def get_orders(self):
        self.cursor.execute(
            "SELECT * FROM orders"
        )
        return self.cursor.fetchall()

    async def get_id_products_from_catalog(self, id_catalog):
        self.cursor.execute(
            'select catalogs_products.catalog, '
            'products.id, '
            'products.name, '
            'products.about, '
            'products.price, '
            'products.count '
            'from catalogs_products join products on catalogs_products.product = products.id '
            'where catalogs_products.catalog = ? and products.count > 0', (id_catalog,)
        )
        return self.cursor.fetchall()

    async def get_orders_user(self, id_user):
        self.cursor.execute(
            "SELECT * FROM orders where tg_id = ?", (id_user,)
        )
        return self.cursor.fetchall()

    async def get_orders_finish(self):
        self.cursor.execute(
            "SELECT * FROM orders where state = 'finish'"
        )
        return self.cursor.fetchall()

    async def get_orders_user_finish(self, id_user):
        self.cursor.execute(
            "SELECT * FROM orders where tg_id = ? and state = 'finish'", (id_user,)
        )
        return self.cursor.fetchall()

    async def get_orders_waiting(self):
        self.cursor.execute(
            "SELECT * FROM orders where state = 'waiting'"
        )
        return self.cursor.fetchall()

    async def get_orders_user_waiting(self, id_user):
        self.cursor.execute(
            "SELECT * FROM orders where tg_id = ? and state = 'waiting'", (id_user,)
        )
        return self.cursor.fetchall()

    async def delete_order(self, id_order):
        self.cursor.execute(
            "DELETE FROM orders WHERE id = ?", (id_order,)
        )
        self.connection.commit()
        return True

    async def get_order(self, id_order):
        self.cursor.execute(
            'SELECT * '
            'from orders join products on orders.id_product = products.id '
            'where orders.id = ?', (id_order,)
        )
        return self.cursor.fetchone()

    async def update_state_order(self, id_order):
        self.cursor.execute(
            "UPDATE orders SET state = 'finish' WHERE id = ?", (id_order,)
        )
        self.connection.commit()
        return True
