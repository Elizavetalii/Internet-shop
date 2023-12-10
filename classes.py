from database import Database
from datetime import datetime

class Product(Database):
    def __init__(self):
        super().__init__('shop.db')

    def get_all_goods(self):
        goods = self._cursor.execute('SELECT * FROM goods')
        for good in goods.fetchall():
            print(f'{good[0]}. {good[1]} / {good[2]} шт. / {good[3]} руб. / {good[4]}')

    def good_is_enough(self, good_id, quantity):
        good_data = self._cursor.execute('SELECT quantity FROM goods WHERE good_id = ?',
                                        (good_id,)).fetchone()
        if good_data:
            good_quantity = good_data[0]
            if good_quantity >= quantity:
                return True
            else:
                print(f'Приносим свои извинения, доступно {good_quantity} товаров.')
                return False
        else:
            print('Ошибка: неверно введен номер товара.')
            return False
    
    def add_goods(self, name, quantity ,price, manufacturer):
        self._connection.execute('INSERT INTO goods (name, quantity ,price, manufacturer) VALUES (?, ?, ?, ?)',
                                    (name, quantity ,price, manufacturer))
        print('\nТовар был добавлен!')
        self._connection.commit()
    
    def delite_good(self, good_id):
        self._cursor.execute('DELETE FROM goods WHERE good_id = ?', (good_id,))
        self._connection.commit()

    def new_goods_change(self):
        try:
            good_id = int(input('Введите номер товара, цену которого хотите изменить: '))
        except ValueError: print('Ошибка. Введите число.')
        try:
            new_price = int(input('Введите новую цену: '))
        except ValueError: print('Ошибка. Введите число.')
        self._cursor.execute('UPDATE goods SET price = ?  WHERE good_id = ?'
                             ,(new_price,good_id))
        self._connection.commit() 

class Basket(Database):
    def __init__(self):
        super().__init__('shop.db')
    
    def get_basket(self, user_id):
        basket = self._connection.execute('SELECT basket_id FROM basket WHERE in_order = 0 and user_id = ?',
                                        (user_id,)).fetchone()
        if basket:
            return basket[0]
        else:
            self._connection.execute('INSERT INTO basket (user_id) VALUES (?)', [user_id])
            basket = self._connection.execute('SELECT basket_id FROM basket WHERE in_order = 0 and user_id = ?',
                                        (user_id,)).fetchone()
            return basket[0]

    def add_goods_basket(self, basket_id, good_id, quantity):
        good_data = self._cursor.execute('SELECT quantity FROM goods WHERE good_id = ?', (good_id,)).fetchone()
        new_quantity = good_data[0] - quantity

        if new_quantity < 0:
            print('\nНа складе недостаточно товара, обновите свой список товаров, чтобы получить свежие данные')
            return

        self._cursor.execute('UPDATE goods SET quantity = ? WHERE good_id = ?', (new_quantity, good_id))
        good_in_basket = self._cursor.execute('SELECT quantity FROM goods_basket WHERE basket_id = ? and good_id = ?',
                                              (basket_id, good_id)).fetchone()
        if good_in_basket:
            quantity += good_in_basket[0]
            self._cursor.execute('UPDATE goods_basket SET quantity = ? WHERE basket_id = ? and good_id = ?', 
                                 (quantity, basket_id, good_id))
        else:
            self._cursor.execute('INSERT OR IGNORE INTO goods_basket (basket_id, good_id, quantity) VALUES (?, ?, ?)',
                             (basket_id, good_id, quantity))
        print('\nТовар добавлен в корзину!')
        self._connection.commit()
 
    def get_goods_of_basket(self, basket_id):
        goods = self._cursor.execute('''
            SELECT
                goods.name, goods_basket.quantity, goods.price
            FROM
                goods_basket
            LEFT JOIN goods ON goods_basket.good_id = goods.good_id
        WHERE basket_id = ?''', (basket_id,)).fetchall()
        return goods

    def clear_basket(self, basket_id):
        goods_in_basket = self._cursor.execute('SELECT good_id, quantity FROM goods_basket WHERE basket_id = ?', (basket_id,)).fetchall()
        for good_in_basket in goods_in_basket:
            good_id = good_in_basket[0]
            good_data = self._cursor.execute('SELECT quantity FROM goods WHERE good_id = ?', (good_id,)).fetchone()
            new_quantity = good_data[0] + good_in_basket[1]
            self._cursor.execute('UPDATE goods SET quantity = ? WHERE good_id = ?', (new_quantity, good_id))

        self._cursor.execute('DELETE FROM goods_basket WHERE basket_id = ?', (basket_id,))
        self._connection.commit()

    def close_basket_to_order(self, user_id, basket_id):
        self._cursor.execute('UPDATE basket SET in_order = 1 WHERE user_id = ? and basket_id = ?',
                             (user_id, basket_id))

class Orders(Database):
    def __init__(self):
        super().__init__('shop.db')
    
    def get_orders(self, user_id):
        data = self._cursor.execute('SELECT order_id, order_time, total, address FROM orders WHERE user_id = ?', (user_id,)).fetchall()
        return data
    
    def add_order(self, user_id, basket_id, address, total):
        t = datetime.now()
        self._cursor.execute('INSERT INTO orders (user_id, basket_id, address, order_time, total) VALUES (?, ?, ?, ?, ?)',
                             (user_id, basket_id, address, t.strftime('%d/%m/%Y, %H:%M'), total))
        print('\nЗаказ добавлен')
        self._connection.commit()
        

class User(Database):
    def __init__(self):
        super().__init__('shop.db')

    def add_user(self, login, password):
        with self._connection :
            user_data = self._connection.execute('SELECT * FROM users WHERE Login = ?', (login, )).fetchone()
            if user_data:
                print('\nПользователь с таким логином уже существует.')
            else:
                self._connection.execute('INSERT INTO users (Login, Password) VALUES (?,?)', [login, password])
                print('\nВы успешно зарегестрированы!')
            
    def login_to_account(self, login, password):
        with self._connection:
            user_data = self._connection.execute('SELECT user_id FROM users WHERE Login = ? AND Password = ?',
                                                 (login, password)).fetchone()
        if user_data:
            print('\nВы успешно вошли в аккаунт!')
            return user_data[0]
        else:
            print('\nНеверно введен логин или пароль!')
            return 0
 
class Employee(Database):
    def __init__(self):
        super().__init__('shop.db')

    def add_employee(self, login, password, age, name, salary):
        with self._connection :
            self._connection.execute('INSERT INTO employees (login, password, age, name, salary) VALUES (?,?, ?, ?, ?)', 
                                     (login, password, age, name, salary))
            print('Сотрудник успешно добавлен!')
    
    def get_all_employees(self):
        goods = self._cursor.execute('SELECT * FROM employees')
        return goods.fetchall()
    
    def new_employee_change(self):
        try:
            employee_id = int(input('Введите номер сотрудника, данные которого хотите изменить: '))
        except ValueError: print('Ошибка. Введите число.')
        employee = self._connection.execute('SELECT login FROM employees WHERE id = ? ',
                                            (employee_id,)).fetchone()
        
        if employee is None:      
            print('Сотрудника с таким номером не существует.')
            return
        
        print(f'Меняете сотрудника с логином {employee[0]}')
        
        new_name = input('Введите новое имя: ')
        new_age = int(input('Введите новый возраст: '))
        new_salary = int(input('Введите новую зарплату: '))
        self._cursor.execute('UPDATE employees SET age = ?, name = ?, salary = ?  WHERE id = ?',
                             (new_age, new_name, new_salary, employee_id))
        self._connection.commit()
        print('Данные изменены')
        
    def delete_employee(self, id):
        data = self._cursor.execute('SELECT * FROM employees WHERE id = ?', (id,))
        employee_data = data.fetchone()

        if employee_data is None:
            print('Ошибка: неверный номер сотрудника.')
            return

        empl = 'DELETE FROM employees WHERE id = ?'
        self._cursor.execute(empl, (id,))
        self._connection.commit()
        
        print('Сотрудник успешно удален.')

    def login_to_employees(self, login, password):
        with self._connection:
            employees_data = self._connection.execute('SELECT * FROM employees WHERE Login = ? AND Password = ?', (login, password)).fetchone()
        if employees_data:
            print('\nВы успешно вошли в аккаунт!')
            return True
        else:
            print('\nНеверно введен логин или пароль!')
            return False 