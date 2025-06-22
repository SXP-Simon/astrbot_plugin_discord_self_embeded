"""
Discord Embed 适配器插件包
"""
from .handlers.embed_handler import embed_handler
from .handlers.error_handler import error_handler
from .models.embed_builder import EmbedBuilder
from .models.embed_data import EmbedData
from .models.embed_theme import EmbedTheme

__all__ = [
    'embed_handler',
    'error_handler',
    'EmbedBuilder',
    'EmbedData',
    'EmbedTheme'
] 