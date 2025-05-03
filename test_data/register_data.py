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
