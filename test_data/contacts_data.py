from test_data.user_creds import UserCredentials as UC

user_to_add_cont = {
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

new_cont_valid_data = {
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

new_cont_not_full = {
    "firstName": 'Akki',
    "lastName": 'Tostison'
}

new_cont_empty_mand_fields = [
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

new_cont_invalid_data = [
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": '1965-13-25', "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
      'Invalid birthdate'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": 'soappost.post',
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
      'Invalid email'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": ncw_phone, "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": 'zipcode', "country": ncw_country},
      'Invalid postal code')
]

inv_phone = [
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": '1965-13-25', "email": ncw_email,
      "phone": '+379-33-685-156', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
      'Invalid phone number format'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": 'soappost.post',
      "phone": '22335', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
      'Short phone number'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": 'soappost.post',
      "phone": '0123456789123', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": ncw_postcode, "country": ncw_country},
      'Phone number is longer, than 11 symbols and shorter, than 15'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": '123045678912345', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": 'zipcode', "country": ncw_country},
      'Phone number contains 15 symbols'),
    ({"firstName": ncw_fname, "lastName": ncw_lname, "birthdate": ncw_bdate, "email": ncw_email,
      "phone": '1230456789123456', "street1": ncw_str1, "street2": ncw_str2, "city": ncw_city,
      "stateProvince": ncw_state, "postalCode": 'zipcode', "country": ncw_country},
      'Phone number is longer, than 15 symbols')
]

inv_adress_data = [
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
