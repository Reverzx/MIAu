from test_data.user_creds import UserCredentials as UC


invalid_email_ui = [
    (UC.reg_new_fname, UC.reg_new_lname, ' ', UC.reg_new_password, 'Empty Email field'),
    (UC.reg_new_fname, UC.reg_new_lname, 'dontforget.me', UC.reg_new_password, 'Email without "@"'),
    (UC.reg_new_fname, UC.reg_new_lname, 'dont@forget', UC.reg_new_password, 'Email without domain'),
    (UC.reg_new_fname, UC.reg_new_lname, 'dont@ forget.me', UC.reg_new_password, 'Space in email'),
    (UC.reg_new_fname, UC.reg_new_lname, '@forget.me', UC.reg_new_password, 'Email without body')
]

short_pasword_ui = [
    (UC.reg_new_fname, UC.reg_new_lname, UC.reg_new_email, 'd'),
    (UC.reg_new_fname, UC.reg_new_lname, UC.reg_new_email, 'do'),
    (UC.reg_new_fname, UC.reg_new_lname, UC.reg_new_email, 'don'),
    (UC.reg_new_fname, UC.reg_new_lname, UC.reg_new_email, 'dont'),
    (UC.reg_new_fname, UC.reg_new_lname, UC.reg_new_email, 'dontf'),
    (UC.reg_new_fname, UC.reg_new_lname, UC.reg_new_email, 'dontfo')
]

usr_to_add = {
    "firstName": UC.reg_new_fname,
    "lastName": UC.reg_new_lname,
    "email": UC.reg_new_email,
    "password": UC.reg_new_password
    }

exist_usr = usr_to_add = {
    "firstName": UC.reg_new_fname,
    "lastName": UC.reg_new_lname,
    "email": UC.reg_new_email,
    "password": UC.reg_new_password
    }

invalid_reg_data_api = [
    ({"firstName": "", "lastName": UC.reg_new_lname, \
      "email": UC.reg_new_email, "password": UC.reg_new_password}, 'Empty First name field'),
    ({"firstName": UC.reg_new_fname, "lastName": "", \
      "email": UC.reg_new_email, "password": UC.reg_new_password}, 'Empty Last namt field'),
    ({"firstName": UC.reg_new_fname, "lastName": UC.reg_new_lname, \
      "email": "", "password": UC.reg_new_password}, 'Empty email field'),
    ({"firstName": UC.reg_new_fname, "lastName": UC.reg_new_lname, \
      "email": UC.reg_new_email, "password": ""}, 'Empty password field'),
    ({"firstName": UC.reg_new_fname, "lastName": UC.reg_new_lname, \
      "email": 'dontforget.me', "password": UC.reg_new_password}, 'Email without "@"'),
    ({"firstName": UC.reg_new_fname, "lastName": UC.reg_new_lname, \
      "email": 'dont@forget', "password": UC.reg_new_password}, 'Email without domain'),
    ({"firstName": UC.reg_new_fname, "lastName": UC.reg_new_lname, \
      "email":'dont@ forget.me', "password": UC.reg_new_password}, 'Space in email'),
    ({"firstName": UC.reg_new_fname, "lastName": UC.reg_new_lname, \
      "email": '@forget.me', "password": UC.reg_new_password}, 'Email without body'),
    ({"firstName": UC.reg_new_fname, "lastName": UC.reg_new_lname, \
      "email": UC.reg_new_email, "password": 'dontfo'}, 'Short password')
]
