from flask  import Flask

app = Flask(__name__)

@app.route('/api/v1', methods=['GET'])
def home():
    return "Сервер работает", 200
if __name__ == '__main__':
    app.run(debug=True)