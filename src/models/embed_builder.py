"""
Discord Embed 构建器模块
"""
from typing import Union, Dict, Any
from .embed_theme import EmbedTheme
from .embed_data import EmbedData

class EmbedBuilder:
    """Embed 消息构建器"""
    
    THEME = EmbedTheme

    @classmethod
    def create(cls, data: Union[Dict[str, Any], EmbedData]) -> EmbedData:
        """
        创建 Embed 数据对象
        
        Args:
            data: 字典或 EmbedData 对象
            
        Returns:
            EmbedData: Embed 数据对象
        """
        if isinstance(data, EmbedData):
            return data
            
        if isinstance(data, dict):
            return EmbedData(**data)
            
        raise ValueError("data must be dict or EmbedData")

    @classmethod
    def info(cls, title: str = None, description: str = None, **kwargs) -> EmbedData:
        """创建信息类型的 Embed"""
        return cls.create({
            "title": title,
            "description": description,
            "color": cls.THEME.info,
            **kwargs
        })

    @classmethod
    def success(cls, title: str = None, description: str = None, **kwargs) -> EmbedData:
        """创建成功类型的 Embed"""
        return cls.create({
            "title": title,
            "description": description,
            "color": cls.THEME.success,
            **kwargs
        })

    @classmethod
    def warning(cls, title: str = None, description: str = None, **kwargs) -> EmbedData:
        """创建警告类型的 Embed"""
        return cls.create({
            "title": title,
            "description": description,
            "color": cls.THEME.warning,
            **kwargs
        })

    @classmethod
    def error(cls, title: str = None, description: str = None, **kwargs) -> EmbedData:
        """创建错误类型的 Embed"""
        return cls.create({
            "title": title,
            "description": description,
            "color": cls.THEME.error,
            **kwargs
        }) 