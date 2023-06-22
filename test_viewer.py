import requests
import pytest
from requests import Session
from bs4 import BeautifulSoup
import psycopg2
from config import host, user, pwd, db_name
import datetime


@pytest.fixture
def clear_table():
    con = psycopg2.connect(host=host, user=user, password=pwd, database=db_name)
    cur = con.cursor()

    cur.execute('DELETE FROM cards')
    con.commit()

    cur.close()
    con.close()


@pytest.fixture
def expect():
    con = psycopg2.connect(host=host, user=user, password=pwd, database=db_name)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS cards(
                                card_number BIGINT PRIMARY KEY NOT NULL,
                                card_expir_date DATE NOT NULL,
                                card_cvv INT NOT NULL,
                                card_date_of_issue DATE NOT NULL,
                                card_user_id UUID NOT NULL,
                                card_status VARCHAR(20));''')

    cur.execute('DELETE FROM cards')
    cur.execute('''INSERT INTO cards VALUES (1111222233334444, '2024-11-01', 123, 
                '2023-11-23', 'e162911d-bb32-46d2-80ba-840c0a1cb010', 'new');''')
    con.commit()

    cur.execute('''SELECT * FROM cards WHERE card_number = 1111222233334444''')

    expect = cur.fetchone()

    cur.close()
    con.close()

    return expect


@pytest.mark.parametrize(
    "number, expir_date, cvv, date_of_issue, user_id, expec_result",
    [
        (
            1111222233334444,
            "11/2024",
            123,
            "2023-11-23",
            "e162911d-bb32-46d2-80ba-840c0a1cb010",
            "Така картка вже є",
        ),
        (
            1111,
            "11/2024",
            123,
            "2023-11-23",
            "e162911d-bb32-46d2-80ba-840c0a1cb010",
            "Невірний номер",
        ),
        (
            1111222233334444,
            "11",
            123,
            "2023-11-23",
            "e162911d-bb32-46d2-80ba-840c0a1cb010",
            "Невірна дата закінчення",
        ),
        (
            1111222233334444,
            "11/2024",
            12,
            "2023-11-23",
            "e162911d-bb32-46d2-80ba-840c0a1cb010",
            "Невірний cvv",
        ),
        (
            1111222233334444,
            "11/2024",
            123,
            "23",
            "e162911d-bb32-46d2-80ba-840c0a1cb010",
            "Невірна дата створення",
        ),
    ],
)
def test_create_valid_card(number, expir_date, cvv, date_of_issue, user_id, expec_result, expect):
    url = r"http://127.0.0.1:5000/create"

    data = {'number': number,
            'expir_date': expir_date,
            'cvv': cvv,
            'date_of_issue': date_of_issue,
            'user_id': user_id}

    res = Session()

    temp = res.post(url, data=data)

    soup = BeautifulSoup(temp.text, 'lxml')

    result = soup.find('p', class_='error').text

    res.close()

    assert result == expec_result


def show_table():
    con = psycopg2.connect(host=host, user=user, password=pwd, database=db_name)
    cur = con.cursor()

    cur.execute('SELECT * FROM cards')
    result = cur.fetchone()

    cur.close()
    con.close()

    return result


@pytest.mark.parametrize(
    "number, expir_date, cvv, date_of_issue, user_id, expec_err",
    [
        (
            1111222233334444,
            "11/2024",
            123,
            "2023-11-23",
            "e162911d-bb32-46d2-80ba-840c0a1cb010",
            "Все добре",
        ),
    ],
)
def test_create_card(number, expir_date, cvv, date_of_issue, user_id, expec_err, clear_table):
    url = r"http://127.0.0.1:5000/create"

    data = {'number': number,
            'expir_date': expir_date,
            'cvv': cvv,
            'date_of_issue': date_of_issue,
            'user_id': user_id}

    res = Session()
    temp = res.post(url, data=data)

    soup = BeautifulSoup(temp.text, 'lxml')
    err = soup.find('p', class_='error').text

    res.close()

    result = show_table()

    assert err == expec_err and result == (1111_2222_3333_4444, datetime.date(2024, 11, 1), 123, 
                                            datetime.date(2023, 11, 23), 'e162911d-bb32-46d2-80ba-840c0a1cb010', 'new')


@pytest.mark.parametrize(
    "number, expec_result",
    [
        (
            1111222233334444,
        '''[
                [
                    1111222233334444,
                    "Fri, 01 Nov 2024 00:00:00 GMT",
                    123,
                    "Thu, 23 Nov 2023 00:00:00 GMT",
                    "e162911d-bb32-46d2-80ba-840c0a1cb010",
                    "new"
                ]
            ]'''
        ),
        (1111222233334445, '[]'),
        (1111222, "Невірні вхідні данні"),
    ],
)
def test_show(number, expec_result, expect):
    url = "http://127.0.0.1:5000/show?number=" + str(number)
    response = requests.get(url)
    assert expec_result.replace('\n', '').replace(' ', '') == response.text.replace('\n', '').replace(' ', '')


if __name__ == "__main__":
    url = "http://127.0.0.1:5000/show?number=1111222233334444"
    response = requests.get(url)
    print(response.text)
