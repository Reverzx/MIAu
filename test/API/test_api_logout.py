import pytest
import requests
from loguru import logger
from test_data.env import Env
from test_data.user_creds import UserCredentials
from api_actions.api_logout import post_logout
from api_actions.api_logout import assert_unauthorized_request
from api_actions.login_and_get_token import login_and_get_token


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.api
def test_successful_post_logout():
    auth_token = login_and_get_token(UserCredentials.it_email,
                                     UserCredentials.it_password)
    logout = post_logout(auth_token)
    assert logout.status_code == 200, (f"Wrong status code: {logout.status_code}. "
                                       f"Expected: 200")


@pytest.mark.regression
@pytest.mark.api
def test_post_logout_fails_without_authorization():
    url = f"{Env.URL_Login}/users/logout"
    logout = requests.post(url)
    assert_unauthorized_request(logout)


@pytest.mark.api
def test_post_logout_fails_for_expired_auth_token():
    auth_token = login_and_get_token(UserCredentials.it_email,
                                     UserCredentials.it_password)
    logout_one = post_logout(auth_token)
    assert logout_one.status_code == 200, \
        f"Wrong status code: {logout_one.status_code}. Expected: 200"
    logout_two = post_logout(auth_token)
    assert_unauthorized_request(logout_two)


@pytest.mark.regression
@pytest.mark.api
def test_post_logout_fails_for_invalid_auth_token():
    auth_token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODBhNWJiNWRjZWQ4"
                  "NjAwMTU3MTUwMGQiLCJpYXQiOjE3NDU1ODg0OTd9.pFSSiLVs59eIScuf514wvX6"
                  "V2q-h6ny-loNg2P0U57s")
    logout = post_logout(auth_token)
    assert_unauthorized_request(logout)


@pytest.mark.api
def test_post_logout_fails_for_auth_token_of_a_deleted_user():
    # Add a new user and retrieve the auth token.
    add_user = requests.post(
        f"{Env.URL_Login}/users",
        json={
            "firstName": "Test",
            "lastName": "User",
            "email": "delete_test@fake.com",
            "password": "Password"
        }
    )
    auth_token = add_user.json()["token"]
    logger.info("A new user was added. Auth token was retrieved.")

    # Delete the added user. Save the auth token.
    requests.delete(
        f"{Env.URL_Login}/users/me",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    logger.info("The added user was deleted. The auth token was saved.")

    # Attempt to log out using the auth token of the deleted user.
    logout = post_logout(auth_token)
    assert_unauthorized_request(logout)
    logger.success("Logout failed as expected with 401 Unauthorized.")
