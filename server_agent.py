from flask import Flask, request, jsonify

app = Flask(__name__)

# Определение Agent Card (метаданные об агенте)
# Особенно полезно в случаи нескольких агентов, чтобы они могли быть идентифицированы и взаимодействовать друг с другом
AGENT_CARD = {
    "name": "EchoAgent",
    "description": "A simple agent that echoes back user messages.",
    "url": "http://localhost:5000",
    "version": "1.0",
    "type": "agent",
    "skills": [
        {"name": "echo", "type": "message_processing", "id": "0"},
        {"name": "text_transformation", "type": "message_processing", "id": "1"},
        {"name": "response_generation", "type": "message_processing", "id": "2"}
    ],
    "capabilities": {
        "streaming": False,
        "pushNotifications": False
    }
}


# Получить карточку агента
@app.get("/.well-known/agent.json")
def get_agent_card():
    """Endpoint to provide this agent's metadata (Agent Card)."""
    return jsonify(AGENT_CARD)


# Обработка запроса в формате A2A
@app.post("/tasks/send")
def handle_task():
    """Endpoint for A2A clients to send a new task (with an initial user message)."""
    task_request = request.get_json()
    # Выделение ID задачи
    task_id = task_request.get("id")
    user_message = ""
    try:
        # Согласно A2A спецификации, сообщение должно быть в таком формате: task_request["params"]["message"]["parts"][0]["text"]
        user_message = task_request["params"]["message"]["parts"][0]["text"]
    except Exception as e:
        return jsonify({"error": "Invalid request format"}), 400

    # Так как это шаблон, сделаем эхо-ответ, можно заменить на необходимую логику
    agent_reply_text = f"Hello! You said: '{user_message}'"

    # Специфицируем ответ в формате A2A Task
    # Мы будем возвращать объект Task со state = 'completed' и ответ непосредственно
    response_task = {
        "id": task_id,
        "status": {"state": "completed"},
        "messages": [
            task_request["params"].get("message"),  # включаем исходное сообщение пользователя
            {
                "role": "agent",  # the agent's reply
                "parts": [{"text": agent_reply_text, "type": "text"}]  # агент ответит текстом TextPart
            }
        ]
    }
    return jsonify(response_task)


# Запуск сервера Flask app (A2A server), если запущен, можно кидать запросы на прописанный выше endpoint'ы
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)