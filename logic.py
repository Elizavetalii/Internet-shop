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
    text="""Добро пожаловать в интернет - магазин профессиональной косметики - 'TITMOUSE'\n
    Выберите, пожалуйста что вам требуется\n"""
    type(text)
    while True:    
        print("1. Регистрация")
        print("2. Авторизация")
        choice = input("Введите ваш выбор: ")
        
        if choice == "1":
            login = input('Введите логин: ')
            password = input('Введите пароль: ') 
            db_user.add_user(login, password)
        elif choice == "2":
            print("Выберите свою роль:")
            print("1. Клиент")
            print("2. Сотрудник")
            print("3. Администратор")
            choice_2 = input("Введите ваш выбор: ")
            if choice_2 == "1":

                user_login = input("\nВведите логин: ")
                user_password = input("\nВведите пароль: ")     

                if db_user.login_to_account(user_login,user_password):
                    while True:
                        text2="""Выберите действие:\n
                        1.Открыть список товаров\n
                        2.Открыть свой список заказов\n
                        3.Сделать заказ\n
                        4.Выйти\n
                        """
                        type(text2)
                        user_choice = input("\n Введите выбраное действие: ")

                        if user_choice =="1":
                            print("Список товаров:\n")
                            db_product.withdraval_of_all_goods()
                            good_id = int(input("Введите номер товара для добавления в корзину: "))
                            quantity = int(input("Введите кол-во товара: "))
                            user = db_user.get_user(user_login)
                            db_basket.add_to_shopping_basket(user, good_id, quantity)
                            basket = db_basket.get_basket(user)
                            baskets = db_basket.get_all_basket(user)
                            db_product.add_goods_basket(good_id, basket, baskets)                            
                        
                        elif user_choice =="2":
                            user = db_user.get_user(user_login)
                            data = db_orders.get_orders(user)

                            if len(data) > 0:
                                for i in data:
                                    print(i)
                            else:
                                print("У вас ещё нет заказов!")                                                
                        
                        elif user_choice =="3":
                            user = db_user.get_user(user_login)
                            data = db_basket.get_all_basket(user)
                            
                            for i in data:
                                print("Номер корзины, прошлые заказы, номер пользователя, количество товара.")
                                print(i)
                            basket_id = int(input('Введети номер товара который хотите заказать: ')) 
                            adress = input("Введите адрес по которому нужно доставить заказ: ")
                            db_orders.add_order(basket_id, user, adress)
                            today = datetime.now().date()
                            tomorrow = today + timedelta(days=1)
                            tomorrows = today + timedelta(days=2)
                            tomorrowss = today + timedelta(days=3)
                            print("Выберите дату и время из 3 предложенных, когда вам будет удобно принять доставку.")
                            print ("1. Время 8:00 - 10:00. Дата ",tomorrow)
                            print ("2. Время 17:00 - 19:00. Дата ",tomorrows)
                            print ("3. Время 19:00 - 21:00. Дата ",tomorrowss)
                            datatime = input("Введите ваш выбор: ")
                            if datatime == "1":
                                print("Спасибо, что выбрали нас! Ваш заказ приедет с 8:00 до 10:00. Дата ",tomorrow)
                                print("По адресу", adress )
                                print("(Если вы выбрали неверную дату, время или адресс. То ваш заказ автоматически отменится по истечению времени доставки.)")
                                payment = """Оплату заказа вы можете осуществить только после получения заказа."""
                                print(payment)
                                return
                            if datatime == "2":
                                print("Спасибо, что выбрали нас! Ваш заказ приедет с 17:00 до 19:00. Дата ",tomorrows)
                                print("По адресу", adress )
                                print("(Если вы выбрали неверную дату, время или адресс. То ваш заказ автоматически отменится по истечению времени доставки.)")
                                print(payment)
                                return
                            if datatime == "3":
                                print("Спасибо, что выбрали нас! Ваш заказ приедет с 19:00 до 21:00. Дата ",tomorrowss)
                                print("По адресу", adress )
                                print("(Если вы выбрали неверную дату, время или адресс. То ваш заказ автоматически отменится по истечению времени доставки.)")
                                print(payment)
                                return
                            else:
                                print("Ошибка.")
                                
                        elif user_choice =="4":
                            print("Досвидания. Будем рады видеть вас снова!")
                            exit()

                        else:

                            print("Некорректный ввод, попробуйте снова.")  
                else:

                    print("Некорректный ввод, попробуйте снова.")  
            
            elif choice_2 == "2":
                Employee_login = input("\nВведите логин: ")
                Employee_password = input("\nВведите пароль:")                 

                if db_employee.login_to_employees(Employee_login,Employee_password):
                    while True:
                        print("Вы успешно авторизовались!\n")
                        text3="""Выберите действие:\n
                        1.Добавление товара на склад\n
                        2.Удаление товара со склада\n
                        3.Изменение цены товара\n
                        4.Просмотр всех товаров\n
                        5.Выход\n
                        """
                        type(text3)
                        Employee_choice = input("\n Введите выбраное действие:")

                        if Employee_choice =="1":
                            good_name = input('Введите название объявления: ')
                            quantity = int(input('Введите количество: '))
                            price = int(input('Введите цену: '))
                            manufacture = input('Страна производитель: ')
                            db_product.add_goods(good_name, quantity, price, manufacture)

                        elif Employee_choice =="2":
                            print("Список товаров:\n")
                            db_product.withdraval_of_all_goods()
                            id = int(input('Введите номер товара который хотите удалить: '))
                            db_product.delite_good(id)
                            print("Товар успешно удален!")
                        
                        elif Employee_choice =="3":
                            db_product.withdraval_of_all_goods()
                            db_product.new_goods_change()
                            print("Товар успешно изменен!")

                        elif Employee_choice =="4":
                            print("Список товаров:\n")
                            db_product.withdraval_of_all_goods()
                            
                        elif Employee_choice =="5":
                            print("Вы вышли из системы.")
                            exit()

                        else:

                            print("Некорректный ввод, попробуйте снова.")  
                else:
                    print("Неверный логин или пароль")
                    
            if choice_2 == "3":
                admin_login = input("\nВведите логин: ")
                admin_password = input("\nВведите пароль: ")  

                if admin_login == "Admin" and admin_password == "12345":
                    print("Вы успешно авторизовались!\n")
                    while True:
                        text3="""Выберите действие:\n
                        1.Добавление сотрудника\n
                        2.Удаление сотрудника\n
                        3.Изменение данных сотрудника\n
                        4.Просмотр всех сотрудников\n
                        5.Выход\n"""
                        type(text3)
                        Employee_choice = input("\n Введите выбраное действие: ")

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
                            print("Вы вышли из системы.")
                            exit()
                        
                        else:

                            print("Некорректный ввод, попробуйте снова.")                  
                else:
                    print("Неверный логин или пароль")
        else:

            print("Некорректный ввод, попробуйте снова.")            
Main()