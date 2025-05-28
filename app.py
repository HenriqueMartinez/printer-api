# app.py

from flask import Flask, request, jsonify
from printer_service import process_print_commands

app = Flask(__name__)

@app.route('/print', methods=['POST'])
def handle_print():
    try:
        data = request.get_json()
        commands = data.get('commands')

        if not commands or not isinstance(commands, list):
            return jsonify({'error': 'Comandos inválidos ou ausentes'}), 400

        success, message = process_print_commands(commands)

        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 500

    except Exception as e:
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)