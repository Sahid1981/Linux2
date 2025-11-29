
#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": "localhost",
    "user": "user",
    "password": os.getenv("chatpw"),
    "database": "mqtt_chat"
}

@app.route('/api/messages', methods=['GET'])
def get_messages():
    Limit = request.args.get('limit', 50, type=int)

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            '''
            SELECT id, nickname, message, client_id, created_at
            FROM messages
            ORDER BY created_at DESC
            LIMIT %s
            ''',
            (limit,)
        )
        messages = cursor.fetchall()

        for msg in messages:
            if msg.get('created_at'):
                msg['created_at'] = msg['created_at'].isoformat()

        cursor.close()
        conn.close()

        return jsonify(messages[::-1]), 200

    except mysql.connector.Error as err:
        return jsonify({"error": "database_error", "message": str(err)}), 500
    except Exception as e:
        return jsonify({"error": "server_error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
