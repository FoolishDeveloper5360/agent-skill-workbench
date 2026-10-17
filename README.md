# agent-skill-workbench

分享我自己编写、并在实际工作中使用的 AI Agent Skills。它们来自具体需求，不追求人人适用，希望能帮到遇到相似问题的你。

## 技能介绍

### [参考驱动三维建模](reference-modeling-quality/README.md)

根据参考图、多视图或尺寸要求制作可编辑的 Blender 模型，适用于道具、车辆和硬表面资产。让 Agent 完成形体对照、几何检查、GLB 导出回读，并保存可恢复的工程文件。

## 自动安装（推荐）

在 Codex 中复制并发送：

```text
使用 $skill-installer 安装这个技能：
https://github.com/FoolishDeveloper5360/agent-skill-workbench/tree/main/reference-modeling-quality
```

无需克隆仓库或手动放置文件。安装完成后，在下一轮对话中使用；若技能未出现，再重启 Codex。

## 使用方法

附上参考图，然后发送：

```text
使用 $reference-modeling-quality，按附件参考图制作可编辑的 Blender 模型。
请先检查现有工具是否可用，将工程和检查点保存在当前项目内，完成质量检查后交付。
```

有尺寸、用途或导出格式要求时一起说明。图片读取、环境检查、保存和文件校验由 Agent 处理。

需要可用的 Blender 和 Agent 操作它的工具；安装技能不会自动安装建模软件。详细依赖、更多示例及手动安装方式见 [技能使用说明](reference-modeling-quality/README.md)。

## 作者与许可

[FoolishDeveloper5360](https://github.com/FoolishDeveloper5360) · [MIT License](LICENSE)
