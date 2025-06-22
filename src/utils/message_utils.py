"""
消息处理工具模块
"""
import os
from typing import List, Tuple
from astrbot.api.message_components import Plain, Image, BaseMessageComponent
import astrbot.core.platform.sources.discord.components as discord_components
from ..models.embed_theme import EmbedTheme

def detect_message_type(text: str) -> Tuple[str, int]:
    """
    检测消息类型并返回对应的主题颜色
    
    Args:
        text: 消息文本
        
    Returns:
        tuple: (消息类型标题前缀, 主题颜色)
    """
    text_lower = text.lower()
    
    # 错误相关关键词
    if any(word in text_lower for word in ['error', 'failed', 'failure', '错误', '失败', 'invalid']):
        return EmbedTheme.get_emoji(EmbedTheme.error), EmbedTheme.error
        
    # 警告相关关键词
    if any(word in text_lower for word in ['warning', 'caution', 'warn', '警告', '注意']):
        return EmbedTheme.get_emoji(EmbedTheme.warning), EmbedTheme.warning
        
    # 成功相关关键词
    if any(word in text_lower for word in ['success', 'succeeded', 'done', '成功', '完成']):
        return EmbedTheme.get_emoji(EmbedTheme.success), EmbedTheme.success
        
    # 帮助或信息相关关键词
    if any(word in text_lower for word in ['help', 'info', 'information', '帮助', '信息']):
        return EmbedTheme.get_emoji(EmbedTheme.info), EmbedTheme.info
        
    # 默认使用primary主题
    return EmbedTheme.get_emoji(EmbedTheme.primary), EmbedTheme.primary

def extract_components(chain: List[BaseMessageComponent]) -> Tuple[List[str], List[Image], List[BaseMessageComponent]]:
    """
    从消息链中分离文本、图片和其他组件
    
    Args:
        chain: 消息组件链
        
    Returns:
        tuple: (文本列表, 图片组件列表, 其他组件列表)
    """
    plain_texts, image_components, other_components = [], [], []
    for component in chain:
        if isinstance(component, Plain) and component.text and component.text.strip():
            plain_texts.append(component.text.strip())
        elif isinstance(component, Image):
            image_components.append(component)
        elif not isinstance(component, (discord_components.DiscordView, discord_components.DiscordButton)):
            other_components.append(component)
    return plain_texts, image_components, other_components

def generate_content(plain_texts: List[str]) -> Tuple[str, str]:
    """
    从文本列表智能生成标题和描述
    
    Args:
        plain_texts: 文本列表
        
    Returns:
        tuple: (标题, 描述)
    """
    full_text = "\n".join(plain_texts)
    lines = full_text.split('\n', 1)
    title, description = None, full_text
    
    if len(lines) > 1 and len(lines[0]) < 256 and lines[0].strip():
        title, description = lines[0].strip(), lines[1]
        
    if len(description) > 4096:
        description = description[:4093] + "..."
        
    return title, description

def extract_image_url(image_components: List[Image]) -> str:
    """
    从图片组件列表中提取第一个可用的URL
    
    Args:
        image_components: 图片组件列表
        
    Returns:
        str: 图片URL或None
    """
    for img in image_components:
        if hasattr(img, 'file') and isinstance(img.file, str):
            if img.file.startswith('http'):
                return img.file
            elif img.file.startswith('file:///'):
                file_path = img.file.replace('file:///', '')
                if os.path.exists(file_path):
                    return f"attachment://{os.path.basename(file_path)}"
            elif os.path.exists(img.file):
                return f"attachment://{os.path.basename(img.file)}"
    return None 