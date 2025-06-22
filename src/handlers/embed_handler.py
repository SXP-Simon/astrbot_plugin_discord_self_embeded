"""
Embed 处理器模块
"""
import os
from typing import List, Optional
from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent
from astrbot.core.message.message_event_result import MessageChain, MessageEventResult
import astrbot.core.platform.sources.discord.components as discord_components

from ..models.embed_builder import EmbedBuilder
from ..models.embed_data import EmbedData
from ..utils.message_utils import (
    detect_message_type,
    extract_components,
    generate_content,
    extract_image_url
)
from .error_handler import error_handler

class EmbedHandler:
    """Embed 消息处理器"""
    
    async def handle_message(self, event: AstrMessageEvent) -> None:
        """
        处理消息事件
        
        Args:
            event: 消息事件
        """
        try:
            # 检查是否为Discord消息
            platform_name = event.get_platform_name()
            if platform_name != "discord":
                logger.debug(f"非 Discord 平台消息 (platform_name={platform_name})，跳过处理")
                return

            result = event.get_result()
            if not result or not result.chain:
                logger.debug("消息结果为空，跳过处理")
                return

            # 检查是否已经包含Discord Embed
            if any(isinstance(comp, discord_components.DiscordEmbed) for comp in result.chain):
                logger.debug("消息已包含 Discord Embed，跳过处理")
                return

            # 提取消息组件
            plain_texts, image_components, other_components = extract_components(result.chain)
            if not plain_texts or other_components:
                logger.debug("消息不包含文本或包含不支持的组件，跳过处理")
                return

            logger.info("DiscordEmbedAdapter: 截获消息，准备转换为Embed格式。")
            
            # 生成内容
            title, description = generate_content(plain_texts)
            image_url = extract_image_url(image_components)
            
            # 检测消息类型
            prefix, theme_color = detect_message_type(description or title or "")
            
            # 准备Embed数据
            embed_data = EmbedData(
                title=prefix + (title or "消息"),
                description=description,
                color=theme_color,
                timestamp=True
            )

            # 添加发送者信息
            try:
                sender_name = event.get_sender_name() or (
                    event.message_obj.sender.nickname 
                    if hasattr(event.message_obj, 'sender') 
                    else ''
                )
                if sender_name:
                    embed_data.footer_text = f"via {sender_name}"
            except Exception:
                pass

            # 创建Discord组件
            discord_embed = discord_components.DiscordEmbed(
                title=embed_data.title,
                description=embed_data.description,
                color=embed_data.color,
                footer=embed_data.footer_text
            )

            # 处理图片
            if image_url:
                if image_url.startswith("attachment://"):
                    # 本地文件需要特殊处理
                    file_path = next(
                        (img.file for img in image_components 
                         if os.path.basename(img.file) == image_url.replace("attachment://", "")),
                        None
                    )
                    if file_path and os.path.exists(file_path):
                        discord_embed.image = image_url
                        # 保留原始文件路径用于发送
                        image_components = [img for img in image_components if img.file == file_path]
                    else:
                        logger.warning(f"图片文件不存在: {file_path}")
                else:
                    # 网络图片直接设置URL
                    discord_embed.image = image_url
                    image_components = [comp for comp in image_components 
                                     if discord_components.img_comp_url(comp) != image_url]

            # 构建新的消息链
            new_chain = [discord_embed] + image_components
            
            try:
                await event.send(MessageChain(new_chain))
                event.set_result(MessageEventResult(chain=[]))
                logger.info("DiscordEmbedAdapter: 已作为Embed发送并清空原始事件结果。")
            except Exception as e:
                if "Invalid Form Body" in str(e):
                    logger.error(f"发送消息失败，可能是图片URL格式错误: {e}")
                    # 移除图片重试
                    discord_embed.image = None
                    await event.send(MessageChain([discord_embed]))
                    event.set_result(MessageEventResult(chain=[]))
                else:
                    await error_handler.handle_error(event, e)

        except Exception as e:
            await error_handler.handle_error(event, e)

embed_handler = EmbedHandler() 
