# Потоковая передача

Потоковая передача позволяет подписаться на обновления выполнения агента по мере его работы. Это полезно для отображения пользователю прогресса и частичных ответов.

Для потоковой передачи вызовите [`Runner.run_streamed()`][cai.sdk.agents.run.Runner.run_streamed], который вернёт [`RunResultStreaming`][cai.sdk.agents.result.RunResultStreaming]. Вызов `result.stream_events()` возвращает асинхронный поток объектов [`StreamEvent`][cai.sdk.agents.stream_events.StreamEvent], которые описаны ниже.

## Сырые события ответа

[`RawResponsesStreamEvent`][cai.sdk.agents.stream_events.RawResponsesStreamEvent] — это сырые события, передаваемые напрямую от LLM. Они соответствуют формату OpenAI Responses API, то есть каждое событие имеет тип (например, `response.created`, `response.output_text.delta` и т.д.) и данные. Эти события полезны, если вы хотите передавать пользователю текст по мере его генерации.

Например, этот код выведет текст, генерируемый LLM, токен за токеном.

```python
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from cai.sdk.agents import Agent, Runner

async def main():
    agent = Agent(
        name="Joker",
        instructions="CyberGuard.",
    )

    result = Runner.run_streamed(agent, input="Please tell me 5 cybersecurity tips.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
```

## События элементов запуска и изменения агента

[`RunItemStreamEvent`][cai.sdk.agents.stream_events.RunItemStreamEvent] — это события более высокого уровня. Они информируют, когда элемент полностью сгенерирован. Это позволяет отображать прогресс на уровне «сообщение готово», «инструмент выполнен» и т.п., вместо каждого токена. Аналогично, [`AgentUpdatedStreamEvent`][cai.sdk.agents.stream_events.AgentUpdatedStreamEvent] сообщает об изменении текущего агента (например, в случае handoff).

Например, этот код будет игнорировать сырые события и передавать пользователю только обновления.

```python
import asyncio
import random
from cai.sdk.agents import Agent, ItemHelpers, Runner, function_tool

@function_tool
def how_many_tips() -> int:
    return random.randint(1, 10)


async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_tips` tool, then tell that many cybersecurity tips.",
        tools=[how_many_tips],
    )

    result = Runner.run_streamed(
        agent,
        input="Hello",
    )
    print("=== Run starting ===")

    async for event in result.stream_events():
        # Мы игнорируем сырые события ответа
        if event.type == "raw_response_event":
            continue
        # Когда агент обновляется, выводим это
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # Когда элементы сгенерированы, выводим их
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Игнорируем другие типы событий

    print("=== Run complete ===")


if __name__ == "__main__":
    asyncio.run(main())
```
