# Настройка SDK

## API-ключи и клиенты

По умолчанию SDK ищет переменную окружения `OPENAI_API_KEY` для запросов к LLM и трассировки сразу при импорте. Если вы не можете установить эту переменную окружения до старта приложения, вы можете вызвать функцию `set_default_openai_key()` для задания ключа.

```python
from cai.sdk.agents import set_default_openai_key

set_default_openai_key("sk-...")
```

Также можно настроить собственный клиент OpenAI. По умолчанию SDK создаёт экземпляр `AsyncOpenAI`, используя API-ключ из переменной окружения или ключ, заданный выше. Вы можете заменить клиент, вызвав функцию `set_default_openai_client()`.

```python
from openai import AsyncOpenAI
from cai.sdk.agents import set_default_openai_client

custom_client = AsyncOpenAI(base_url="...", api_key="...")
set_default_openai_client(custom_client)
```

Наконец, можно выбрать, какой API OpenAI использовать. По умолчанию используется Responses API. Для переключения на Chat Completions используйте `set_default_openai_api()`.

```python
from cai.sdk.agents import set_default_openai_api

set_default_openai_api("chat_completions")
```

## Трассировка

Трассировка включена по умолчанию. Она использует OpenAI API-ключи, указанные выше (переменная окружения или заданный по умолчанию ключ). Вы можете задать отдельный API-ключ для экспорта трассировки с помощью функции `set_tracing_export_api_key`.

```python
from cai.sdk.agents import set_tracing_export_api_key

set_tracing_export_api_key("sk-...")
```

Трассировку также можно полностью отключить, вызвав `set_tracing_disabled()`.

```python
from cai.sdk.agents import set_tracing_disabled

set_tracing_disabled(True)
```

## Отладочные логи

SDK предоставляет два Python-логгера без настроенных обработчиков. По умолчанию предупреждения и ошибки направляются в `stdout`, а остальные логи подавляются.

Чтобы включить подробный вывод в `stdout`, используйте `enable_verbose_stdout_logging()`.

```python
from cai.sdk.agents import enable_verbose_stdout_logging

enable_verbose_stdout_logging()
```

В качестве альтернативы вы можете самостоятельно настроить логирование (обработчики, фильтры, форматтеры и т.д.). Больше информации в руководстве по [логированию Python](https://docs.python.org/3/howto/logging.html).

```python
import logging

logger =  logging.getLogger("openai.agents") # или openai.agents.tracing для логгера трассировки

# Чтобы видеть все логи
logger.setLevel(logging.DEBUG)
# Чтобы видеть info и выше
logger.setLevel(logging.INFO)
# Чтобы видеть warning и выше
logger.setLevel(logging.WARNING)
# и т.д.

# По умолчанию вывод будет в `stderr`
logger.addHandler(logging.StreamHandler())
```

### Чувствительные данные в логах

Некоторые логи могут содержать чувствительные данные (например, данные пользователей). Чтобы запретить логирование таких данных, установите соответствующие переменные окружения.

Чтобы отключить логирование входных и выходных данных моделей:

```bash
export OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1
```

Чтобы отключить логирование входных и выходных данных инструментов:

```bash
export OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1
```
