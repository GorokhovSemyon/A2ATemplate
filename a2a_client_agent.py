import uuid

from samples.python.common.client import A2AClient, A2ACardResolver
from samples.python.common.types import TaskSendParams, Message, TextPart


class A2ATemplate:
    @staticmethod
    async def query_agent(agent_url, user_text):
        # Автоматически получить карточку агента
        card_resolver = A2ACardResolver(agent_url)
        agent_card = card_resolver.get_agent_card()
        print("Discovered Agent:", agent_card.name)
        # Создать клиента A2A с карточкой агента
        client = A2AClient(agent_card=agent_card)
        client.url = client.url + "/tasks/send"
        # Подготовить запрос Task (A2A type)
        payload = TaskSendParams(
            id=str(uuid.uuid4()),
            message=Message(role="user", parts=[TextPart(text=user_text)])
        )
        # Отправить запрос и ожидать ответ со статусом
        result_task = await client.send_task(payload.model_dump())
        # Выделить ответ агента из result_task
        if result_task.result.status.state.value == "completed":
            # Объект A2A Task может содержать дополнительные поля
            for msg in result_task.result.history:
                if msg.role == "agent":
                    # Выводим ответ агента
                    print("Agent's reply:", " ".join(part.text for part in msg.parts if hasattr(part, "text")))
