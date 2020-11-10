from eeprom import EEPROM

eeprom = EEPROM("24c64", 0, 0x54)

test_string = "This is a string of test data."
test_length = len(test_string)

eeprom.write(test_string.encode())
verify = eeprom.read(test_length).decode()

print(verify)

assert verify == test_string
