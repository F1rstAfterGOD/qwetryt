"""
Утилиты для работы с водяными знаками согласно ТЗ
"""

def position_to_opus_format(position: str) -> str:
    """
    Конвертация позиции из формата кнопок в формат Opus API
    Согласно ТЗ: tl,t,tr,l,c,r,bl,b,br
    """
    position_map = {
        "tl": "tl",  # top-left
        "t": "t",    # top
        "tr": "tr",  # top-right
        "l": "l",    # left
        "c": "c",    # center
        "r": "r",    # right
        "bl": "bl",  # bottom-left
        "b": "b",    # bottom
        "br": "br"   # bottom-right
    }
    return position_map.get(position, "c")

def scale_to_opus_format(scale_percent: int) -> float:
    """
    Конвертация масштаба из процентов в формат Opus API
    Согласно ТЗ: 100/75/50/25 -> 1.0/0.75/0.5/0.25
    """
    return scale_percent / 100.0

def opacity_to_opus_format(opacity_percent: int) -> float:
    """
    Конвертация прозрачности из процентов в формат Opus API
    Согласно ТЗ: 100/80/60/40 -> 1/0.8/0.6/0.4
    """
    return opacity_percent / 100.0

def validate_watermark_params(position: str, scale: int, opacity: int) -> bool:
    """
    Валидация параметров водяного знака согласно ТЗ
    """
    valid_positions = ["tl", "t", "tr", "l", "c", "r", "bl", "b", "br"]
    valid_scales = [100, 75, 50, 25]
    valid_opacities = [100, 80, 60, 40]
    
    return (
        position in valid_positions and
        scale in valid_scales and
        opacity in valid_opacities
    )