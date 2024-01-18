from aiogram import Bot, types


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(
            command='start',
            description='Запуск'
        ),
    ]

    await bot.set_my_commands(commands, types.BotCommandScopeDefault())
