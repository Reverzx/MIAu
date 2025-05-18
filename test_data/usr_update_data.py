from test_data.user_creds import UserCredentials as UC

user_to_be_update = {
    "firstName": 'Johny',
    "lastName": 'Whiskers',
    "email": 'best@mail.soap',
    "password": 'thepassword'
}

upd_data = {
    "firstName": 'uJohny',
    "lastName": 'uWhiskers',
    "email": 'ubest@mail.soap',
    "password": 'uthepassword'
}

upd_usr_with_empty_fields = [
    ({"firstName": "", "lastName": UC.to_be_update_lname, "email": UC.to_be_update_email,
      "password": UC.to_be_update_password}, 'Empty First name field', 'firstName'),
    ({"firstName": UC.to_be_update_fname, "lastName": "", "email": UC.to_be_update_email,
      "password": UC.to_be_update_password}, 'Empty Last namt field', 'lastName'),
    ({"firstName": UC.to_be_update_fname, "lastName": UC.to_be_update_lname,
      "email": "", "password": UC.to_be_update_password}, 'Empty email field', 'email'),
    ({"firstName": UC.to_be_update_fname, "lastName": UC.to_be_update_lname,
      "email": UC.to_be_update_email, "password": ""}, 'Empty password field', 'password')
]
upd_usr_with_some_empty_fields = [
    ({"firstName": "", "lastName": UC.to_be_update_lname, "email": UC.to_be_update_email,
      "password": UC.to_be_update_password}, 'Empty First name field', 'firstName'),
    ({"firstName": UC.to_be_update_fname, "lastName": "", "email": UC.to_be_update_email,
      "password": UC.to_be_update_password}, 'Empty Last namt field', 'lastName'),
    ({"firstName": UC.to_be_update_fname, "lastName": UC.to_be_update_lname,
      "email": "", "password": UC.to_be_update_password}, 'Empty email field', 'email')
]

invalid_data_to_upd = [
    ({"firstName": UC.to_be_update_fname, "lastName": UC.to_be_update_lname,
      "email": 'updbestmail.soap', "password": UC.to_be_update_password}, 'Email without "@"'),
    ({"firstName": UC.to_be_update_fname, "lastName": UC.to_be_update_lname,
      "email": 'updbest@mail', "password": UC.to_be_update_password}, 'Email without domain'),
    ({"firstName": UC.to_be_update_fname, "lastName": UC.to_be_update_lname,
      "email": 'updbest@ma il.soap', "password": UC.to_be_update_password}, 'Space in email'),
    ({"firstName": UC.to_be_update_fname, "lastName": UC.to_be_update_lname,
      "email": '@mail.soap', "password": UC.to_be_update_password}, 'Email without body'),
    ({"firstName": UC.to_be_update_fname, "lastName": UC.to_be_update_lname,
      "email": UC.to_be_update_email, "password": 'updb'}, 'Short password')
]
