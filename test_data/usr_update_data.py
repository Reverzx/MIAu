from test_data.user_creds import UserCredentials as UC

usr_to_be_update = {
    "firstName": UC.to_be_update_fname,
    "lastName": UC.to_be_update_lname,
    "email": UC.to_be_update_email,
    "password": UC.to_be_update_password
}

upd_data = {
    "firstName": f'upd{UC.to_be_update_fname}',
    "lastName": f'upd{UC.to_be_update_lname}',
    "email": f'upd{UC.to_be_update_email}',
    "password": f'upd{UC.to_be_update_password}'
}

upd_usr_with_empty_fields = [
    ({"firstName": "", "lastName": UC.to_be_update_lname, "email": UC.to_be_update_email,
      "password": UC.to_be_update_password}, 'Empty First name field', 'First name'),
    ({"firstName": UC.to_be_update_fname, "lastName": "", "email": UC.to_be_update_email,
      "password": UC.to_be_update_password}, 'Empty Last namt field', 'Last name'),
    ({"firstName": UC.to_be_update_fname, "lastName": UC.to_be_update_lname,
      "email": "", "password": UC.to_be_update_password}, 'Empty email field', 'Email'),
    ({"firstName": UC.to_be_update_fname, "lastName": UC.to_be_update_lname,
      "email": UC.to_be_update_email, "password": ""}, 'Empty password field', 'Password')
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
