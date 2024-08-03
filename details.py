from src.details.app import app

HOST='0.0.0.0'
PORT=8000
DEBUG=True

def test_always_passes():
    assert True

def test_always_fails():
    assert False

app.run(host=HOST, port=PORT, debug=DEBUG)