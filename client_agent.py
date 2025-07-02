import requests
import uuid


# 1. Проверка наличия агента, через получения его Agent Card
AGENT_BASE_URL = "http://localhost:5000"
agent_card_url = f"{AGENT_BASE_URL}/.well-known/agent.json"
response = requests.get(agent_card_url)
if response.status_code != 200:
    raise RuntimeError(f"Failed to get agent card: {response.status_code}")
agent_card = response.json()
print("Discovered Agent:", agent_card["name"], "-", agent_card.get("description", ""))

# 2. Подготовка запроса в формате A2A полностью прописанное, без шаблонов из A2A репозитория
task_id = str(uuid.uuid4())  # generate a random unique task ID
user_text = "What is the meaning of life?"
task_payload = {
    "id": task_id,
    "params": {
        "message": {
            "role": "user",
            "parts": [
                {"text": user_text, "type": "text"}
        ]
        }
    }
}
print(f"Sending task {task_id} to agent with message: '{user_text}'")

# 3. Отправка запроса на выполнение задания в A2A server tasks/send endpoint
tasks_send_url = f"{AGENT_BASE_URL}/tasks/send"
result = requests.post(tasks_send_url, json=task_payload)
if result.status_code != 200:
    raise RuntimeError(f"Task request failed: {result.status_code}, {result.text}")
task_response = result.json()

# 4. Обработка ответа от A2A server
# Ответ содержит статус выполнения задания и список сообщений (если есть)
if task_response.get("status", {}).get("state") == "completed":
    # Последнее сообщение в списке должно быть ответом агентаT (с момента включения агентом истории в сообщениях).
    messages = task_response.get("messages", [])
    if messages:
        agent_message = messages[-1]
        agent_reply_text = ""
        # Выделение текста из сообщения агента
        for part in agent_message.get("parts", []):
            if "text" in part:
                agent_reply_text += part["text"]
        print("Agent's reply:", agent_reply_text)
    else:
        print("No messages in response!")
else:
    print("Task did not complete. Status:", task_response.get("status"))