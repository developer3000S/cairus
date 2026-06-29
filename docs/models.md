# Модели

SDK агентов поддерживает OpenAI-модели двумя способами:

-   **Рекомендуемый**: [`OpenAIResponsesModel`][cai.sdk.agents.models.openai_responses.OpenAIResponsesModel], который вызывает OpenAI API через новый [Responses API](https://platform.openai.com/docs/api-reference/responses).
-   [`OpenAIChatCompletionsModel`][cai.sdk.agents.models.openai_chatcompletions.OpenAIChatCompletionsModel], который вызывает OpenAI API через [Chat Completions API](https://platform.openai.com/docs/api-reference/chat).

## Смешивание и сочетание моделей

В одном рабочем процессе вы можете захотеть использовать разные модели для разных агентов. Например, можно взять меньшую, более быструю модель для триажа и большую, более мощную модель для сложных задач. При настройке [`Agent`][cai.sdk.agents.Agent] вы можете выбрать конкретную модель одним из способов:

1. Передать имя модели OpenAI.
2. Передать любое имя модели + [`ModelProvider`][cai.sdk.agents.models.interface.ModelProvider], который может сопоставить это имя с экземпляром Model.
3. Напрямую передать реализацию [`Model`][cai.sdk.agents.models.interface.Model].

!!!note

    Хотя наш SDK поддерживает формы [`OpenAIResponsesModel`][cai.sdk.agents.models.openai_responses.OpenAIResponsesModel] и [`OpenAIChatCompletionsModel`][cai.sdk.agents.models.openai_chatcompletions.OpenAIChatCompletionsModel], мы рекомендуем использовать один тип модели для каждого рабочего процесса, потому что эти формы поддерживают разные наборы функций и инструментов. Если вашему рабочему процессу требуется смешивание форм моделей, убедитесь, что все используемые функции поддерживаются обоими.

```python
from cai.sdk.agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
    model="o3-mini", # (1)!
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
    model=OpenAIChatCompletionsModel( # (2)!
        model="gpt-4o",
        openai_client=AsyncOpenAI()
    ),
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
    model="gpt-3.5-turbo",
)

async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)
```

1.  Указывает имя модели OpenAI напрямую.
2.  Передает реализацию [`Model`][cai.sdk.agents.models.interface.Model].

## Использование других провайдеров LLM

Вы можете использовать других провайдеров LLM тремя способами (примеры [здесь](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers/)):

1. [`set_default_openai_client`][cai.sdk.agents.set_default_openai_client] полезен, если вы хотите глобально использовать экземпляр `AsyncOpenAI` в качестве клиента LLM. Это работает, когда провайдер LLM имеет совместимый с OpenAI API endpoint, и вы можете задать `base_url` и `api_key`. Смотрите настраиваемый пример в [examples/model_providers/custom_example_global.py](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers/custom_example_global.py).
2. [`ModelProvider`][cai.sdk.agents.models.interface.ModelProvider] работает на уровне `Runner.run`. Это позволяет указать «использовать пользовательский провайдер моделей для всех агентов в этом запуске». Смотрите настраиваемый пример в [examples/model_providers/custom_example_provider.py](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers/custom_example_provider.py).
3. [`Agent.model`][cai.sdk.agents.agent.Agent.model] позволяет указать модель на конкретном экземпляре агента. Это позволяет смешивать и сочетать разных провайдеров для разных агентов. Смотрите пример в [examples/model_providers/custom_example_agent.py](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers/custom_example_agent.py).

Если у вас нет ключа API от `platform.openai.com`, мы рекомендуем отключить трассировку с помощью `set_tracing_disabled()` или настроить [другой процессор трассировки](tracing.md).

!!! note

    В этих примерах мы используем API/модель Chat Completions, потому что большинство других провайдеров LLM пока не поддерживают Responses API. Если ваш провайдер поддерживает Responses, мы рекомендуем использовать его.

## Распространённые проблемы при использовании других провайдеров LLM

### Ошибка клиента трассировки 401

Если вы получаете ошибки, связанные с трассировкой, это означает, что трассы выгружаются на серверы OpenAI, а у вас нет ключа OpenAI API. У вас есть три варианта решения:

1. Отключить трассировку полностью: [`set_tracing_disabled(True)`][cai.sdk.agents.set_tracing_disabled].
2. Установить ключ OpenAI для трассировки: [`set_tracing_export_api_key(...)`][cai.sdk.agents.set_tracing_export_api_key]. Этот ключ API будет использоваться только для загрузки трасс, и он должен быть из [platform.openai.com](https://platform.openai.com/).
3. Использовать процессор трассировки, не зависящий от OpenAI. Смотрите [документацию по трассировке](tracing.md#custom-tracing-processors).

### Поддержка Responses API

SDK использует Responses API по умолчанию, но большинство других провайдеров LLM ещё не поддерживают его. В результате вы можете получить 404 или похожую ошибку. Чтобы решить проблему, у вас есть два варианта:

1. Вызвать [`set_default_openai_api("chat_completions")`][cai.sdk.agents.set_default_openai_api]. Это работает, если вы задаёте `OPENAI_API_KEY` и `OPENAI_BASE_URL` через переменные окружения.
2. Использовать [`OpenAIChatCompletionsModel`][cai.sdk.agents.models.openai_chatcompletions.OpenAIChatCompletionsModel]. Примеры есть [здесь](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers/).

### Поддержка структурированных выводов

Некоторые провайдеры моделей не поддерживают [структурированные выводы](https://platform.openai.com/docs/guides/structured-outputs). Это иногда приводит к ошибке вида:

```
BadRequestError: Error code: 400 - {'error': {'message': "'response_format.type' : value is not one of the allowed values ['text','json_object']", 'type': 'invalid_request_error'}}
```

Это ограничение некоторых провайдеров — они поддерживают JSON-вывод, но не позволяют задавать `json_schema` для вывода. Мы работаем над исправлением этой проблемы, но рекомендуем полагаться на провайдеров, которые поддерживают JSON-схему, иначе ваше приложение может часто ломаться из-за некорректного JSON.
