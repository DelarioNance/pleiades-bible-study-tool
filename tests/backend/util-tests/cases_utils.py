# cases_get_db_url.py

class GetDbUrlCases:

    # -----------------------------------------------------
    # Valid cases
    # -----------------------------------------------------
    VALID = [
        {
            "alias": "sandbox",
            "user": "sandbox_user",
            "password": "sandbox_pass",
            "name": "mydb_sandbox",
            "host": "localhost",
            "expected": "postgresql+psycopg2://sandbox_user:sandbox_pass@localhost/mydb_sandbox",
        },
        {
            "alias": "prod",
            "user": "prod_user",
            "password": "prod_pass",
            "name": "mydb_prod",
            "host": "localhost",
            "expected": "postgresql+psycopg2://prod_user:prod_pass@localhost/mydb_prod",
        },
    ]

    # -----------------------------------------------------
    # Invalid cases
    # -----------------------------------------------------
    INVALID = [
        {"alias": "Test"},
        {"alias": "PROD"},
        {"alias": "other"},
    ]