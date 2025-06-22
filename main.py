# -*- coding: utf-8 -*-
"""
Discord Embed 适配器插件
自动将发送至Discord的文本消息转换为精美的Embed格式。
"""
import sys
from typing import List, Optional

import discord

# =================================================================
#  插件标准导入
# =================================================================
from astrbot.api import logger, AstrBotConfig
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Star, register, Context
from astrbot.api.message_components import BaseMessageComponent
import astrbot.core.platform.sources.discord.components as discord_components

from .src.handlers.embed_handler import embed_handler

# =================================================================
#  DiscordEmbed 动态热修复
# =================================================================
def _apply_discord_embed_patch():
    """动态替换内存中有问题的 DiscordEmbed 组件，修复 ValueError。"""

    class PatchedDiscordEmbed(BaseMessageComponent):
        """兼容 Pydantic 的 DiscordEmbed 版本。"""
        type: str = "discord_embed"
        title: Optional[str] = None
        description: Optional[str] = None
        color: Optional[int] = None
        url: Optional[str] = None
        thumbnail: Optional[str] = None
        image: Optional[str] = None
        footer: Optional[str] = None
        fields: Optional[List[dict]] = None

        def __init__(
            self,
            title: str = None,
            description: str = None,
            color: int = None,
            url: str = None,
            thumbnail: str = None,
            image: str = None,
            footer: str = None,
            fields: List[dict] = None,
        ):
            super().__init__()
            self.title = title
            self.description = description
            self.color = color
            self.url = url
            self.thumbnail = thumbnail
            self.image = image
            self.footer = footer
            self.fields = fields or []

        def to_discord_embed(self) -> discord.Embed:
            """转换为Discord Embed对象"""
            embed = discord.Embed()
            if self.title:
                embed.title = self.title
            if self.description:
                embed.description = self.description
            if self.color is not None:
                embed.color = self.color
            if self.url:
                embed.url = self.url
            if self.thumbnail:
                embed.set_thumbnail(url=self.thumbnail)
            if self.image:
                embed.set_image(url=self.image)
            if self.footer:
                embed.set_footer(text=self.footer)
            for field in self.fields:
                embed.add_field(
                    name=field.get("name", ""),
                    value=field.get("value", ""),
                    inline=field.get("inline", False),
                )
            return embed

    try:
        # 直接在 sys.modules 中替换，确保所有使用者都获得新版本
        setattr(discord_components, 'DiscordEmbed', PatchedDiscordEmbed)
        logger.info("DiscordEmbedAdapter: 成功热修复 DiscordEmbed 组件。")
    except Exception as e:
        logger.error(f"DiscordEmbedAdapter: 热修复 DiscordEmbed 组件失败: {e}")

_apply_discord_embed_patch()


@register(
    name="DiscordEmbedAdapter",
    author="Gemini & Simon",
    desc="自动将发送至Discord的文本消息转换为精美的Embed格式。",
    version="4.2.0-final",
)
class DiscordEmbedAdapter(Star):
    """拦截发往Discord的消息，转换为Embed格式后自行发送，并终止原始事件。"""

    def __init__(self, context: Context, config: AstrBotConfig = None):
        super().__init__(context)
        self.config = config

    @filter.on_decorating_result(priority=-200)
    async def adapt_and_send_embed(self, event: AstrMessageEvent):
        """拦截并处理预备发送的消息。"""
        await embed_handler.handle_message(event) 