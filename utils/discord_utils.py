import re

async def mention_to_username(mention_str, bot):
    user_id_match = re.search(r'<@(\d+)>', mention_str)
    
    if user_id_match:
        user_id = int(user_id_match.group(1))
        user = await bot.fetch_user(user_id)
        return "@" + user.display_name
    else:
        return None

async def replace_mentions_with_usernames(message, bot):
    mention_matches = re.finditer(r'<@!?(\d+)>', message)
    mention_ranges = [(m.start(), m.end()) for m in mention_matches]

    new_message_parts = []
    prev_end = 0
    for start, end in mention_ranges:
        new_message_parts.append(message[prev_end:start])
        user_id = int(message[start + 2:end - 1].lstrip('!'))
        user = await bot.fetch_user(user_id)
        new_message_parts.append("@" + user.display_name)
        prev_end = end

    new_message_parts.append(message[prev_end:])
    new_message = "".join(new_message_parts)

    return new_message

async def read_last_n_responses(num, message, bot):
    previous_messages = await get_history_messages(message, num)
    previous_messages_str = "\n".join(previous_messages)

    final_str = f"{previous_messages_str}\n{message.author.name}: {message.content}"
    final_str = await replace_mentions_with_usernames(final_str, bot)

    print(message.author.name)
    if "GentryBot" in message.author.name:
        final_str = "NoUsername:"
    
    print(final_str)
    return final_str

async def get_history_messages(message, num):
    previous_messages = [] 
    async for msg in message.channel.history(limit=num, before=message): 
        previous_messages.append(f"{msg.author.name}: {msg.content}")

    previous_messages.reverse() 
    return previous_messages
