import openai
from config import openai_token, bot_name
from prompt_cache import initial_prompt, classifier_system

openai.api_key = openai_token

messages = list()
messages.append(initial_prompt)


def generate_response(p, last_username):
    messages.append(f"\n{p}\n {bot_name}:")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="".join(messages),
        temperature=0.9,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0.5,
        stop=[f"{last_username}:", "{bot_name}:"],
    )
    messages.append(response.choices[0].text)
    return response.choices[0].text


def should_respond(message_string):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{classifier_system}"},
            {"role": "user", "content": f'Should the user "{bot_name}" reply to this conversation?\n{message_string}'}
        ]
    )

    decision_text = completion['choices'][0]['message']['content']

    if "Yes" in decision_text or "yes" in decision_text:
        return (True, decision_text)
    else:
        return (False, decision_text)
    
def get_general_chat_completion(system_prompt, user_prompt, temp):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=temp,
        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f'{user_prompt}'}
        ]
    )

    return completion['choices'][0]['message']['content']


def clear_memory():
    messages.clear()
    messages.append(initial_prompt)
