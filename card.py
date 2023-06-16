class Card:

    def __init__(self, number: int, expir_date: str, cvv: int,
                date_of_issue: str, user_id: str, status: str):
        self.__number = number
        self.__expir_date = expir_date[3:] + '-' + expir_date[:2] + '-01' 
        self.__cvv = cvv
        self.__date_of_issue = date_of_issue
        self.__user_id = user_id
        self.__status = status


    def number(self) -> int:
        return self.__number


    @property
    def status(self) -> str:
        return self.__status


    @status.setter
    def status(self, new_status: str):
        values = ('new', 'active', 'blocked')

        if new_status not in values:
            raise ValueError('Value entered incorrectly')

        elif self.__status == 'blocked':
            raise AssertionError('A blocked card cannot be activated')

        else:
            self.__status = new_status


    def attributes(self) -> tuple:
        return (self.__number,
                self.__expir_date,
                self.__cvv,
                self.__date_of_issue,
                self.__user_id,
                self.__status)


if __name__ == '__main__':
    print('hello')