# ⚠️ Трассировка

!!!warning

    Функция трассировки отключена, поскольку мы переписываем её, чтобы она соответствовала стандартам OpenTelemetry. Новая реализация будет доступна в будущем.


SDK агентов включает встроенную трассировку, которая собирает полный журнал событий во время выполнения агента: генерации LLM, вызовы инструментов, handoff, guardrails и даже пользовательские события. С помощью [Traces dashboard](https://platform.openai.com/traces) вы можете отлаживать, визуализировать и мониторить рабочие процессы во время разработки и в продакшене.

!!!note

    Трассировка включена по умолчанию. Есть два способа отключить трассировку:

    1. Можно глобально отключить трассировку, установив переменную окружения `OPENAI_AGENTS_DISABLE_TRACING=1`
    2. Можно отключить трассировку для одного запуска, установив [`cai.sdk.agents.run.RunConfig.tracing_disabled`][] в `True`

***Для организаций, работающих в рамках политики Zero Data Retention (ZDR) с API OpenAI, трассировка недоступна.***

## Трейсы и спаны

-   **Трейсы** представляют собой одну сквозную операцию «workflow». Они состоят из спанов. Трейсы имеют следующие свойства:
    -   `workflow_name`: логическое имя рабочего процесса или приложения. Например «Генерация кода» или «Служба поддержки».
    -   `trace_id`: уникальный идентификатор трейса. Генерируется автоматически, если вы не передаёте его. Должен иметь формат `trace_<32_alphanumeric>`.
    -   `group_id`: опциональный идентификатор группы, чтобы связать несколько трейсов из одной беседы. Например, можно использовать идентификатор чата.
    -   `disabled`: если `True`, трейc не будет записан.
    -   `metadata`: опциональные метаданные для трейса.
-   **Спаны** представляют операции с началом и концом. У спанов есть:
    -   метки времени `started_at` и `ended_at`.
    -   `trace_id`, указывающий, к какому трейсу они принадлежат.
    -   `parent_id`, указывающий на родительский спан (если есть).
    -   `span_data`, содержащие информацию о спане. Например, `AgentSpanData` хранит данные агента, `GenerationSpanData` хранит данные генерации LLM и т.д.

## Трассировка по умолчанию

По умолчанию SDK трассирует следующие события:

-   Весь `Runner.{run, run_sync, run_streamed}()` оборачивается в `trace()`.
-   Каждый запуск агента оборачивается в `agent_span()`.
-   Генерации LLM оборачиваются в `generation_span()`.
-   Вызовы function tools оборачиваются в `function_span()`.
-   Guardrails оборачиваются в `guardrail_span()`.
-   Handoffs оборачиваются в `handoff_span()`.
-   Аудиовход (speech-to-text) оборачивается в `transcription_span()`.
-   Аудиовыход (text-to-speech) оборачивается в `speech_span()`.
-   Связанные аудиоспаны могут быть вложены в `speech_group_span()`.

По умолчанию трейс называется «Agent trace». Вы можете задать это имя через `trace`, либо настроить имя и другие свойства с помощью [`RunConfig`][cai.sdk.agents.run.RunConfig].

Кроме того, вы можете настроить [пользовательские процессоры трассировки](#custom-tracing-processors), чтобы отправлять трейсы в другие места назначения (в качестве замены или дополнительной цели).

## Трейсы более высокого уровня

Иногда вы хотите, чтобы несколько вызовов `run()` были частью одного трейса. Это можно сделать, обернув весь код в `trace()`.

```python
from cai.sdk.agents import Agent, Runner, trace

async def main():
    agent = Agent(name="Joke generator", instructions="Tell funny jokes.")

    with trace("Joke workflow"): # (1)!
        first_result = await Runner.run(agent, "Tell me a joke")
        second_result = await Runner.run(agent, f"Rate this joke: {first_result.final_output}")
        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")
```

1. Поскольку два вызова `Runner.run` обёрнуты в `with trace()`, отдельные запуски будут частью общего трейса, а не создадут два отдельных трейса.

## Создание трейсов

Вы можете использовать функцию [`trace()`][cai.sdk.agents.tracing.trace] для создания трейса. Трейсы нужно начинать и завершать. Есть два способа сделать это:

1. **Рекомендуется**: использовать трейc как менеджер контекста, т.е. `with trace(...) as my_trace`. Это автоматически запустит и завершит трейс в правильное время.
2. Также можно вручную вызвать [`trace.start()`][cai.sdk.agents.tracing.Trace.start] и [`trace.finish()`][cai.sdk.agents.tracing.Trace.finish].

Текущий трейс отслеживается через Python [`contextvar`](https://docs.python.org/3/library/contextvars.html). Это означает, что он автоматически работает с конкурентностью. Если вы вручную стартуете/завершаете трейс, вам нужно передать `mark_as_current` и `reset_current` в `start()`/`finish()`, чтобы обновить текущий трейс.

## Создание спанов

Вы можете использовать различные методы [`*_span()`][cai.sdk.agents.tracing.create] для создания спана. В общем случае вам не нужно создавать спаны вручную. Доступна функция [`custom_span()`][cai.sdk.agents.tracing.custom_span] для отслеживания пользовательской информации о спане.

Спаны автоматически становятся частью текущего трейса и вкладываются в ближайший текущий спан, который отслеживается через Python [`contextvar`](https://docs.python.org/3/library/contextvars.html).

## Конфиденциальные данные

Некоторые спаны могут содержать потенциально конфиденциальные данные.

`generation_span()` сохраняет входные и выходные данные генерации LLM, а `function_span()` сохраняет входные и выходные данные вызовов функций. Они могут содержать конфиденциальную информацию, поэтому вы можете отключить захват этих данных через [`RunConfig.trace_include_sensitive_data`][cai.sdk.agents.run.RunConfig.trace_include_sensitive_data].

Аналогично, аудиоспаны по умолчанию включают в себя PCM-данные в base64 для входного и выходного аудио. Вы можете отключить захват этих аудиоданных, настроив [`VoicePipelineConfig.trace_include_sensitive_audio_data`][cai.sdk.agents.voice.pipeline_config.VoicePipelineConfig.trace_include_sensitive_audio_data].

## Пользовательские процессоры трассировки

Высокоуровневая архитектура трассировки:

-   При инициализации создаётся глобальный [`TraceProvider`][cai.sdk.agents.tracing.setup.TraceProvider], который отвечает за создание трейсов.
-   Мы настраиваем `TraceProvider` с помощью [`BatchTraceProcessor`][cai.sdk.agents.tracing.processors.BatchTraceProcessor], который отправляет трейсы/спаны пакетами в [`BackendSpanExporter`][cai.sdk.agents.tracing.processors.BackendSpanExporter], экспортирующий спаны и трейсы в OpenAI backend.

Чтобы настроить эту дефолтную конфигурацию, отправлять трейсы в альтернативные или дополнительные бекенды или изменять поведение экспорта, у вас есть два варианта:

1. [`add_trace_processor()`][cai.sdk.agents.tracing.add_trace_processor] позволяет добавить **дополнительный** процессор трассировки, который будет получать трейсы и спаны по мере их готовности. Это позволяет вам выполнять собственную обработку помимо отправки трейсов на OpenAI backend.
2. [`set_trace_processors()`][cai.sdk.agents.tracing.set_trace_processors] позволяет **заменить** стандартные процессоры своими собственными. Это значит, что трейсы не будут отправляться на OpenAI backend, если вы не включите `TracingProcessor`, который это делает.

## Список внешних процессоров трассировки

-   [Weights & Biases](https://weave-docs.wandb.ai/guides/integrations/openai_agents)
-   [Arize-Phoenix](https://docs.arize.com/phoenix/tracing/integrations-tracing/openai-agents-sdk)
-   [MLflow (self-hosted/OSS](https://mlflow.org/docs/latest/tracing/integrations/openai-agent)
-   [MLflow (Databricks hosted](https://docs.databricks.com/aws/en/mlflow/mlflow-tracing#-automatic-tracing)
-   [Braintrust](https://braintrust.dev/docs/guides/traces/integrations#openai-agents-sdk)
-   [Pydantic Logfire](https://logfire.pydantic.dev/docs/integrations/llms/openai/#openai-agents)
-   [AgentOps](https://docs.agentops.ai/v1/integrations/agentssdk)
-   [Scorecard](https://docs.scorecard.io/docs/documentation/features/tracing#openai-agents-sdk-integration)
-   [Keywords AI](https://docs.keywordsai.co/integration/development-frameworks/openai-agent)
-   [LangSmith](https://docs.smith.langchain.com/observability/how_to_guides/trace_with_openai_agents_sdk)
-   [Maxim AI](https://www.getmaxim.ai/docs/observe/integrations/openai-agents-sdk)
-   [Comet Opik](https://www.comet.com/docs/opik/tracing/integrations/openai_agents)
-   [Langfuse](https://langfuse.com/docs/integrations/openaiagentssdk/openai-agents)
-   [Langtrace](https://docs.langtrace.ai/supported-integrations/llm-frameworks/openai-agents-sdk)
