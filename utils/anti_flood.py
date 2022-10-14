async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.reply("Подождите 1 секунду перед следующим запросом! 🙃")