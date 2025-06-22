# Discord Self Embeded Plugin for AstrBot

一个用于 AstrBot 的 Discord Embed 适配器插件，可以自动将发送至 Discord 的文本消息转换为精美的 Embed 格式。

## 功能特点

- 自动将普通文本消息转换为 Discord Embed 格式
- 支持自定义 Embed 主题和样式
- 支持标题、描述、颜色、URL、缩略图、图片等 Embed 元素
- 支持添加自定义字段（fields）
- 支持页脚文本
- 高优先级消息拦截，确保所有消息都能被正确转换

## 配置说明

插件会自动加载并运行，无需额外配置。默认会拦截所有发往 Discord 的消息并转换为 Embed 格式。

## 使用方法

插件安装后会自动工作，所有发往 Discord 的消息都会被自动转换为 Embed 格式。插件使用优化过的消息处理逻辑，确保消息格式美观统一。

### Embed 格式支持

- 标题（Title）
- 描述文本（Description）
- 自定义颜色（Color）
- 链接 URL（URL）
- 缩略图（Thumbnail）
- 大图（Image）
- 页脚文本（Footer）
- 自定义字段（Fields）：支持名称、内容和布局设置


## 问题反馈

如果你在使用过程中遇到任何问题，请通过以下方式反馈：

在 GitHub 仓库提交 Issue

## 许可证

本项目使用 [LICENSE](./LICENSE) 许可证。

## 插件信息

- 作者：SXP-Simon