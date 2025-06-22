"""
错误处理器模块
"""
from typing import Optional
from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent
from astrbot.core.message.message_event_result import MessageChain
import astrbot.core.platform.sources.discord.components as discord_components
from ..models.embed_builder import EmbedBuilder

class ErrorHandler:
    """错误处理器"""
    
    async def handle_error(self, event: AstrMessageEvent, error: Exception) -> None:
        """
        处理错误并发送错误消息
        
        Args:
            event: 消息事件
            error: 异常对象
        """
        error_msg = self._format_error_message(error)
        logger.error(f"DiscordEmbedAdapter: {error_msg}")
        
        try:
            # 创建错误Embed
            embed_data = EmbedBuilder.error(
                title="❌ 错误",
                description=error_msg
            )
            
            # 创建Discord组件
            discord_embed = discord_components.DiscordEmbed(
                title=embed_data.title,
                description=embed_data.description,
                color=embed_data.color,
                footer="via Error Handler"
            )
            
            # 发送错误消息
            await event.send(MessageChain([discord_embed]))
            
        except Exception as e:
            logger.error(f"DiscordEmbedAdapter: 发送错误消息时发生异常: {e}")
            # 如果发送错误消息失败，尝试发送普通文本
            await event.send(MessageChain([f"❌ 错误: {error_msg}"]))
    
    def _format_error_message(self, error: Exception) -> str:
        """
        格式化错误消息
        
        Args:
            error: 异常对象
            
        Returns:
            str: 格式化后的错误消息
        """
        error_str = str(error)
        
        # 处理特定类型的错误
        if "User location is not supported" in error_str:
            return "当前地区不支持访问此API服务。请检查您的网络设置或使用VPN。"
        elif "Invalid Form Body" in error_str:
            return "消息格式无效。请检查消息内容是否符合Discord的要求。"
            
        return error_str

error_handler = ErrorHandler() 