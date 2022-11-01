def test_index(app, client):
    res = client.get("/")
    assert res.status_code == 200


def test_trade_add(app, client):
    res = client.get("/trade/add")
    assert res.status_code == 200


def test_trade_import(app, client):
    res = client.get("/trade/import")
    assert res.status_code == 200


def test_risk(app, client):
    res = client.get("/risk")
    assert res.status_code == 200
