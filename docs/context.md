# Управление контекстом

Context (контекст) — перегруженный термин. Существуют два основных класса контекста, о которых вам может быть важно знать:

1. Контекст, доступный локально вашему коду: это данные и зависимости, которые вам могут понадобиться при запуске функций инструментов, во время callbacks вроде `on_handoff`, в lifecycle hooks и т.д.
2. Контекст, доступный LLM: это данные, которые LLM видит при генерировании ответа.

## Локальный контекст

Это представляется через класс [`RunContextWrapper`][cai.sdk.agents.run_context.RunContextWrapper] и свойство [`context`][cai.sdk.agents.run_context.RunContextWrapper.context] в нём. Как это работает:

1. Вы создаёте любой объект Python, который хотите. Распространённый паттерн — использовать dataclass или объект Pydantic.
2. Вы передаёте этот объект в различные методы run (например, `Runner.run(..., **context=whatever**))`).
3. Все ваши вызовы инструментов, lifecycle hooks и т.д. получат объект-оболочку `RunContextWrapper[T]`, где `T` представляет тип вашего объекта контекста, доступный через `wrapper.context`.

**Самое важное** помнить: каждый агент, функция инструмента, lifecycle и т.д. для данного запуска агента должны использовать одинаковый _тип_ контекста.

Вы можете использовать контекст для:

- Контекстных данных для вашего запуска (например, имя пользователя/uid или другая информация о пользователе)
- Зависимостей (например, объекты логгера, fetchers данных и т.д.)
- Вспомогательных функций

!!!danger "Примечание"

    Объект контекста **не** отправляется LLM. Это чисто локальный объект, из которого вы можете читать, писать и вызывать методы.

```python
import asyncio
from dataclasses import dataclass

from cai.sdk.agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class SecurityAlert:  # (1)!
    ip_address: str
    threat_id: int

@function_tool
async def fetch_threat_details(wrapper: RunContextWrapper[SecurityAlert]) -> str:  # (2)!
    return f"IP {wrapper.context.ip_address} is associated with a DDoS attack"

async def main():
    security_alert = SecurityAlert(ip_address="192.168.1.100", threat_id=507)

    agent = Agent[SecurityAlert](  # (3)!
        name="SecurityAnalyst",
        tools=[fetch_threat_details],
    )

    result = await Runner.run(  # (4)!
        starting_agent=agent,
        input="What type of threat is associated with this IP?",
        context=security_alert,
    )

    print(result.final_output)  # (5)!
    # IP 192.168.1.100 is associated with a DDoS attack.

if __name__ == "__main__":
    asyncio.run(main())
```

1. Это объект контекста. Мы использовали здесь dataclass, но вы можете использовать любой тип.
2. Это инструмент. Видно, что он принимает `RunContextWrapper[SecurityAlert]`. Реализация инструмента читает из контекста.
3. Мы помечаем агент с генерик `SecurityAlert`, чтобы type-checker мог перехватывать ошибки (например, если бы мы попытались передать инструмент, который требует другой тип контекста).
4. Контекст передаётся функции `run`.
5. Агент корректно вызывает инструмент и получает информацию об угрозе.

## Контекст агента/LLM

Когда вызывается LLM, **единственные** данные, которые она может видеть — это из истории беседы. Это означает, что если вы хотите сделать новые данные доступными LLM, вы должны сделать это способом, который делает их доступными в этой истории. Есть несколько способов сделать это:

1. Вы можете добавить это в `instructions` агента. Это также называется "system prompt" или "developer message". System prompts могут быть статическими строками, или динамическими функциями, которые получают контекст и выводят строку. Это распространённая тактика для информации, которая всегда полезна (например, имя пользователя или текущая дата).
2. Добавить это в `input` при вызове функций `Runner.run`. Это похоже на тактику `instructions`, но позволяет вам иметь сообщения, которые находятся ниже в [цепи командования](https://cdn.openai.com/spec/model-spec-2024-05-08.html#follow-the-chain-of-command).
3. Предоставить его через function tools. Это полезно для контекста _по требованию_ — LLM решает, когда ей нужны некоторые данные, и может вызвать инструмент для получения этих данных.
4. Использовать retrieval или web search. Это специальные инструменты, которые могут получать релевантные данные из файлов или баз данных (retrieval) или из веб-сети (web search). Это полезно для "anchoring" ответа в релевантные контекстные данные.
