import re
from typing import Optional

def validate_youtube_url(url: str) -> Optional[str]:
    """Валидация YouTube URL и извлечение video_id согласно ТЗ"""
    if not url:
        return None
        
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def validate_watermark_file(file_size: int, content_type: str) -> bool:
    """Валидация файла водяного знака согласно ТЗ: PNG/JPG/WebP, до 5 МБ"""
    max_size = 5 * 1024 * 1024  # 5 MB
    allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp']
    
    if file_size is None or not content_type:
        return False
        
    return file_size <= max_size and content_type.lower() in allowed_types