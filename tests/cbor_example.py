from eeprom import CBOR_EEPROM

eeprom = CBOR_EEPROM("24c64", 0, 0x54)

# Write sample data file
test_data = { 'some_key' : "This is a sample value." }
eeprom.write_file(test_data)

# Re-initialize to clear cached file
del eeprom
eeprom = CBOR_EEPROM("24c64", 0, 0x54)

# Read data file
verify_data = eeprom.read_file()
print(verify_data)
assert verify_data == test_data

# Re-initialize to clear cached file
del eeprom
eeprom = CBOR_EEPROM("24c64", 0, 0x54)

# Read data object
val = eeprom.get('some_key')
print(val)
assert val == test_data['some_key']

# Erase data file
eeprom.erase_file()
erased = eeprom.read_file()
print(erased)
assert erased == {}
