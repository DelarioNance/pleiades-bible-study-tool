# cases_get_db_url.py

class GetDbUrlCases:

    # -----------------------------------------------------
    # Valid cases
    # -----------------------------------------------------
    VALID = [
        {
            "alias": "test",
            "user": "test_user",
            "password": "test_pass",
            "name": "mydb_test",
            "expected": "postgresql+psycopg2://test_user:test_pass@localhost/mydb_test",
        },
        {
            "alias": "prod",
            "user": "prod_user",
            "password": "prod_pass",
            "name": "mydb_prod",
            "expected": "postgresql+psycopg2://prod_user:prod_pass@localhost/mydb_prod",
        },
    ]

    # -----------------------------------------------------
    # Invalid cases
    # -----------------------------------------------------
    INVALID = [
        {"alias": "TEST"},
        {"alias": "PROD"},
        {"alias": "other"},
    ]
