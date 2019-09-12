from flask import Flask, jsonify, request
import logging


logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/br')
def index():
    logger.info('covfefe')
    return jsonify(request.json)


def main():
    app.run('0.0.0.0', 5000)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
