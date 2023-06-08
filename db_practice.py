import os
import sqlite3

from typing import List, Set
from flask import Flask, request


def execute_query(query_sql: str) -> List:
    '''
    Функция для выполнения запроса
    :param query_sql: запрос
    :return: результат выполнения запроса
    '''
    db_pass = os.path.join(os.getcwd(), 'chinook.db')
    connection = sqlite3.connect(db_pass)
    cur = connection.cursor()
    result = cur.execute(query_sql).fetchall()
    connection.close()
    return result


def unwrapper(records: List) -> None:
    '''
    Функция для вывода результата выполнения запроса
    :param records: список ответа БД
    '''
    for record in records:
        print(*record)


def get_employees() -> None:
    '''
    Возвращает список
    '''
    query_sql = f'''
        SELECT *
          FROM employees;
    '''
    unwrapper(execute_query(query_sql))


#get_employees()

app = Flask('app')


@app.route('/customers', methods=['GET'])
def get_customers():
    city = request.args.get('city', default=None)
    state = request.args.get('state', default=None)

    query_sql = '''
        SELECT FirstName
              ,City 
              ,State
          FROM customers
        '''
    filter_query = ''
    if city and state:
        filter_query = f" WHERE City = '{city}' and State = '{state}'"
    if city and not state:
        filter_query = f" WHERE City = '{city}'"
    if state and not city:
        filter_query = f" WHERE State = '{state}'"

    query_sql += filter_query
    return execute_query(query_sql)


# get_customers()
# get_customers(city_name='Budapest')
# get_customers(state_name='RJ')
# get_customers(state_name='RJ', city_name='Rio de Janeiro')


def get_unique_customers_by_python():
    query_sql = f'''
        SELECT FirstName
          FROM customers
    '''
    records = execute_query(query_sql)
    result = set()
    for record in records:
        result.add(record[0])
    return len(result)


# print(get_unique_customers_by_python())


def get_unique_customers_by_sql():
    query_sql = f'''
            SELECT count(distinct FirstName) as first_names_qty
              FROM customers
    '''

    result = execute_query(query_sql)[0][0]
    return result

#print(get_unique_customers_by_sql())


def get_profit_by_sql() -> float:
    '''
    Функция для нахождения прибыли
    из таблицы invoice_items с помощью запроса sql
    '''
    query_sql = '''
            SELECT sum(UnitPrice * Quantity) AS profit
                FROM invoice_items;
        '''

    result = execute_query(query_sql)
    return result[0][0]


def get_recur_customers_by_sql() -> list:
    '''
    Функция для нахождения повторяющихся имён
    из таблицы customers с помощью запроса sql
    '''
    query_sql = '''
            SELECT FirstName, count(FirstName) AS count 
                FROM customers 
                GROUP BY FirstName
                HAVING count > 1;
        '''

    result = execute_query(query_sql)
    return result


# query_sql = '''
#       SELECT *
#         FROM customers
# '''

# result = execute_query(query_sql)

# print(result)

print('Profit:', get_profit_by_sql())
unwrapper(get_recur_customers_by_sql())

#http://127.0.0.1:5000/customers?city=Mountain View&state=CA
app.run()