from aiogram import Bot, Dispatcher, types, Router
from aiogram.dispatcher.filters import ContentTypesFilter
from aiogram.types import ContentType
from datetime import datetime, timezone

from config import TOKEN, MESSAGE_SCHEMA

MEDIA_GROUPS = {}


# Вынести в мидлварь
def delete_media_group(media_groups: dict) -> None:
    now = datetime.now(tz=timezone.utc)

    return {
        key: media_groups[key] for key in media_groups
        if (now - media_groups[key]).total_seconds() <= 60
    }


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
    global MEDIA_GROUPS

    if "button" in MESSAGE_SCHEMA and MESSAGE_SCHEMA["button"]:
        keyboard = message_kb(MESSAGE_SCHEMA["button"])
    else:
        keyboard = None

    if (message.media_group_id is not None
            and message.media_group_id not in MEDIA_GROUPS):
        MEDIA_GROUPS[message.media_group_id] = message.date
        MEDIA_GROUPS = delete_media_group(MEDIA_GROUPS)
    elif (message.media_group_id is not None
            and message.media_group_id in MEDIA_GROUPS):
        return

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
