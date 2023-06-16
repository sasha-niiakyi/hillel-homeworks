from config import host, user, pwd, db_name
from card import Card
from uuid import uuid4

import psycopg2


class CardRepository:

	@staticmethod
	def format_date(date: str) -> str:
		return date[3:] + '-' + date[:2] + '-01' 


	def __init__(self, host: str, user: str, pwd: str, db_name: str):
		try:
			self.con = psycopg2.connect(host=host, user=user, password=pwd, database=db_name)
			self.con.autocommit = True
		except:
			raise ConnectionError('Connection to database failed')
		self.cur = self.con.cursor()
		self.cur.execute('''CREATE TABLE IF NOT EXISTS cards(
								card_number BIGINT PRIMARY KEY NOT NULL,
								card_expir_date DATE NOT NULL,
								card_cvv INT NOT NULL,
								card_date_of_issue DATE NOT NULL,
								card_user_id UUID NOT NULL,
								card_status VARCHAR(20));''')


	def get(self, number: int) -> tuple:
		self.cur.execute('SELECT * FROM cards WHERE card_number = %s', (number,))
		return self.cur.fetchall()


	def save(self, card: Card):
		self.cur.execute('INSERT INTO cards VALUES(%s, %s, %s, %s, %s, %s)', card.attributes())


	def update_status(self, card: Card):
		upd = '''UPDATE cards SET card_status = %s WHERE card_number = %s'''
		self.cur.execute(upd, (card.status, card.number()))


	def find_by_expir_date(self, date: str) -> tuple:
		self.cur.execute('SELECT * FROM cards WHERE card_expir_date = %s', (self.format_date(date),))
		return self.cur.fetchall()


	def find_by_date_of_issue(self, date_of_issue: str) -> tuple:
		self.cur.execute('SELECT * FROM cards WHERE card_date_of_issue = %s', (date_of_issue,))
		return self.cur.fetchall()


if __name__ == '__main__':
	...
	# rep = CardRepository(host, user, pwd, db_name)
	# card1 = Card(1234_5678_9012_3456, '11/2024', 123, '2023-11-10', str(uuid4()), 'active')

	# rep.save(card1)
	# print(rep.get(1234_5678_9012_3456))

	# card1.status = 'blocked'
	# rep.update_status(card1)
	# print(rep.get(1234_5678_9012_3456))

	# print(rep.find_by_expir_date('11/2024'))
	# print('Good!')