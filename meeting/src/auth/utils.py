import re


PATTERN_NAME = re.compile(r"^\w{2,25}$")
NO_PATTERN_NAME = re.compile(r".*\W")

def name_validator(name: str) -> str:
	if not 2 <= len(name) <= 25:
		return 'Enter the name from 2 to 25 letters'

	if NO_PATTERN_NAME.match(name):
		return 'The name must contain only letters and numbers'

	return ''


PATTERN_PASSWORD = re.compile(r"^(?=.*?[A-Za-z])(?=.*?[0-9#?!@$%_^&*-]).{8,}$")

def password_validator(password: str) -> str:
	if len(password) < 8:
		return 'The password must contain more than 8 letters'

	if not PATTERN_PASSWORD.match(password):
		return 'The password also must contain numbers or special charapters'

	return ''

