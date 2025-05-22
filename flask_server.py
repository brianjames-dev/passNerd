from flask import Flask, request, jsonify

app = Flask(__name__)


def password_converter(password, hidden):
    password_label = password

    if hidden:
        # Password is currently hidden, show it
        hidden = False
        print(f"Password: {password}")
        print(f"Hidden: {hidden}")
        return {'converted_password': password_label, 'converted_hidden': hidden}
    else:
        # Password is currently shown, hide it
        hidden_password_label = "•" * len(password)
        hidden = True
        print(f"Password: {password}")
        print(f"Hidden: {hidden}")
        return {'converted_password': hidden_password_label, 'converted_hidden': hidden}


@app.route('/passnerd', methods=['POST'])
def convert_currency():
    try:
        data = request.get_json()

        # Extract data from the request
        password = data.get('password')
        hidden = data.get('hidden')

        # Perform the currency conversion
        converted_password = password_converter(password, hidden)

        return jsonify(converted_password)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    app.run(host=host, port=port, debug=True)
