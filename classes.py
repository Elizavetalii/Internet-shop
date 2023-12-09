from database import Database
from datetime import datetime

class Product(Database):
    def __init__(self):
        super().__init__('shop.db')

    def withdraval_of_all_goods(self):
        goods = self._cursor.execute('SELECT * FROM goods')
        for good in goods.fetchall():
            print(good)

    def add_goods_basket(self, good_id, basket, baskets):
        for i in basket:
            if i[0] not in baskets:
                self._cursor.execute("INSERT OR IGNORE INTO goods_basket (basket_id, good_id) VALUES (?, ?)", (i[0], good_id))
                self._connection.commit()
    
    def add_goods(self, good_name, quantity ,price, manufacturer):
        with self._connection:
            self._connection.execute("INSERT INTO goods (good_name, quantity ,price, manufacturer) VALUES (?, ?, ?, ?)",
                                    (good_name, quantity ,price, manufacturer))
        print("\nТовар был добавлен!")
        self._connection.commit()
    
    def delite_good(self, good_id):
        good = "DELETE FROM goods WHERE good_id = ?"
        self._cursor.execute(good, (good_id,))
        self._connection.commit()

    def new_goods_change(self):
        try:
            good_id = int(input("Введите номер товара, цену которого хотите изменить: "))
        except ValueError: print("Ошибка. Введите число.")
        try:
            new_price = int(input("Введите новую цену: "))
        except ValueError: print("Ошибка. Введите число.")
        update_query = "UPDATE goods SET price = ?  WHERE good_id = ? "
        self._cursor.execute(update_query,(new_price,good_id))
        self._connection.commit() 

class Basket(Database):
    def __init__(self):
        super().__init__('shop.db')
    
    def add_to_shopping_basket(self, user_id, good_id, quantity):
        data = self._cursor.execute("SELECT quantity FROM goods WHERE good_id = ?", (good_id,))
        good_data = data.fetchone()

        if good_data is None:
            print("Ошибка: неверно введен номер товара.")
            return
        if good_data[0] >= quantity:
            new_quantity = good_data[0] - quantity
            self._cursor.execute("UPDATE goods SET quantity = ? WHERE good_id = ?", (new_quantity, good_id))

            self._cursor.execute("INSERT INTO basket (in_order, user_id, quantity) VALUES (?, ?, ?)",
                    (False, user_id, quantity))
            print("\nТовар добавлен в корзину!")
            self._connection.commit()
        else:
            print("Приносим свои извенения, на складе нет такого количества товара.")
    
    def get_basket(self, user_id):
        query = 'SELECT basket_id FROM basket WHERE user_id = ?'
        request = self._connection.execute(query, (user_id,))
        basket = request.fetchall()
        return basket

    def get_all_basket(self, user_id):
        data = self._cursor.execute('SELECT * FROM basket WHERE user_id = ?', [user_id]).fetchall()
        return data

class Orders(Database):
    def __init__(self):
        super().__init__('shop.db')
    
    def get_orders(self, user_id):
        data = self._cursor.execute('SELECT * FROM orders WHERE user_id = ?', (user_id,)).fetchall()
        return data
    
    def add_order(self, basket_id, user_id, addres):
        t = datetime.now()
        self._cursor.execute("INSERT INTO orders (user_id, basket_id, address, order_time) VALUES (?, ?, ?, ?)",
                             (user_id, basket_id, addres, t.strftime("%d/%m/%Y, %H:%M")))
        self._connection.commit()
        print('Заказ добавлен')

class User(Database):
    def __init__(self):
        super().__init__('shop.db')

    def add_user(self, login, password):
        with self._connection :
            self._connection.execute("INSERT INTO users (Login, Password) VALUES (?,?)", [login, password])
            print("Вы успешно зарегестрированы!")
            
    def login_to_account(self, login, password):
        with self._connection:
            user_data = self._connection.execute("SELECT * FROM users WHERE Login = ? AND Password = ?", (login, password)).fetchone()
        if user_data:
            print("\nВы успешно вошли в аккаунт!")
            return True
        else:
            print("\nНеверно введен логин или пароль!")
            return False
            
    def get_user(self, login):
        query = 'SELECT * FROM users WHERE login = ?'
        request = self._connection.execute(query, (login,))
        user = request.fetchone()
        return user[0]


class Employee(Database):
    def __init__(self):
        super().__init__('shop.db')

    def add_employee(self, login, password, age, name, salary):
        with self._connection :
            self._connection.execute("INSERT INTO employees (login, password, age, name, salary) VALUES (?,?, ?, ?, ?)", 
                                     [login, password, age, name, salary])
            print("Сотрудник успешно добавлен!")
    
    def get_all_employees(self):
        goods = self._cursor.execute('SELECT * FROM employees')
        return goods.fetchall()
    
    def new_employee_change(self):
        try:
            employee_id = int(input("Введите номер сотрудника, данные которого хотите изменить: "))
        except ValueError: print("Ошибка. Введите число.")
        
        new_name = input("Введите новое имя: ")
        new_age = int(input('Введите новый возраст: '))
        new_salary = int(input('Введите новую зарплату: '))
        update_query = "UPDATE employees SET age = ?, name = ?, salary = ?  WHERE id = ? "
        self._cursor.execute(update_query,(new_age, new_name, new_salary, employee_id))
        self._connection.commit()
        print('Данные изменены')
        
    def delete_employee(self, id):
        data = self._cursor.execute("SELECT * FROM employees WHERE id = ?", (id,))
        employee_data = data.fetchone()

        if employee_data is None:
            print("Ошибка: неверный номер сотрудника.")
            return

        empl = "DELETE FROM employees WHERE id = ?"
        self._cursor.execute(empl, (id,))
        self._connection.commit()
        
        print("Сотрудник успешно удален.")

    def login_to_employees(self, login, password):
        with self._connection:
            employees_data = self._connection.execute("SELECT * FROM employees WHERE Login = ? AND Password = ?", (login, password)).fetchone()
        if employees_data:
            print("\nВы успешно вошли в аккаунт!")
            return True
        else:
            print("\nНеверно введен логин или пароль!")
            return False 