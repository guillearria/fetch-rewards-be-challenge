from chalice.test import Client
from app import app


def test_post_transactions_missing_json():
    with Client(app) as client:
        response = client.http.post("/transactions")
        assert response.status_code == 400
        assert response.json_body == {
            "Code": "BadRequestError",
            "Message": "BadRequestError: Error Parsing JSON",
        }


def test_post_transactions_empty_list():
    with Client(app) as client:
        response = client.http.post(
            "/transactions", headers={"content-type": "application/json"}, body=[]
        )

        assert response.status_code == 200
        assert response.json_body == []


def test_post_transactions_wrong_json_type():
    with Client(app) as client:
        response = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body={
                "payer": "DANNON",
                "points": 300,
                "timestamp": "2020-10-31T10:00:00Z",
            },
        )

        assert response.status_code == 400
        assert response.json_body == {
            "Code": "BadRequestError",
            "Message": "BadRequestError: Request body must be of type list and include at least one transaction record",
        }


def test_post_transactions_invalid_record_keys1():
    with Client(app) as client:
        response = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=[
                {"user": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}
            ],
        )

        assert response.status_code == 400
        assert response.json_body == {
            "Code": "BadRequestError",
            "Message": "BadRequestError: Transaction records must contain payer, points, and timestamp keys",
        }


def test_post_transactions_invalid_record_keys2():
    with Client(app) as client:
        request_body = [
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
            {"payer": "DANNON", "points": 300},
        ]

        response = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=request_body,
        )

        assert response.status_code == 400
        assert response.json_body == {
            "Code": "BadRequestError",
            "Message": "BadRequestError: Transaction records must contain payer, points, and timestamp keys",
        }


def test_post_transactions_invalid_record_keys3():
    with Client(app) as client:
        request_body = [
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
            {"payer": "DANNON", "timestamp": "2020-10-31T10:00:00Z"},
        ]

        response = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=request_body,
        )

        assert response.status_code == 400
        assert response.json_body == {
            "Code": "BadRequestError",
            "Message": "BadRequestError: Transaction records must contain payer, points, and timestamp keys",
        }


def test_post_transactions_invalid_data_types1():
    with Client(app) as client:
        request_body = [
            {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
            {
                "payer": "MILLER COORS",
                "points": "10000",
                "timestamp": "2020-11-01T14:00:00Z",
            },
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
        ]

        response = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=request_body,
        )

        assert response.status_code == 400
        assert response.json_body == {
            "Code": "BadRequestError",
            "Message": "BadRequestError: Transaction records must contain valid data types: payer (string), points (integer), timestamp (string as YYYY-MM-DDT00:00:00Z)",
        }


def test_post_transactions_invalid_data_types2():
    with Client(app) as client:
        request_body = [
            {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
            {
                "payer": "MILLER COORS",
                "points": 10000,
                "timestamp": "2020-11-01T14:00:00Z",
            },
            {"payer": 26, "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
        ]

        response = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=request_body,
        )

        assert response.status_code == 400
        assert response.json_body == {
            "Code": "BadRequestError",
            "Message": "BadRequestError: Transaction records must contain valid data types: payer (string), points (integer), timestamp (string as YYYY-MM-DDT00:00:00Z)",
        }


def test_post_transactions_invalid_data_types3():
    with Client(app) as client:
        request_body = [
            {"payer": "DANNON", "points": -200, "timestamp": 20201101},
            {
                "payer": "MILLER COORS",
                "points": 10000,
                "timestamp": "2020-11-01T14:00:00Z",
            },
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
        ]

        response = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=request_body,
        )

        assert response.status_code == 400
        assert response.json_body == {
            "Code": "BadRequestError",
            "Message": "BadRequestError: Transaction records must contain valid data types: payer (string), points (integer), timestamp (string as YYYY-MM-DDT00:00:00Z)",
        }


def test_post_transactions_success_single():
    with Client(app) as client:
        request_body = [
            {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"}
        ]

        response = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=request_body,
        )

        assert response.status_code == 200
        assert response.json_body == [
            {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"}
        ]


def test_post_transactions_success_multiple():
    with Client(app) as client:
        request_body = [
            {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
            {
                "payer": "MILLER COORS",
                "points": 10000,
                "timestamp": "2020-11-01T14:00:00Z",
            },
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
        ]

        response = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=request_body,
        )

        assert response.status_code == 200
        assert response.json_body == [
            {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
            {
                "payer": "MILLER COORS",
                "points": 10000,
                "timestamp": "2020-11-01T14:00:00Z",
            },
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
        ]


def test_post_transactions_success_multiple_successive():
    with Client(app) as client:
        request_body1 = [
            {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
            {
                "payer": "MILLER COORS",
                "points": 10000,
                "timestamp": "2020-11-01T14:00:00Z",
            },
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
        ]

        request_body2 = [
            {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
            {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
        ]

        response1 = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=request_body1,
        )

        response2 = client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=request_body2,
        )

        assert response1.status_code == 200
        assert response1.json_body == [
            {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
            {
                "payer": "MILLER COORS",
                "points": 10000,
                "timestamp": "2020-11-01T14:00:00Z",
            },
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
        ]

        assert response2.status_code == 200
        assert response1.json_body == [
            {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
            {
                "payer": "MILLER COORS",
                "points": 10000,
                "timestamp": "2020-11-01T14:00:00Z",
            },
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
            {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
            {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
        ]


def test_get_payer_point_balances_no_transactions():
    with Client(app) as client:
        response = client.http.get("/points")

        assert response.status_code == 200
        assert response.json_body == {}


def test_get_payer_point_balances_with_transactions():
    with Client(app) as client:
        request_body = [
            {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
            {
                "payer": "MILLER COORS",
                "points": 10000,
                "timestamp": "2020-11-01T14:00:00Z",
            },
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
        ]

        client.http.post(
            "/transactions",
            headers={"content-type": "application/json"},
            body=request_body,
        )

        response = client.http.get("/points")

        assert response.status_code == 200
        assert response.json_body == {"DANNON": 100, "MILLER COORS": 10000}


# points

## get payer points balance

## spend points
# no json object
# non-numerical value
# points key missing
# more than one key exists
# more points than what is available
