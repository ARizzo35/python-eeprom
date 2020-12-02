import setuptools

setuptools.setup(
    name="eeprom",
    version="0.0.5",
    author="Adam Rizkalla",
    author_email="a1rizkalla@gmail.com",
    description="A pure Python 3 library for Linux sysfs EEPROM devices.",
    long_description="""python-eeprom is a pure Python 3 library for initializing, reading, and writing EEPROM devices in userspace Linux. It is useful in embedded Linux environments, including custom hardware based platforms. python-eeprom also includes a wrapper class for managing storage and retrieval of CBOR files in EEPROM (using 'cbor2' library). python-eeprom is MIT licensed. See https://github.com/ARizzo35/python-eeprom for more information.""",
    url="https://github.com/ARizzo35/python-eeprom.git",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Hardware',
        'Topic :: System :: Hardware :: Hardware Drivers'
    ],
    setup_requires = [
        'wheel'
    ],
    install_requires = [
        'cbor2>=5.2.0'
    ],
    entry_points = {
        'console_scripts': [
            'cbor_eeprom=eeprom.cbor_eeprom:main',
        ],
    },
    python_requires='~=3.7',
    license='MIT',
    keywords='eeprom at24 embedded linux',
)
