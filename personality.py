with open('raw text/prompts/system_messages.txt', 'r', encoding='utf-8') as f1:
    classifier_system = f1.read()

with open('raw text/prompts/prompts.txt', 'r', encoding='utf-8') as f2:
    initial_prompt = f2.read()