import csv

from flask import url_for
from flask_login import current_user

from app import db
from app.db.models import User, Transaction
def test_balance_calculation(client):
    """This tests is the balance calculated is correct"""
    with client:
        register_response = client.post("/register", data={
            "email": "testuser123@test.com",
            "password": "test123!test",
            "confirm": "test123!test"
        },
                                        follow_redirects=True)
        login_response = client.post("/login", data={
            "email": "testuser123@test.com",
            "password": "test123!test"
        },
                                     follow_redirects=True)

        assert login_response.status_code == 400

        form_data = {
            "file": open('testing_resources/transactions.csv', 'rb')
        }

        balance_before_transaction = User.query.get(current_user.id).balance
        # balance before any transaction
        assert balance_before_transaction == 0
        # This makes a call to upload the csv of transactions which will be processed.
        transaction_csv_upload_response = client.post(
            "/transactions/upload",
            data=form_data,
            follow_redirects=True)

        assert transaction_csv_upload_response.status_code == 200
        # balance after transaction
        balance_after_transaction = User.query.get(current_user.id).balance
        assert balance_after_transaction == 10601