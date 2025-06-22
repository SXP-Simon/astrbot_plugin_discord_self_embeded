"""
Discord Embed 主题定义模块
"""

class EmbedTheme:
    """Embed 主题颜色定义"""
    
    # 主要主题颜色
    primary = 0x1e88e5  # 蓝色
    info = 0x03c9d7    # 青色
    success = 0x00c853  # 绿色
    warning = 0xffc107  # 黄色
    error = 0xf44336   # 红色

    # 主题对应的表情符号
    EMOJI = {
        primary: "",      # 默认无表情
        info: "ℹ️",      # 信息
        success: "✅",    # 成功
        warning: "⚠️",   # 警告
        error: "❌"      # 错误
    }

    @classmethod
    def get_emoji(cls, theme_color: int) -> str:
        """获取主题对应的表情符号"""
        return cls.EMOJI.get(theme_color, "") 