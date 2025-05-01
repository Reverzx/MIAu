from test_data.user_creds import UserCredentials


invalid_login_data_ui = [
    ('240425test @test.com', UserCredentials.it_password, "Invalid email format (space)"),
    ('240425test@test.', UserCredentials.it_password, "Invalid email format (no domain)"),
    (UserCredentials.it_email, 'Passw0rd', "Wrong password"),
    (UserCredentials.not_registered_email, UserCredentials.it_password, "Not registered user"),
    ('', UserCredentials.it_password, "Missing email"),
    (UserCredentials.it_email, '', "Missing password"),
    (UserCredentials.updated_old_email, UserCredentials.updated_old_password, "Old credentials"),
    (UserCredentials.deleted_email, UserCredentials.deleted_password, "Deleted user"),
]

invalid_login_data_api = [
    ('240425test @test.com', UserCredentials.it_password, "Invalid email format (space)"),
    ('240425test@test.', UserCredentials.it_password, "Invalid email format (no domain)"),
    (UserCredentials.it_email, 'Passw0rd', "Wrong password"),
    (UserCredentials.not_registered_email, UserCredentials.it_password,
     "Email of a not registered user"),
    (UserCredentials.updated_old_email, UserCredentials.updated_old_password,
     "Old credentials after update"),
    (UserCredentials.deleted_email, UserCredentials.deleted_password,
     "Credentials of a deleted user"),
    ("", UserCredentials.it_password, "Missing email"),
    (" ", UserCredentials.it_password, "Space as an email"),
    (None, UserCredentials.it_password, "None as an email"),
    (UserCredentials.it_email, "", "Missing password"),
    (UserCredentials.it_email, " ", "Space as an password"),
    (UserCredentials.it_email, None, "None as an password"),
]
