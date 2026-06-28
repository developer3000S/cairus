# Быстрый старт

## Создайте проект и виртуальное окружение

Это нужно сделать только один раз.

```bash
mkdir my_project
cd my_project
python -m venv .venv
```

### Активируйте виртуальное окружение

Делайте это при каждом новом запуске терминала.

```bash
source .venv/bin/activate
```

### Установите Agents SDK

```bash
pip install openai-agents # или `uv add openai-agents`, и т.д.
```

### Установите OpenAI API-ключ

Если у вас ещё нет ключа, выполните [инструкции](https://platform.openai.com/docs/quickstart#create-and-export-an-api-key) для создания OpenAI API-ключа.

```bash
export OPENAI_API_KEY=sk-...
```

## Создайте первого агента

Агенты определяются инструкциями, именем и опциональной конфигурацией (например, `model_config`).

```python
from cai.sdk.agents import Agent

agent = Agent(
    name="Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)
```

## Добавьте ещё несколько агентов

Дополнительных агентов можно определять таким же образом. `handoff_descriptions` дают дополнительный контекст для маршрутизации передачи задач.

```python
from cai.sdk.agents import Agent

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)
```

## Определите handoff'ы

Для каждого агента можно задать набор вариантов передачи, из которых агент будет выбирать, чтобы продвигаться к своей задаче.

```python
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent]
)
```

## Запустите оркестровку агентов

Проверим, что workflow работает, и triage-agent правильно направляет запросы между двумя специалистами.

```python
from cai.sdk.agents import Runner

async def main():
    result = await Runner.run(triage_agent, "What is the capital of France?")
    print(result.final_output)
```

## Добавьте guardrail

Вы можете определить собственные guardrail'ы для входных или выходных данных.

```python
from cai.sdk.agents import GuardrailFunctionOutput, Agent, Runner
from pydantic import BaseModel

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )
```

## Соберём всё вместе

Теперь соберём всё в один пример и запустим workflow с handoff'ами и входным guardrail'ом.

```python
from cai.sdk.agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print(result.final_output)

    result = await Runner.run(triage_agent, "what is life")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Просмотр трассировки

Чтобы посмотреть, что происходило во время запуска агента, перейдите в [Trace viewer в OpenAI Dashboard](https://platform.openai.com/traces).

## Следующие шаги

Узнайте, как строить более сложные agentic-потоки:

-   Изучите настройку [Agents](agents.md).
-   Изучите [запуск агентов](running_agents.md).
-   Изучите [tools](tools.md), [guardrails](guardrails.md) и [models](models.md).
