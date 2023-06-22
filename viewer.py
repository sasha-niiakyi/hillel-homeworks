from flask import Flask, render_template, request
from config import host, user, pwd, db_name
from card import Card
from card_repository import CardRepository


app = Flask('app')

@app.route('/')
def home():
    return '''<h1><a href='http://127.0.0.1:5000/create'>Create</a></h1>
              <h1><a href='http://127.0.0.1:5000/show?number=0'>Show</a></h1>'''


#всі перевірки не повні, роозумію
def check_number(number: str) -> bool:
    if len(number) != 16 or not number.isdigit():
        return True
    else:
        return False


def check_expir_date(expir_date: str) -> bool:
    if len(expir_date) != 7:
        return True

    fist_part = expir_date[:2]
    last_part = expir_date[3:]
    delim = expir_date[2]

    if len(fist_part) != 2 or len(last_part) != 4 or delim != '/':
        return True
    else:
        return False


def check_cvv(cvv: str) -> bool:
    if len(cvv) != 3 or not cvv.isdigit() or cvv[0] == '0':
        return True
    else:
        return False


def check_date_of_issue(date):
    if len(date[:4]) != 4 or not date[:4].isdigit():
        return True

    elif date[4:5] != '-' or date[-3:-2] != '-':
        return True

    elif len(date[5:7]) != 2 or not date[5:7].isdigit():
        return True

    elif len(date[-2:]) != 2 or not date[-2:].isdigit():
        return True

    else:
        return False


def check_user_id(user_id):
    return False


@app.route('/create', methods=["GET", "POST"])
def create():
    error = ''
    if request.method == 'POST':

        if check_number(number := request.form['number']):
            error = 'Невірний номер'

        elif check_expir_date(expir_date := request.form['expir_date']):
            error = 'Невірна дата закінчення'

        elif check_cvv(cvv := request.form['cvv']):
            error = 'Невірний cvv'

        elif check_date_of_issue(date_of_issue := request.form['date_of_issue']):
            error = 'Невірна дата створення'

        elif check_user_id(user_id := request.form['user_id']):
            error = 'Невірний айді юзера'

        else:
            card1 = Card(int(number), expir_date, int(cvv), date_of_issue, user_id, 'new')

            try:
                rep = CardRepository(host, user, pwd, db_name)
                rep.save(card1)
                error = 'Все добре'

            except:
                error = 'Така картка вже є'

            finally:
                rep.unconnect
    else:
        pass

    return render_template('create.html', title='Створення картки', error=error)


@app.route('/show', methods=["GET"])
def show():
    number = request.args.get('number', default='0')

    if check_number(number):
        result = 'Невірні вхідні данні'

    else:
        rep = CardRepository(host, user, pwd, db_name)
        result = rep.get(int(number))
        rep.unconnect

    return result


if __name__ == '__main__':
    app.run(debug=True)