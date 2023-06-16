from config.py import host, user, pwd, db_name


class CardRepository:

	@staticmethod
	def format_date(date: str) -> str:
		return date[3:] + '-' + date[:2] + '-01' 


	def __init__(self):
		try:
			self.con = psycopg2.connect(host=host, user=user, password=pwd, database=db_name)
		except:
			raise ConnectionError('Connection to database failed')
		self.cur = con.cursor()
		self.cur.execute('''CREATE TABLE IF NOT EXISTS cards(
								card_number INT PRIMARY KEY NOT NULL,
								card_expir_date DATE NOT NULL,
								card_cvv INT NOT NULL,
								card_date_of_issue DATE NOT NULL,
								card_user_id UUID NOT NULL,
								card_status VARCHAR(20));''')


	def get(self, number: int) -> tuple:
		self.cur.execute('SELECT * FROM cards WHERE card_number = %s', number)
		return self.cur.fetchall()


	def save(self, card: Card):
		self.cur.execute('INSERT INTO cards VALUES(%s, %s, %s, %s, %s, %s)', card.attributs())


	def find_by_expir_date(self, date: str) -> tuple:
		self.cur.execute('SELECT * FROM cards WHERE expir_date = %s', format_date(date))
		return self.cur.fetchall()


	def find_by_date_of_issue(self, date_of_issue: str) -> tuple:
		self.cur.execute('SELECT * FROM cards WHERE date_of_issue = %s', date_of_issue)
		return self.cur.fetchall()


if __name__ == '__main__':
    print('hello')