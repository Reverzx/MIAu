class EditData:
    contact_data_only_mandatory = {
        'firstName': 'Polina',
        'lastName': 'Kulik',
    }

    contact_data = {
        'firstName': 'Polina',
        'lastName': 'Kulik',
        'birthdate': '1990-01-01',
        'email': 'it_test@testmail.com',
        'phone': '+375291234561',
        'street1': 'Molokova str',
        'street2': '123/A',
        'city': 'Orsha',
        'stateProvince': 'Vitebsk',
        'postalCode': '211030',
        'country': 'Belarus',
    }

    updated_data = {
        'firstName': 'Marina',
        'lastName': 'Kulikova',
        'birthdate': '1990-10-10',
        'email': 'it_test_upd@testmail.com',
        'phone': '+375291234500',
        'street1': 'Mir str',
        'street2': '5',
        'city': 'Minsk',
        'stateProvince': 'Minsk',
        'postalCode': '200000',
        'country': 'The Republic of Belarus',
    }

    error_message = {
        'email': 'Validation failed: email: Email is invalid',
        'phone': 'Validation failed: phone: Phone number is invalid',
        'birthdate': 'Validation failed: birthdate: Birthdate is invalid',
    }

    max_length_allowed = {
        '20 chars': 'ABCDEFGHIJKLMNOPQRST',
        '15 chars': '+1 800-555-5555',
        '40 chars': 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMN',
        '10 chars': '12345-6789',
    }

    max_length_allowed_filled = {
        'firstName': 'ABCDEFGHIJKLMNOPQRST',
        'lastName': 'ABCDEFGHIJKLMNOPQRST',
        'birthdate': '1990-10-10',
        'email': 'it_test_upd@testmail.com',
        'phone': '+1 800-555-5555',
        'street1': 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMN',
        'street2': 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMN',
        'city': 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMN',
        'stateProvince': 'ABCDEFGHIJKLMNOPQRST',
        'postalCode': '12345-6789',
        'country': 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMN',
    }

    max_length_exceeded = [
        ('firstName', 'ABCDEFGHIJKLMNOPQRSTU',
         'Validation failed: firstName: Path `firstName` (`ABCDEFGHIJKLMNOPQRSTU`) '
         'is longer than the maximum allowed length (20).'),
        ('lastName', 'ABCDEFGHIJKLMNOPQRSTU',
         'Validation failed: lastName: Path `lastName` (`ABCDEFGHIJKLMNOPQRSTU`)'
         ' is longer than the maximum allowed length (20).'),
        ('phone', '+375 029 1234567',
         'Validation failed: phone: Path `phone` (`+375 029 1234567`)'
         ' is longer than the maximum allowed length (15).'),
        ('street1', 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNO',
         'Validation failed: street1: Path `street1` (`ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNO`)'
         ' is longer than the maximum allowed length (40).'),
        ('street2', 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNO',
         'Validation failed: street2: Path `street2` (`ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNO`)'
         ' is longer than the maximum allowed length (40).'),
        ('city', 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNO',
         'Validation failed: city: Path `city` (`ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNO`)'
         ' is longer than the maximum allowed length (40).'),
        ('stateProvince', 'ABCDEFGHIJKLMNOPQRSTU',
         'Validation failed: stateProvince: Path `stateProvince` (`ABCDEFGHIJKLMNOPQRSTU`)'
         ' is longer than the maximum allowed length (20).'),
        ('postalCode', '12345-67890',
         'Validation failed: postalCode: Path `postalCode` (`12345-67890`)'
         ' is longer than the maximum allowed length (10).'),
        ('country', 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNO',
         'Validation failed: country: Path `country` (`ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNO`)'
         ' is longer than the maximum allowed length (40).'),
    ]

    invalid_emails = [
        ('test.test.com', 'missing @ symbol'),
        ('.test@test.com', 'local part starts with a dot (.)'),
        ('test.@test.com', 'local part ends with a dot (.)'),
        ('test..test@test.com', 'local part has two consecutive dots (..)'),
        ('test@testcom', 'domain part has no a dot'),
        ('test@test_test.com', 'not allowed symbol (_) in domain part'),
        ('test@test+test.com', 'not allowed symbol (+) in domain part'),
        ('test@test%test.com', 'not allowed symbol (%) in domain part'),
        ('test @test.com', 'space before the @ symbol'),
        ('test@ test.com', 'space after the @ symbol'),
        ('test@test. com', 'space in the domain'),
        ('ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNABCDEFGHIJKLMNOPQRSTABCD1@test.com',
         'exceeds max length allowed (64 chars)'),
        (' ', 'a space'),
    ]

    valid_emails = [
        'AB_CDE%FGHIJ+KLMNO-PQRST.UVWXYZ@ABCDEFGHIJKLMNO-PQRST.UVWXYZ.org',
        'ab_cde%fghijk+lmno-pqrstu.vwxyz@abcdefghijklmno-pqrstu.vwxyz.net',
        '1.23_45%67+89-0@1.23456789-0.com',
        ' test@test.com',
        'test@test.com '
    ]

    mandatory_fields_errors = [
        ('firstName', '', 'Validation failed: firstName: Path `firstName` is required.'),
        ('firstName', ' ', 'Validation failed: firstName: Path `firstName` is required.'),
        ('firstName', None, 'Validation failed: firstName: Path `firstName` is required.'),
        ('lastName', '', 'Validation failed: lastName: Path `lastName` is required.'),
        ('lastName', ' ', 'Validation failed: lastName: Path `lastName` is required.'),
        ('lastName', None, 'Validation failed: lastName: Path `lastName` is required.'),
    ]

    invalid_phones = [
        '+375.29.1234567',
        '+37529123456o',
        '+375-29-1234567',
        '+375/29/1234567',
        '+375,29,1234567',
        '+375(29)1234561',
        '+375 29 1234567',
        ' '
    ]

    valid_phones = [
        '+375291234561',
        '(202) 555-0198',
        '+447911123456',
        '+919876543210',
        '+61412345678',
    ]

    invalid_birthdate = [
        ('01-01-1990', 'Invalid format: dd-MM-yyyy'),
        ('1990-13-12', 'Invalid months: Month out of range'),
        ('2023-04-31', 'Invalid day: Day out of range'),
        ('1990-12/30', 'Invalid symbol: /'),
        ('1990.12.30', 'Invalid symbol: .'),
        ('1990 12 30', 'Space is not allowed'),
        ('2023-02-29', 'Invalid date for a non-leap year'),
        ('1999-1-1', 'Invalid format: "1" instead of "01"'),
        (' ', 'No date'),
    ]

    valid_birthdate = [
        '1990/12/30',
        '1990-12-30',
        '2020-02-29',
    ]
