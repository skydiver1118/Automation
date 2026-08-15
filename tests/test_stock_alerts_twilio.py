from urllib.parse import parse_qs

from src.strategy_lab.stock_alerts import send_email, send_twilio_sms


def test_send_twilio_sms_posts_expected_payload(monkeypatch) -> None:
    captured = {}

    class FakeResponse:
        status = 201

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["data"] = request.data.decode("utf-8")
        captured["auth"] = request.headers["Authorization"]
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "AC123")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "secret")
    monkeypatch.setenv("TWILIO_FROM_NUMBER", "+15550000001")
    monkeypatch.setenv("TWILIO_TO_NUMBER", "+15550000002")
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    send_twilio_sms({"notifications": {"twilio_sms": {"enabled": True}}}, "test alert")

    payload = parse_qs(captured["data"])
    assert captured["url"].endswith("/Accounts/AC123/Messages.json")
    assert payload["From"] == ["+15550000001"]
    assert payload["To"] == ["+15550000002"]
    assert payload["Body"] == ["test alert"]
    assert captured["auth"].startswith("Basic ")
    assert captured["timeout"] == 30


def test_send_email_uses_recipient_environment_override(monkeypatch) -> None:
    captured = {}

    class FakeSmtp:
        def __init__(self, host, port, timeout):
            captured["host"] = host
            captured["port"] = port
            captured["timeout"] = timeout

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def starttls(self, context):
            captured["starttls"] = context is not None

        def login(self, username, password):
            captured["username"] = username
            captured["password"] = password

        def send_message(self, message):
            captured["to"] = message["To"]
            captured["subject"] = message["Subject"]

    monkeypatch.setenv("ALERT_SMTP_USER", "sender@example.com")
    monkeypatch.setenv("ALERT_SMTP_PASSWORD", "secret")
    monkeypatch.setenv("ALERT_EMAIL_FROM", "sender@example.com")
    monkeypatch.setenv("ALERT_EMAIL_TO", "receiver@example.com")
    monkeypatch.setattr("smtplib.SMTP", FakeSmtp)

    send_email(
        {"notifications": {"email": {"enabled": True, "to": ["ignored@example.com"]}}},
        "subject",
        "body",
    )

    assert captured["host"] == "smtp.gmail.com"
    assert captured["port"] == 587
    assert captured["username"] == "sender@example.com"
    assert captured["password"] == "secret"
    assert captured["to"] == "receiver@example.com"
    assert captured["subject"] == "subject"
