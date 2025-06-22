"""
Discord Embed 数据结构定义模块
"""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class EmbedData:
    """Embed 消息数据结构"""
    title: Optional[str] = None
    description: Optional[str] = None
    color: Optional[int] = None
    footer_text: Optional[str] = None
    timestamp: bool = True
    fields: List[Dict[str, Any]] = None
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    def __post_init__(self):
        """初始化后处理"""
        if self.fields is None:
            self.fields = []

    def add_field(self, name: str, value: str, inline: bool = False) -> None:
        """添加字段"""
        self.fields.append({
            "name": name,
            "value": value,
            "inline": inline
        })

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "title": self.title,
            "description": self.description,
            "color": self.color,
            "footer_text": self.footer_text,
            "timestamp": self.timestamp,
            "fields": self.fields,
            "image_url": self.image_url,
            "thumbnail_url": self.thumbnail_url
        } 