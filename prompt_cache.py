from config import bot_name

with open('raw text/prompts/system_messages.txt', 'r', encoding='utf-8') as f1:
    classifier_system = f1.read().replace("<<BotName>>", bot_name)

with open('raw text/prompts/prompts.txt', 'r', encoding='utf-8') as f2:
    initial_prompt = f2.read().replace("<<BotName>>", bot_name)

with open('raw text/prompts/system_url_intent.txt', 'r', encoding='utf-8') as f3:
    system_url_intent = f3.read().replace("<<BotName>>", bot_name)

def get_url_viewer_system_prompt(message, web_contents):
    with open('raw text/prompts/system_url_viewer.txt', 'r', encoding='utf-8') as f4:
        system_url_intent = f4.read().split("[Prompt]")
        clean_strings = []
        if len(system_url_intent) >= 2:
            for i in system_url_intent:
                 clean_strings.append(i.replace("<<Message>>", message).replace("<<Webpage>>", web_contents))
            return clean_strings[0], clean_strings[1]
        else:
            print("No [Prompt] tag found.")