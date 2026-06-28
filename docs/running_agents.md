# Запуск агентов

Агентов можно запускать через класс [`Runner`][cai.sdk.agents.run.Runner]. Есть 3 варианта:

1. [`Runner.run()`][cai.sdk.agents.run.Runner.run] — асинхронный метод, возвращает [`RunResult`][cai.sdk.agents.result.RunResult].
2. [`Runner.run_sync()`][cai.sdk.agents.run.Runner.run_sync] — синхронный метод, который вызывает `.run()` под капотом.
3. [`Runner.run_streamed()`][cai.sdk.agents.run.Runner.run_streamed] — асинхронный метод, возвращает [`RunResultStreaming`][cai.sdk.agents.result.RunResultStreaming]. Он выполняет LLM в потоковом режиме и передаёт события по мере их поступления.

```python
from cai.sdk.agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")

    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)
    # Code within the code,
    # Functions calling themselves,
    # Infinite loop's dance.
```

Подробнее см. в [руководстве по результатам](results.md).

## Цикл агента

При вызове метода run в `Runner` вы передаёте стартового агента и ввод. Ввод может быть строкой (рассматривается как сообщение от пользователя) или списком элементов ввода, соответствующих элементам OpenAI Responses API.

Runner выполняет цикл:

1. Мы вызываем LLM для текущего агента с текущим вводом.
2. LLM генерирует вывод.
    1. Если LLM возвращает `final_output`, цикл завершается и мы возвращаем результат.
    2. Если LLM выполняет handoff, мы обновляем текущего агента и ввод и повторно запускаем цикл.
    3. Если LLM создаёт вызовы инструментов, мы выполняем эти вызовы, добавляем результаты и снова запускаем цикл.
3. Если мы превышаем переданное `max_turns`, выбрасывается исключение [`MaxTurnsExceeded`][cai.sdk.agents.exceptions.MaxTurnsExceeded].

!!! note

    Правило, по которому вывод LLM считается "финальным", таково: он выдаёт текстовый результат нужного типа, и при этом нет вызовов инструментов.

## Потоковая передача

Потоковая передача позволяет получать события по мере выполнения LLM. Когда поток завершится, [`RunResultStreaming`][cai.sdk.agents.result.RunResultStreaming] будет содержать полную информацию о запуске, включая все новые результаты. Вы можете вызвать `.stream_events()` для получения потоковых событий. Подробнее см. [руководство по streaming](streaming.md).

Параметр `run_config` позволяет настраивать глобальные параметры запуска агента:

-   [`model`][cai.sdk.agents.run.RunConfig.model]: позволяет задать глобальную модель LLM независимо от модели каждого агента.
-   [`model_provider`][cai.sdk.agents.run.RunConfig.model_provider]: провайдер моделей для поиска имён моделей, по умолчанию OpenAI.
-   [`model_settings`][cai.sdk.agents.run.RunConfig.model_settings]: переопределяет настройки, специфичные для агента. Например, глобальные `temperature` или `top_p`.
-   [`input_guardrails`][cai.sdk.agents.run.RunConfig.input_guardrails], [`output_guardrails`][cai.sdk.agents.run.RunConfig.output_guardrails]: список входных или выходных guardrail'ов, применяемых ко всем запускам.
-   [`handoff_input_filter`][cai.sdk.agents.run.RunConfig.handoff_input_filter]: глобальный фильтр входа для всех handoff'ов, если у handoff'а ещё нет собственного. Фильтр позволяет изменять вход, передаваемый новому агенту. Подробнее см. [`Handoff.input_filter`][cai.sdk.agents.handoffs.Handoff.input_filter].
-   [`tracing_disabled`][cai.sdk.agents.run.RunConfig.tracing_disabled]: позволяет отключить [trейсинг](tracing.md) для всего запуска.
-   [`trace_include_sensitive_data`][cai.sdk.agents.run.RunConfig.trace_include_sensitive_data]: настраивает, будут ли трассы содержать потенциально чувствительные данные, такие как входы/выходы LLM и вызовов инструментов.
-   [`workflow_name`][cai.sdk.agents.run.RunConfig.workflow_name], [`trace_id`][cai.sdk.agents.run.RunConfig.trace_id], [`group_id`][cai.sdk.agents.run.RunConfig.group_id]: задаёт имя рабочего процесса трассировки, идентификатор трассы и идентификатор группы для запуска. Рекомендуется задавать как минимум `workflow_name`. Идентификатор сессии — необязательное поле, которое позволяет связывать трассы между разными запусками.
-   [`trace_metadata`][cai.sdk.agents.run.RunConfig.trace_metadata]: метаданные для всех трасс.

## Разговоры / chat threads

Вызов любого метода run может привести к запуску одного или нескольких агентов (и, следовательно, одного или нескольких запросов к LLM), но это считается одним логическим ходом в чат-разговоре. Например:

1. Ход пользователя: пользователь вводит текст
2. Запуск Runner: первый агент вызывает LLM, выполняет инструменты, передаёт задачу второму агенту, второй агент выполняет дополнительные инструменты и затем формирует результат.

В конце запуска агента вы можете выбрать, что показать пользователю. Например, можно показать все новые элементы, сгенерированные агентами, или только финальный результат. Пользователь может задать уточняющий вопрос, и тогда можно снова вызвать метод run.

Вы можете использовать метод [`RunResultBase.to_input_list()`][cai.sdk.agents.result.RunResultBase.to_input_list], чтобы получить ввод для следующего хода.

```python
async def main():
    agent = Agent(name="Assistant", instructions="Reply very concisely.")

    with trace(workflow_name="Conversation", group_id=thread_id):
        # Первый ход
        result = await Runner.run(agent, "What is phishing?")
        print(result.final_output)
        # Ожидается: Тип кибератаки, при которой пользователей вводят в заблуждение, чтобы получить конфиденциальную информацию.
        
        # Второй ход
        new_input = result.to_input_list() + [{"role": "user", "content": "How can I protect myself from it?"}]
        result = await Runner.run(agent, new_input)
        print(result.final_output)
        # Ожидается: Используйте фильтры электронной почты, не переходите по подозрительным ссылкам и включите двухфакторную аутентификацию.
```

## Исключения

SDK выбрасывает исключения в определённых случаях. Полный список доступен в [`cai.sdk.agents.exceptions`][]. Краткий обзор:

-   [`AgentsException`][cai.sdk.agents.exceptions.AgentsException] — базовый класс для всех исключений.
-   [`MaxTurnsExceeded`][cai.sdk.agents.exceptions.MaxTurnsExceeded] — выбрасывается, когда запуск превышает переданное `max_turns`.
-   [`ModelBehaviorError`][cai.sdk.agents.exceptions.ModelBehaviorError] — выбрасывается, когда модель генерирует некорректный вывод, например malformed JSON или вызывает несуществующий инструмент.
-   [`UserError`][cai.sdk.agents.exceptions.UserError] — выбрасывается, когда вы (разработчик, использующий CAI) совершаете ошибку.
-   [`InputGuardrailTripwireTriggered`][cai.sdk.agents.exceptions.InputGuardrailTripwireTriggered], [`OutputGuardrailTripwireTriggered`][cai.sdk.agents.exceptions.OutputGuardrailTripwireTriggered] — выбрасываются, когда срабатывает [guardrail](guardrails.md).
