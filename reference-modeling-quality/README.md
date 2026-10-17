# 参考驱动三维建模

让 AI Agent 根据参考图、多视图或尺寸要求制作和修改可编辑的 Blender 模型，并检查形体、结构、导出文件和工程保存。

适用于道具、车辆与硬表面资产；有机对象采用对应的雕刻和拓扑流程。

## 自动安装（推荐）

在 Codex 中复制并发送：

```text
使用 $skill-installer 安装这个技能：
https://github.com/FoolishDeveloper5360/agent-skill-workbench/tree/main/reference-modeling-quality
```

安装器会下载完整技能，无需手动选择路径。安装完成后，在下一轮对话中使用；若技能未出现，再重启 Codex。

## 使用方法

直接附上参考图并发送，不需要先整理图片目录：

```text
使用 $reference-modeling-quality，按附件参考图制作可编辑的 Blender 模型。
请先检查现有工具是否可用，将工程和检查点保存在当前项目内，完成质量检查后交付。
```

有具体要求时，可以这样补充：

```text
制作一个用于网页展示的静态道具，总高度 0.4 米，其他尺寸按参考比例推断。
不需要绑定或动画。交付可编辑 .blend、GLB、关键视角对照图和简洁检查记录。
```

以上为调用示例。将尺寸和用途替换为自己的需求，也可以直接给出已有图片的路径。

## 会得到什么

- 可编辑的 Blender 源工程，以及需要的纹理等依赖。
- 按任务要求导出的模型文件；交付 GLB 时，独立回读检查实际导出结果。
- 关键视角对照图、检查结果与已知偏差说明。
- 对应版本的保存目录与文件校验清单。

环境检查、文件保存和校验由 Agent 执行。成果保存在已授权的项目目录内，无需额外云盘；本地保存不等于异地备份。

## 使用条件

- Agent 能查看参考图、读写项目文件，并通过本地脚本或已配置工具操作 Blender。
- 已有可用的 Blender；技能本身不安装软件，也不包含 Blender 连接器。
- 清单校验需要 Python 3.8 或更新版本，仅使用标准库，由 Agent 调用。

缺少必要工具时，Agent 会说明需要补充什么。其他 Agent 与操作系统的完整建模流程尚未逐一验证。

<details>
<summary>备选：手动安装</summary>

将完整的 `reference-modeling-quality/` 文件夹放到目标项目的 `.agents/skills/` 下，保留内部结构。也可放入个人技能目录 `~/.agents/skills/`，避免同名重复安装。

安装与调用方式参考 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)。其他宿主工具请按各自说明配置。

</details>

<details>
<summary>进阶：执行规则与文件校验</summary>

查看 [技能指令](SKILL.md)、[质量检查要求](references/quality-gates.md) 与 [保存及清单工具说明](references/checkpoint-delivery.md)。正常使用无需手动运行命令。

清单校验只能证明登记文件内容一致，不证明模型正确或文件会永久保留。

</details>

## 作者与许可

[FoolishDeveloper5360](https://github.com/FoolishDeveloper5360) · [MIT License](LICENSE)
