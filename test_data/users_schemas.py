signin_and_login_user_response_schema = {
    "type": "object",
    "properties": {
        "user": {
            "type": "object",
            "properties": {
                "_id": {"type": "string"},
                "firstName": {"type": "string"},
                "lastName": {"type": "string"},
                "email": {"type": "string"},
                "__v": {"type": "number"}
            },
            "required": ["_id", "firstName", "lastName", "email", "__v"]
        },
        "token": {"type": "string"}
    },
    "required": ["user", "token"]
}

update_and_get_user_profile_response_schema = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"},
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "email": {"type": "string"},
        "__v": {"type": "number"}
    },
    "required": ["_id", "firstName", "lastName", "email", "__v"]
}
