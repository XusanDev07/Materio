import json
import requests

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjQwOTYsInJvbGUiOm51bGwsImRhdGEiOnsiaWQiOjQwOTYsIm5hbWUiOiJLdXJib25vdmEgWmlsb2xhIiwiZW1haWwiOiJ4dXNhbnhhbGlsb3Y3MDdAZ21haWwuY29tIiwicm9sZSI6bnVsbCwiYXBpX3Rva2VuIjpudWxsLCJzdGF0dXMiOiJhY3RpdmUiLCJzbXNfYXBpX2xvZ2luIjoiZXNraXoyIiwic21zX2FwaV9wYXNzd29yZCI6ImUkJGsheiIsInV6X3ByaWNlIjo1MCwidWNlbGxfcHJpY2UiOjExNSwidGVzdF91Y2VsbF9wcmljZSI6bnVsbCwiYmFsYW5jZSI6NDk1MCwiaXNfdmlwIjowLCJob3N0Ijoic2VydmVyMSIsImNyZWF0ZWRfYXQiOiIyMDIzLTA1LTI4VDEzOjQ1OjQ0LjAwMDAwMFoiLCJ1cGRhdGVkX2F0IjoiMjAyMy0wNS0yOVQwNjozOTowNS4wMDAwMDBaIiwid2hpdGVsaXN0IjpudWxsLCJoYXNfcGVyZmVjdHVtIjowfSwiaWF0IjoxNjg1MzQ0OTAyLCJleHAiOjE2ODc5MzY5MDJ9.NYWjly1OPZ17hdtIVPj-KsP7rxoDiD1yh42K5nI6_jg"


def send_sms(otp, phone):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    msg = f"Maxfiy kod {otp}"

    data = json.dumps({
        "phone_number": str(phone),
        "message": msg,
        "from": 4546,
        "callback_url": "http://0000.uz/test.php"
    })

    headers = f"Bearer {token}"
    response = requests.post(url, data=data, headers=headers)
    return response
