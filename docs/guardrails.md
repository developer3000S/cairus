# Guardrails

Guardrails работают _параллельно_ с вашими агентами и позволяют выполнять проверки и валидации пользовательского ввода. Например, представьте, что у вас есть агент, который использует очень умную (а значит медленную и дорогую) модель для помощи клиентам. Вы не захотите, чтобы злоумышленники просили модель помочь им с домашним заданием по математике. Поэтому вы можете запустить guardrail на быстрой и дешёвой модели. Если guardrail обнаружит вредоносное использование, он сразу генерирует ошибку, что остановит выполнение дорогой модели и сэкономит вам время/деньги.

Существует два типа guardrails:

1. Input guardrails работают на начальном пользовательском вводе
2. Output guardrails работают на конечном выводе агента

## Input guardrails

Input guardrails выполняются в 3 этапа:

1. Сначала guardrail получает тот же ввод, что был передан агенту.
2. Затем выполняется функция guardrail, чтобы получить [`GuardrailFunctionOutput`][cai.sdk.agents.guardrail.GuardrailFunctionOutput], который затем оборачивается в [`InputGuardrailResult`][cai.sdk.agents.guardrail.InputGuardrailResult].
3. Наконец, проверяется, равно ли [`.tripwire_triggered`][cai.sdk.agents.guardrail.GuardrailFunctionOutput.tripwire_triggered] `true`. Если да, то выбрасывается исключение [`InputGuardrailTripwireTriggered`][cai.sdk.agents.exceptions.InputGuardrailTripwireTriggered], чтобы вы могли корректно обработать ситуацию.

!!! Note

    Input guardrails предназначены для работы с пользовательским вводом, поэтому guardrails агента выполняются только если агент является *первым* агентом. Возможно, вы спросите: почему свойство `guardrails` находится на агенте, а не передаётся в `Runner.run`? Потому что guardrails обычно связаны с конкретным агентом — для разных агентов нужны разные guardrails, поэтому удобно хранить их рядом с определением агента.

## Output guardrails

Output guardrails выполняются в 3 этапа:

1. Сначала guardrail получает тот же ввод, что был передан агенту.
2. Затем выполняется функция guardrail, чтобы получить [`GuardrailFunctionOutput`][cai.sdk.agents.guardrail.GuardrailFunctionOutput], который затем оборачивается в [`OutputGuardrailResult`][cai.sdk.agents.guardrail.OutputGuardrailResult].
3. Наконец, проверяется, равно ли [`.tripwire_triggered`][cai.sdk.agents.guardrail.GuardrailFunctionOutput.tripwire_triggered] `true`. Если да, то выбрасывается исключение [`OutputGuardrailTripwireTriggered`][cai.sdk.agents.exceptions.OutputGuardrailTripwireTriggered], чтобы вы могли корректно обработать ситуацию.

!!! Note

    Output guardrails предназначены для работы с итоговым выводом агента, поэтому guardrails агента выполняются только если агент является *последним* агентом. Как и в случае с input guardrails, это связано с тем, что guardrails обычно привязаны к конкретному агенту — для разных агентов нужны разные guardrails, поэтому удобно хранить их рядом с определением агента.

## Tripwires

Если ввод или вывод не проходят проверку guardrail, guardrail может сигнализировать об этом срабатыванием tripwire. Как только мы обнаруживаем сработавший guardrail, мы немедленно выбрасываем исключение `{Input,Output}GuardrailTripwireTriggered` и прекращаем выполнение агента.

## Реализация guardrail

Вам нужно предоставить функцию, которая принимает ввод и возвращает [`GuardrailFunctionOutput`][cai.sdk.agents.guardrail.GuardrailFunctionOutput]. В этом примере мы реализуем это, запуская агента внутри guardrail.

```python
from pydantic import BaseModel
from cai.sdk.agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)

class MaliciousRequestOutput(BaseModel):
    is_malicious_request: bool
    reasoning: str

guardrail_agent = Agent( # (1)!
    name="Security Guardrail Check",
    instructions="Check if the user is asking for help with hacking or bypassing security systems.",
    output_type=MaliciousRequestOutput,
)


@input_guardrail
async def security_guardrail( # (2)!
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, # (3)!
        tripwire_triggered=result.final_output.is_malicious_request,
    )


agent = Agent(  # (4)!
    name="Security assistant",
    instructions="You are a security assistant. You help users with legitimate security questions.",
    input_guardrails=[security_guardrail],
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me bypass the firewall on this corporate network?")
        print("Guardrail didn't trip - this is unexpected")

    except InputGuardrailTripwireTriggered:
        print("Security guardrail tripped")
```

1. Этот агент будет использоваться внутри guardrail-функции.
2. Это функция guardrail, которая получает ввод/контекст агента и возвращает результат.
3. Мы можем включить дополнительную информацию в результат guardrail.
4. Это сам агент, который определяет рабочий процесс.

Output guardrails работают аналогично.

```python
from pydantic import BaseModel
from cai.sdk.agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)
class MessageOutput(BaseModel): # (1)!
    response: str

class SecurityOutput(BaseModel): # (2)!
    reasoning: str
    contains_sensitive_data: bool

guardrail_agent = Agent(
    name="Data Leakage Guardrail Check",
    instructions="Check if the output includes any sensitive data like passwords or API keys.",
    output_type=SecurityOutput,
)

@output_guardrail
async def data_leakage_guardrail(  # (3)!
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.contains_sensitive_data,
    )

agent = Agent( # (4)!
    name="Security assistant",
    instructions="You are a security assistant. You help users with legitimate security questions.",
    output_guardrails=[data_leakage_guardrail],
    output_type=ResponseOutput,
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "What are the best practices for storing API keys in code?")
        print("Guardrail didn't trip - this is unexpected")

    except OutputGuardrailTripwireTriggered:
        print("Data leakage guardrail tripped")
```

1. Это тип вывода самого агента.
2. Это тип вывода guardrail.
3. Это функция guardrail, которая получает вывод агента и возвращает результат.
4. Это сам агент, который определяет рабочий процесс.
