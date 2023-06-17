from conftest import host, user, pwd, db_name
from card_repository import CardRepository
from uuid import uuid4
from card import Card
import datetime
import pytest
import psycopg2


@pytest.mark.parametrize(
	"old_status, new_status, expec_result", [('new', 'active', 'active'),
											('active', 'blocked', 'blocked'),
											('active', 'new', 'new'),
											('new', 'blocked', 'blocked')]
)
def test_card_status(old_status, new_status, expec_result):
	''''''
	card1 = Card(1234_5678_9012_3456, '11/2024', 123, '2023-11-10', str(uuid4()), old_status)
	card1.status = new_status
	assert card1.status == expec_result


@pytest.mark.parametrize(
	"old_status, new_status, expec_exception", [('blocked', 'active', AssertionError),
												('blocked', 'new', AssertionError),
												('active', 'dead', ValueError)]
)
def test_card_status_error(old_status, new_status, expec_exception):
	card1 = Card(1234_5678_9012_3456, '11/2024', 123, '2023-11-10', str(uuid4()), old_status)
	with pytest.raises(expec_exception):
		card1.status = new_status


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
				'2023-11-10', 'e162911d-bb32-46d2-80ba-840c0a1cb010', 'active');''')
	con.commit()

	cur.execute('''SELECT * FROM cards WHERE card_number = 1111222233334444''')

	expect = cur.fetchone()

	cur.close()
	con.close()

	return expect


def test_read_repository(expect):
	rep = CardRepository(host, user, pwd, db_name)

	result = rep.get(1111222233334444)
	rep.unconnect()

	assert result[0] == expect


@pytest.fixture
def clear_table():
	con = psycopg2.connect(host=host, user=user, password=pwd, database=db_name)
	cur = con.cursor()

	cur.execute('DELETE FROM cards')
	con.commit()

	cur.close()
	con.close()


def show_table():
	con = psycopg2.connect(host=host, user=user, password=pwd, database=db_name)
	cur = con.cursor()

	cur.execute('SELECT * FROM cards')
	result = cur.fetchone()

	cur.close()
	con.close()

	return result


def test_save_to_repository(clear_table):
	rep = CardRepository(host, user, pwd, db_name)
	card1 = Card(1111_2222_3333_4444, '11/2024', 123, 
				'2023-11-10', 'e162911d-bb32-46d2-80ba-840c0a1cb010', 'active')

	rep.save(card1)
	rep.unconnect()

	result = show_table()

	assert result == (1111_2222_3333_4444, datetime.date(2024, 11, 1), 123, 
				datetime.date(2023, 11, 10), 'e162911d-bb32-46d2-80ba-840c0a1cb010', 'active')




	