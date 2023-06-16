from conftest import host, user, pwd, db_name
from card_repository import CardRepository
from uuid import uuid4
from card import Card
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







	