from aiogram.utils.keyboard import InlineKeyboardBuilder



def get_main_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text='🗒️Добавить заметку', callback_data='menu_add_not')
    builder.button(text='🗒️Мои заметки', callback_data='menu_show_notes')
    builder.button(text='💣Напоминание', callback_data='menu_notion')
    builder.button(text='⚒️Настройки', callback_data='menu_settings')


    builder.adjust(2, 1, 1)

    return builder.as_markup()


def back_to_main_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text='🔙Назад', callback_data='to_main_menu')

    return builder.as_markup()



