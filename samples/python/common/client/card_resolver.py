import json
import logging

import httpx

from samples.python.common.types import (
    A2AClientJSONError,
    AgentCard,
)


class A2ACardResolver:
    def __init__(self, base_url, agent_card_path='/.well-known/agent.json'):
        self.base_url = base_url.rstrip('/')
        self.agent_card_path = agent_card_path.lstrip('/')
        self.combined_url = f'{self.base_url}/{self.agent_card_path}'

    def get_agent_card(self) -> AgentCard:
        with httpx.Client() as client:
            response = client.get(self.combined_url)
            response.raise_for_status()
            try:
                return AgentCard(**response.json())
            except json.JSONDecodeError as e:
                raise A2AClientJSONError(str(e)) from e
