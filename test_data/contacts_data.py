from test_data.user_creds import UserCredentials as UC

user_to_add_contact = {
    "firstName": UC.usr_to_add_cont_fname,
    "lastName": UC.usr_to_add_cont_lname,
    "email": UC.usr_to_add_cont_email,
    "password": UC.usr_to_add_cont_password
}

user_to_up_cont = {
    "firstName": UC.usr_to_add_cont_fname,
    "lastName": UC.usr_to_add_cont_lname,
    "email": UC.usr_to_add_cont_email,
    "password": UC.usr_to_add_cont_password
}

nc_fname = 'Richard'
nc_lname = 'Moser'
nc_bdate = '1975-03-12'
nc_email = 'mail@post.post'
nc_phone = '88005553535'
nc_str1 = '22 Main street'
nc_str2 = 'Apartment 42'
nc_city = 'Castle Rock'
nc_state = 'Man'
nc_postcode = '212850'
nc_country = 'USA'

new_contact_valid_data = {
    "firstName": nc_fname,
    "lastName": nc_lname,
    "birthdate": nc_bdate,
    "email": nc_email,
    "phone": nc_phone,
    "street1": nc_str1,
    "street2": nc_str2,
    "city": nc_city,
    "stateProvince": nc_state,
    "postalCode": nc_postcode,
    "country": nc_country
}

new_cont_cancel_data = {
    "firstName": 'Ralf',
    "lastName": 'Stokinger'
}

ncw_fname = 'Harald'               # New contact data for negative test
ncw_lname = 'Johnson'
ncw_bdate = '1965-12-25'
ncw_email = 'soap@post.post'
ncw_phone = '2128506'
ncw_str1 = '33 Winners Avenue'
ncw_str2 = 'Room 404'
ncw_city = 'Toronto'
ncw_state = 'Ontario'
ncw_postcode = '3345'
ncw_country = 'Canada '

new_contact_not_full_data = {
    "firstName": 'Akki',
    "lastName": 'Tostison'
}

new_contact_empty_mandatory_fields = [
    ({"firstName": "", "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Empty First name field'),
    ({"firstName": ncw_fname, "lastName": "", "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Empty Last name field'),
    ({"firstName": "", "lastName": "", "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Empty First name and Last name fields')
]

new_contact_invalid_data = [
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": '1965-13-25', "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Invalid birthdate'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate,
      "email": 'soappost.post',
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Invalid email'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": 'zipcode', "country": ncw_country},
     'Invalid postal code')
]

invalid_phone = [
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": '+379-33-685-156', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Invalid phone number format'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate,
      "email": ncw_email,
      "phone": '22335', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Short phone number'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": '123045678912345', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Phone number contains 15 symbols'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": '1230456789123456', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Phone number is longer, than 15 symbols')
]

invalid_adress_data = [
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": '42',
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Invalid city name'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": '42', "postalCode": ncw_postcode, "country": ncw_country},
     'Invalid state name'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": '42'},
     'Invalid country name'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": '____',
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Invalid city name'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": '_____', "postalCode": ncw_postcode, "country": ncw_country},
     'Invalid state name'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": '______'},
     'Invalid country name')
]

error_fname_msg = 'Contact validation failed: firstName: Path `firstName` is required.'
error_lname_msg = 'Contact validation failed: lastName: Path `lastName` is required.'
error_mfields_msg = "Contact validation failed: firstName: Path `firstName` is required., " \
  "lastName: Path `lastName` is required."
error_bdate_msg = 'Contact validation failed: birthdate: Birthdate is invalid'
error_email_msg = 'Contact validation failed: email: Email is invalid'
error_phone_msg = 'Contact validation failed: phone: Phone number is invalid'
error_postcode_msg = 'Contact validation failed: postalCode: Postal code is invalid'

long_phone_numb = '012345678987654321'

ui_new_cont_empty_mand_fields = [
    ({"firstName": "", "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Empty First name field', error_fname_msg),
    ({"firstName": ncw_fname, "lastName": "", "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Empty Last name field', error_lname_msg),
    ({"firstName": "", "lastName": "", "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Empty First name and Last name fields', error_mfields_msg)
]

ui_new_cont_invalid_data = [
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": '1965-13-25', "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Invalid birthdate', error_bdate_msg),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate,
      "email": 'soappost.post',
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Invalid email', error_email_msg),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": 'zipcode', "country": ncw_country},
     'Invalid postal code', error_postcode_msg)
]

ui_inv_phone = [
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": '+379-33-685-156', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Invalid phone number format', error_phone_msg),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate,
      "email": ncw_email,
      "phone": '22335', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Short phone number', error_phone_msg),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": '123045678912345', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Phone number contains 15 symbols', error_phone_msg),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": long_phone_numb, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
     'Phone number is longer, than 15 symbols',
     f'Contact validation failed: phone: Path `phone` (`{long_phone_numb}`) is longer than '
     'the maximum allowed length (15).')
]
