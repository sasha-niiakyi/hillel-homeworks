from datetime import datetime as datetime_type


def datetime_validator(datetime: str) -> str:
	try:
		datetime = datetime_type.strptime(datetime, '%Y-%m-%d %H:%M')
		print(type(datetime))
	except:
		return 'The date was written wrong'

	if datetime < datetime_type.now():
		return 'Why are you creating the meeting in the past?'

	return ''
