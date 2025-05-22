import requests


def send_conversion_request(password, hidden):
    url = 'http://127.0.0.1:5000/passnerd'
    data = {'password': password, 'hidden': hidden}

    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            result = response.json()
            print(f"Converted Password: {result['converted_password']}")
        else:
            print(f"Error: {response.json()}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    password_to_convert = '<sDW5_s9xG6<D0'
    hidden = False

    send_conversion_request(password_to_convert, hidden)
