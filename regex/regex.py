import re


def is_passport_number(text: str) -> bool:
	#AA12345
	#[A-Z]{2}\d{5}
	return True if re.fullmatch(r'[A-Z]{2}\d{5}', text) else False


def is_ipn(text: str) -> bool:
	#1234567890
	#\d{10}
	return True if re.fullmatch(r'\d{10}', text) else False


def is_car_number_dnipro(text: str) -> bool:
	#AE1234BB, #KE1234BB
	#(AE|KE)\d{4}[A-Z]{2}
	return True if re.fullmatch(r'(AE|KE)\d{4}[A-Z]{2}', text) else False


def is_car_number_kharkiv(text: str) -> bool:
	#AX1234BB, #KX1234BB
	#(AX|KX)\d{4}[A-Z]{2}
	return True if re.fullmatch(r'(AX|KX)\d{4}[A-Z]{2}', text) else False

# print(is_passport_number('AA12345'))
# print(is_ipn('1234567890'))
# print(is_car_number_dnipro('KE1234BB'))
# print(is_car_number_kharkiv('KX1234BB'))