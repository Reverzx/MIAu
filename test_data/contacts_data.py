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