from test_data.user_creds import UserCredentials as UC


invalid_email_ui_data = [
    (UC.register_new_first_name, UC.register_new_last_name, ' ', UC.register_new_password,
     'Empty Email field'),
    (UC.register_new_first_name, UC.register_new_last_name, 'dontforget.me',
     UC.register_new_password, 'Email without "@"'),
    (UC.register_new_first_name, UC.register_new_last_name, 'dont@forget',
     UC.register_new_password, 'Email without domain'),
    (UC.register_new_first_name, UC.register_new_last_name, 'dont@ forget.me',
     UC.register_new_password, 'Space in email'),
    (UC.register_new_first_name, UC.register_new_last_name, '@forget.me', UC.register_new_password,
      'Email without body')
]

short_pasword_ui_data = [
    (UC.register_new_first_name, UC.register_new_last_name, UC.register_new_email, 'd'),
    (UC.register_new_first_name, UC.register_new_last_name, UC.register_new_email, 'do'),
    (UC.register_new_first_name, UC.register_new_last_name, UC.register_new_email, 'don'),
    (UC.register_new_first_name, UC.register_new_last_name, UC.register_new_email, 'dont'),
    (UC.register_new_first_name, UC.register_new_last_name, UC.register_new_email, 'dontf'),
    (UC.register_new_first_name, UC.register_new_last_name, UC.register_new_email, 'dontfo')
]

user_to_add = {
    "firstName": UC.register_new_first_name,
    "lastName": UC.register_new_first_name,
    "email": UC.register_new_email,
    "password": UC.register_new_password
    }

exist_user = {
    "firstName": UC.exist_usr_fname,
    "lastName": UC.exist_usr_lname,
    "email": UC.exist_usr_email,
    "password": UC.exist_usr_password
    }

usr_to_delete = {
    "firstName": UC.to_delete_fname,
    "lastName": UC.to_delete_lname,
    "email": UC.to_delete_email,
    "password": UC.to_delete_password
}

invalid_reg_data_api = [
    ({"firstName": "", "lastName": UC.register_new_last_name,
      "email": UC.register_new_email, "password": UC.register_new_password},
      'Empty First name field'),
    ({"firstName": UC.register_new_first_name, "lastName": "",
      "email": UC.register_new_email, "password": UC.register_new_password},
      'Empty Last namt field'),
    ({"firstName": UC.register_new_first_name, "lastName": UC.register_new_last_name,
      "email": "", "password": UC.register_new_password}, 'Empty email field'),
    ({"firstName": UC.register_new_first_name, "lastName": UC.register_new_last_name,
      "email": UC.register_new_email, "password": ""}, 'Empty password field'),
    ({"firstName": UC.register_new_first_name, "lastName": UC.register_new_last_name,
      "email": 'dontforget.me', "password": UC.register_new_password}, 'Email without "@"'),
    ({"firstName": UC.register_new_first_name, "lastName": UC.register_new_last_name,
      "email": 'dont@forget', "password": UC.register_new_password}, 'Email without domain'),
    ({"firstName": UC.register_new_first_name, "lastName": UC.register_new_last_name,
      "email": 'dont@ forget.me', "password": UC.register_new_password}, 'Space in email'),
    ({"firstName": UC.register_new_first_name, "lastName": UC.register_new_last_name,
      "email": '@forget.me', "password": UC.register_new_password}, 'Email without body'),
    ({"firstName": UC.register_new_first_name, "lastName": UC.register_new_last_name,
      "email": UC.register_new_email, "password": 'dontfo'}, 'Short password')
]
