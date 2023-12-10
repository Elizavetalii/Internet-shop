import os
from service import db_user, db_product, db_basket, db_orders, db_employee
from time import sleep
from classes import *
from msvcrt import kbhit, getch
from os import system as command
from datetime import datetime, timedelta

def clear_console():
    command= 'sls' if os.name =='nt' else 'clear'
    os.system(command)

def type(text: str, name: str = None) -> None:
    for letter in text:
        if kbhit():
            key = getch()
            
            if key == b'\r':
                command("cls")
                print(text)
            break

        print(letter, end="", flush=True)
        sleep(0.025)
        
def Main():
    
    type("Добро пожаловать в интернет - магазин профессиональной косметики - 'TITMOUSE'\n")
    
    while True:    
        print('\nВыберите, пожалуйста что вам требуется \n1. Регистрация \n2. Авторизация')
        login_choice = input('\nВведите ваш выбор: ')
        
        if login_choice == "1":
            login = input('Введите логин: ')
            password = input('Введите пароль: ') 
            db_user.add_user(login, password)

        elif login_choice == "2":
            print('\nВыберите свою роль: \n1. Клиент \n2. Сотрудник \n3. Администратор')
            role_choise = input("\nВведите ваш выбор: ")

            if role_choise == "1":
                user_login = input('\nВведите логин: ')
                user_password = input('Введите пароль: ')     
                user_id = db_user.login_to_account(user_login, user_password)
                basket_id = db_basket.get_basket(user_id)
               
                if user_id > 0:

                    while True:
                        type("""\nВыберите действие:\n
                        1. Открыть список товаров\n
                        2. Посмотреть корзину\n
                        3. Открыть свой список заказов\n
                        4. Выйти\n""")
                        user_choice = input('\nВведите выбраное действие: ')

                        if user_choice =="1":
                            print('Список товаров:\n')
                            db_product.get_all_goods()
                            good_id = int(input('\nВведите номер товара для добавления в корзину: '))
                            quantity = int(input('Введите кол-во товара: '))
                            if db_product.good_is_enough(good_id, quantity):
                                db_basket.add_goods_basket(basket_id, good_id, quantity) 
                        
                        elif user_choice =="2":
                            goods = db_basket.get_goods_of_basket(basket_id)
                            if len(goods) == 0:
                                print('Ваша корзина пуста, добавьте товары :)')
                                
                            else:
                                total = 0
                                print('Название товара / Штук / Итого за позицию, руб.')
                                for good in goods:
                                    cost = good[1] * good[2]
                                    total +=cost
                                    print(f'{good[0]} / {good[1]} / {cost}')

                                print(f'К оформлению: {total} руб.\n')
                                print('\nЧто хотите сделать с корзиной? \n 1. Сделать заказ \n 2. Очистить корзину')
                                
                                basket_choice = input("\nВведите выбраное действие: ")
                                
                                if basket_choice == "1":
                                    address = input('\nВведите адрес, по которому нужно доставить заказ: ')
                                    today = datetime.now().date()
                                    tomorrow = today + timedelta(days=1)
                                    tomorrows = today + timedelta(days=2)
                                    tomorrowss = today + timedelta(days=3)
                                    print('Выберите дату и время из 3 предложенных, когда вам будет удобно принять доставку.')
                                    print ('1. Время 8:00 - 10:00. Дата ',tomorrow)
                                    print ('2. Время 17:00 - 19:00. Дата ',tomorrows)
                                    print ('3. Время 19:00 - 21:00. Дата ',tomorrowss)
                                    datatime = input("\nВведите ваш выбор: ")

                                    if datatime == "1":
                                        print('Спасибо, что выбрали нас! Ваш заказ приедет с 8:00 до 10:00. Дата ',tomorrow)
                                    elif datatime == "2":
                                        print('Спасибо, что выбрали нас! Ваш заказ приедет с 17:00 до 19:00. Дата ',tomorrows)
                                    elif datatime == "3":
                                        print('Спасибо, что выбрали нас! Ваш заказ приедет с 19:00 до 21:00. Дата ',tomorrowss)
                                    else:
                                        print('Ошибка.')

                                    print('По адресу ', address)
                                    print('''(Если вы выбрали неверную дату, время или адрес. 
                                    То ваш заказ автоматически отменится по истечению времени доставки.)''')
                                    print('Оплату заказа вы можете осуществить только после получения заказа.')

                                    db_orders.add_order(user_id, basket_id, address, total)
                                    db_basket.close_basket_to_order(user_id, basket_id)
                                    basket_id = db_basket.get_basket(user_id)

                                elif basket_choice == "2":
                                    db_basket.clear_basket(basket_id)
                                    print('\nКорзина очищена')
                                else:
                                    print('Ошибка.')

                        elif user_choice =="3":
                            orders = db_orders.get_orders(user_id)
                            print('Номер заказа\t| Время заказа\t\t| Cумма заказа, руб.\t| Адрес заказа')

                            if len(orders) > 0:
                                for order in orders:
                                    print(f'{order[0]}\t\t| {order[1]}\t| {order[2]}\t\t| {order[3]}')
                            else:
                                print('\nУ вас ещё нет заказов!')                                                
                                
                        elif user_choice =="4":
                            print('\nДосвидания. Будем рады видеть вас снова!')
                            exit()

                        else:
                            print('Некорректный ввод, попробуйте снова.')  
                else:
                    print('Некорректный ввод, попробуйте снова.')  
            
            elif role_choise == "2":
                Employee_login = input('\nВведите логин: ')
                Employee_password = input('\nВведите пароль:')                 

                if db_employee.login_to_employees(Employee_login,Employee_password):
                    while True:
                        print("Вы успешно авторизовались!\n")
                        text3="""Выберите действие:\n
                        1. Добавление товара на склад\n
                        2. Удаление товара со склада\n
                        3. Изменение цены товара\n
                        4. Просмотр всех товаров\n
                        5. Выход\n
                        """
                        type(text3)
                        Employee_choice = input('\n Введите выбраное действие: ')

                        if Employee_choice =="1":
                            name = input('Введите название товара: ')
                            quantity = int(input('Введите количество: '))
                            price = int(input('Введите цену: '))
                            manufacture = input('Страна производитель: ')
                            db_product.add_goods(name, quantity, price, manufacture)

                        elif Employee_choice =="2":
                            print('Список товаров:\n')
                            db_product.get_all_goods()
                            id = int(input('Введите номер товара который хотите удалить: '))
                            db_product.delite_good(id)
                            print('Товар успешно удален!')
                        
                        elif Employee_choice =="3":
                            db_product.get_all_goods()
                            db_product.new_goods_change()
                            print('Товар успешно изменен!')

                        elif Employee_choice =="4":
                            print('Список товаров:\n')
                            db_product.get_all_goods()
                            
                        elif Employee_choice =="5":
                            print('Вы вышли из системы.')
                            exit()
                        else:
                            print('Некорректный ввод, попробуйте снова.')  
                else:
                    print('Неверный логин или пароль')
                    
            elif role_choise == "3":
                admin_login = input('\nВведите логин: ')
                admin_password = input('\nВведите пароль: ')  

                if admin_login == "Admin" and admin_password == "12345":
                    print('Вы успешно авторизовались!\n')
                    while True:
                        text3="""Выберите действие:\n
                        1. Добавление сотрудника\n
                        2. Удаление сотрудника\n
                        3. Изменение данных сотрудника\n
                        4. Просмотр всех сотрудников\n
                        5. Выход\n"""
                        type(text3)
                        Employee_choice = input('\n Введите выбраное действие: ')

                        if Employee_choice =="1":
                            login = input('Введите логин сотрудника: ')
                            password = int(input('Введите пароль сотрудника: '))
                            age = int(input('Введите возраст сотрудника: '))
                            name = input('Введите имя сотрудника: ')
                            salary = int(input('Введите зарплату сотрудника: '))
                            db_employee.add_employee(login, password, age, name, salary)

                        elif Employee_choice =="2":
                            for i in db_employee.get_all_employees():
                                print(i)
                            id = int(input('Введите номер сотрудника которого хотите удалить: '))
                            db_employee.delete_employee(id)
                        
                        elif Employee_choice =="3":
                            db_employee.new_employee_change()

                        elif Employee_choice =="4":
                            for i in db_employee.get_all_employees():
                                print(i)
                
                        elif Employee_choice =="5":
                            print('Вы вышли из системы.')
                            exit()
                        
                        else:
                            print('Некорректный ввод, попробуйте снова.')                  
                else:
                    print('Неверный логин или пароль')
        else:
            print('Некорректный ввод, попробуйте снова.')            
Main()