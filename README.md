# agent-skill-workbench

个人原创 AI Agent Skills 工作台。

这里分享我自己编写，并在日常工作中实际使用的 AI Agent Skills。每个技能都来自具体需求，也带着我的使用习惯；不追求人人都用得到，希望能为遇到相似问题的人提供参考。

当前为首次发布准备稿，采用 [MIT 许可证](LICENSE)。

GitHub 仓库：[FoolishDeveloper5360/agent-skill-workbench](https://github.com/FoolishDeveloper5360/agent-skill-workbench)。

## 技能目录

| 技能 | 用途 | 使用说明 |
| --- | --- | --- |
| [reference-modeling-quality](reference-modeling-quality/SKILL.md) | 根据参考图制作可编辑的 Blender 模型，检查视觉、几何、导出与可恢复交付 | [安装、依赖与示例](reference-modeling-quality/README.md) |

## 开始使用

1. 先阅读目标技能的使用说明，确认工具与环境条件。
2. 获取完整技能文件夹，保留 `SKILL.md`、`agents/`、`references/`、`scripts/` 的相对结构。
3. 按宿主工具的技能安装方式放置文件夹，再明确调用技能并提供任务素材。

本仓库提供技能指令和辅助文件。执行能力由使用它的 Agent 和已配置工具提供；不会随技能自动安装 Blender、连接服务或授予文件访问权限。

目前提供 Codex 的手动安装示例。其他支持 `SKILL.md` 的工具需按各自文档配置，尚未完成跨工具兼容性验证。

## 仓库约定

- 每个技能使用独立目录，入口为 `SKILL.md`。
- 面向使用者的依赖、调用方式和限制写在技能的 `README.md` 中。
- 辅助脚本的检查与实际任务效果分开记录；脚本通过不等于建模质量通过。
- 示例会标明是说明性示例还是实际案例，不使用未经验证的效果或兼容性宣传。

## 检查与维护

在仓库根目录运行清单脚本测试（仅需 Python 标准库）：

```sh
python -m unittest discover -s tests -v
```

查看 [变更记录](CHANGELOG.md)、[本次检查记录](docs/VALIDATION.md) 与 [发布前待办](docs/PUBLISHING.md)。

## 作者与许可

这些技能源于本仓库作者的原创制作与实际使用。采用 [MIT 许可证](LICENSE)，允许使用、修改、分发和商用，分发副本或实质性部分时须保留版权声明和许可文本。

作者：[FoolishDeveloper5360](https://github.com/FoolishDeveloper5360)。本仓库的许可证适用于仓库中的技能说明、文档和脚本。
