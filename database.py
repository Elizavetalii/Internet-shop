import sqlite3

class Database:
    def __init__(self, db_name):
        self._connection = sqlite3.connect(db_name)
        self._cursor = self._connection.cursor()
        self._create_tables()
        self._filling_with_goods()

    def close(self):
        self._connection.close()

    def _execute(self, query, params = None, commit=False):
        query_result = self._cursor.execute(query, params or [])
        if commit:
            self._connection.commit()
        return self._cursor if not commit else query_result

    def _create_tables(self):
        with self._connection:

            self._connection.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,                    
                login TEXT NOT NULL,
                password TEXT NOT NULL
                                     )""")
            
            self._connection.execute("""
            CREATE TABLE IF NOT EXISTS goods(
                good_id INTEGER PRIMARY KEY AUTOINCREMENT,
                good_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL, 
                manufacturer TEXT NOT NULL             
                                     )""")
            
            self._connection.execute("""
            CREATE TABLE IF NOT EXISTS basket(
                basket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                in_order BOOL NOT NULL,
                user_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)                                 
                                     )""")
            
            self._connection.execute("""
            CREATE TABLE IF NOT EXISTS goods_basket(
                basket_id INTEGER NOT NULL,
                good_id INTEGER NOT NULL,
                UNIQUE(basket_id, good_id),
                FOREIGN KEY (basket_id) REFERENCES basket_id (basket_id),
                FOREIGN KEY (good_id) REFERENCES goods (good_id)                     
                                     )""")       
            
        with self._connection:
            self._connection.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                basket_id INTEGER NOT NULL,
                address TEXT NOT NULL,
                order_time TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (basket_id) REFERENCES users (basket_id)                                       
                                     )""")
            
            self._connection.execute("""
            CREATE TABLE IF NOT EXISTS employees(
                id INTEGER PRIMARY KEY AUTOINCREMENT,                    
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                age INT NOT NULL,
                name TEXT NOT NULL,
                salary INT NOT NULL
                                     )""")
                  
    def _filling_with_goods(self):
        goods = [
            ('Карандаш для губ GOAR', 100 , 1148 , 'Россия'),
            ('Палетка теней REVOLUTION PRO ', 150 , 1825, 'Великобритания'),
            ('Маска для волос ARAVIA', 70 , 679, 'Россия'),
            ('Сыворотка для лица RAD', 55 , 799, 'Нидерланды'),
            ('Гель для бровей ART-VASAGE', 85 , 355, 'Россия'),
            ('Духи ZIELINSKI & ROZEN', 40 , 2250, 'Израиль'),
            ('Тканевая маска для лица ABIB', 150 , 299, 'Республика Корея'),
            ('Губная помада FUNKY MONKEY', 90 , 1645, 'Россия'),
            ('Гель для душа MOSCHINO', 50 , 4060, 'Италия'),
            ('Адвент-календарь ERBORIAN 10 days', 140 , 7500, 'Республика Корея')
        ]
             
        self._cursor.execute("SELECT COUNT(*) FROM goods")
        if self._cursor.fetchone()[0] == 0:
            self._cursor.executemany("INSERT INTO goods (good_name, quantity ,price, manufacturer) VALUES (?, ?, ?, ?)",
                                goods)
            self._connection.commit()
            print("На складе сейчас 10 видов товаров!")