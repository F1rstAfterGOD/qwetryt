from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Константы для позиций водяного знака
WATERMARK_POSITIONS = [
    [("↖️", "tl"), ("⬆️", "t"), ("↗️", "tr")],
    [("⬅️", "l"), ("⭕️", "c"), ("➡️", "r")],
    [("↙️", "bl"), ("⬇️", "b"), ("↘️", "br")]
]

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать", callback_data="start_new")]
    ])

def get_skip_watermark_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏭️ Пропустить водяной знак", callback_data="wm:skip")]
    ])

def get_watermark_settings_keyboard(position="c", size=100, alpha=100):
    keyboard = []
    
    # Добавляем кнопки позиций
    for row in WATERMARK_POSITIONS:
        keyboard_row = []
        for emoji, pos in row:
            text = f"✅{emoji}" if pos == position else emoji
            keyboard_row.append(InlineKeyboardButton(text=text, callback_data=f"wm:pos:{pos}"))
        keyboard.append(keyboard_row)
    
    # Параметры (циклические переключатели согласно ТЗ)
    keyboard.append([
        InlineKeyboardButton(text=f"Размер: {size}%", callback_data=f"wm:size:{size}"),
        InlineKeyboardButton(text=f"Прозрачность: {alpha}%", callback_data=f"wm:alpha:{alpha}")
    ])
    
    # Управление
    keyboard.append([
        InlineKeyboardButton(text="🔁 Сброс", callback_data="wm:reset"),
        InlineKeyboardButton(text="✅ Готово", callback_data="wm:done")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)