import openai
from config import openai_token
from prompt_cache import initial_prompt, classifier_system

openai.api_key = openai_token

messages = list()
messages.append(initial_prompt)


def generate_response(p, last_username):
    messages.append(f"\n{p}\n GentryBot:")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="".join(messages),
        temperature=0.9,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0.5,
        stop=[f"{last_username}:", "GentryBot:", "Friend:"],
    )
    #print(messages[-1])
    messages.append(response.choices[0].text)
    return response.choices[0].text


def should_respond(message_string):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{classifier_system}"},
            {"role": "user", "content": f'Should the user "GentryBot" reply to this conversation?\n{message_string}'}
        ]
    )

    decision_text = completion['choices'][0]['message']['content']

    if "Yes" in decision_text or "yes" in decision_text:
        return True
    else:
        return False


def clear_memory():
    messages.clear()
    messages.append(initial_prompt)
