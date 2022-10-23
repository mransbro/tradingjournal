def test_addtrade(app, client):
    res = client.post(
        "trade/add",
        data={
            "date": "2022-10-26",
            "symbol": "MSFT",
            "num_of_shares": "11",
            "buy_price": "323.34",
            "notes": "",
        },
    )
    assert res.status_code == 200


def test_risk(app, client):
    res = client.post(
        "risk",
        data={
            "account_value": "23000",
            "max_risk": "1",
            "entry_price": "11",
            "stop": "9",
        },
    )
    assert res.status_code == 200
