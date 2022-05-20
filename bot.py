from aiogram import Bot, Dispatcher, types, Router

from config import TOKEN, MESSAGE_SCHEMA

router = Router()


def message_kb(button: dict) -> str:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=button["title"],
                                           url=button["url"])
            ]
        ]
    )


@router.message()
async def echo_handler(message: types.Message):
    if "button" in MESSAGE_SCHEMA and MESSAGE_SCHEMA["button"]:
        keyboard = message_kb(MESSAGE_SCHEMA["button"])
    else:
        keyboard = None
    text = MESSAGE_SCHEMA["message"].replace(
        "«Имя»",
        (
            f"<a href='tg://user?id={message.from_user.id}'>"
            f"@{message.from_user.username}</a>"
        )

    )

    await message.answer(text, reply_markup=keyboard,
                         disable_web_page_preview=True)


def main() -> None:
    bot = Bot(TOKEN, parse_mode="HTML")
    dispatcher = Dispatcher()
    dispatcher.include_router(router=router)
    dispatcher.run_polling(bot)


if __name__ == "__main__":
    main()
