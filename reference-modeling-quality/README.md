# 参考驱动三维建模

这个技能让 AI Agent 按参考图、多个视角或尺寸要求制作和修改 Blender 模型，并用可检查的证据交付。重点是形体、结构、可编辑性和可恢复保存。

适用于道具、车辆与硬表面资产；有机对象需要采用相应雕刻和拓扑流程。仅需一张效果图时通常不必使用这个技能。

## 推荐：自动安装后直接使用

在 Codex 中发送：

```text
使用 $skill-installer 安装这个技能：
https://github.com/FoolishDeveloper5360/agent-skill-workbench/tree/main/reference-modeling-quality
```

安装器会下载完整技能文件夹，无需手动选择路径。安装完成后，在下一轮对话附上参考图并发送：

```text
使用 $reference-modeling-quality，按附件参考图制作可编辑的 Blender 模型。
请先检查现有工具是否可用，将工程和检查点保存在当前项目内，完成质量检查后交付。
```

无需预先整理图片目录或自己运行清单命令。可直接附图；有尺寸、用途或格式要求时一并说明，其他由 Agent 根据任务处理。若技能没有出现，再重启 Codex。

### 环境由 Agent 先检查

- 一个能读取本地技能文件、查看参考图并执行建模操作的 AI Agent。
- 可使用的 Blender，以及 Agent 调用它的途径，例如已配置的本地脚本执行或建模工具连接。技能不包含 Blender 控制连接器，也不会自动安装软件。
- 任务所需的参考图片、尺寸约束和可写入的项目目录。
- 运行附带清单脚本需要 Python 3.8 或更新版本，仅使用标准库。它可独立运行，无需 Blender。
- 输出 GLB 时需要可用的导出与回读能力；具体 Blender 版本和工具连接由使用环境决定，尚未建立兼容版本矩阵。

## 备选：手动安装

安装器不可用或需要离线复制时，将整个 `reference-modeling-quality` 文件夹复制到目标项目的 `.agents/skills/` 下：

```text
你的项目/
└── .agents/
    └── skills/
        └── reference-modeling-quality/
            ├── SKILL.md
            ├── README.md
            ├── LICENSE
            ├── agents/openai.yaml
            ├── references/
            └── scripts/
```

个人范围的技能也可放到 `~/.agents/skills/`。避免重复安装同名技能。若安装后没有出现，重新启动 Codex，再确认是否能在技能列表中找到它。

以上路径与调用方式依据 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)（核对日期：2026-10-18）。其他宿主工具按各自的安装说明配置；`agents/openai.yaml` 是 OpenAI 界面元数据，不代表其他宿主已验证兼容。

## 调用示例

需要更精确地控制交付时，可参考下面的说明性任务（并非已经完成的建模案例）。直接附上有权使用的参考图；图片已在项目内时也可给出路径：

```text
使用 $reference-modeling-quality，按附件中的三张参考图
制作一个静态硬表面道具模型，用于网页展示。

约束：总高度 0.4 米，其他尺寸按参考比例推断，无需绑定或动画。
交付：可编辑 .blend、GLB、关键视角对照图和简洁 QA 记录。
项目内的 checkpoints/ 是我指定保留的本地交付位置，可以写入。
保存后重新打开源工程检查依赖，验证清单，再发对应版本的预览。
不需要上传外部服务。请标明无法从参考确定的部分。
```

将对象、尺寸和路径替换为自己的需求，并附上实际图片。没有可用的建模执行工具时，Agent 应报告缺少什么，而不能声称已完成模型。

预期过程：先确认参考与约束，制作粗模并对照，再修正结构和细节，导出后独立回读，保存并验证对应版本。

最终交付应能找到源工程、所需依赖、GLB（本任务要求时）、对照图、QA 记录和清单；粗模阶段尚不存在的产物应注明。QA 分别记录视觉和技术结果，以及未验证项。具体要求见 [技能入口](SKILL.md) 和 [保存说明](references/checkpoint-delivery.md)。

## 清单脚本（由 Agent 运行）

正常使用时，Agent 会完成清单生成与验证，用户无需手动执行。下面命令供排查或独立检查时参考。

在技能目录运行，路径含空格时加引号：

```sh
python scripts/checkpoint_manifest.py create "你的检查点目录"
python scripts/checkpoint_manifest.py verify "你的检查点目录"
```

`create` 创建或覆盖根目录的 `manifest.json`；`verify` 检查文件集合、大小和 SHA-256。成功退出码为 0，失败为非零。可用 `--manifest inventory.json` 更改清单文件名。

先停止修改目录内的工作文件，再生成清单；后续修改模型或新增预览需要创建新版本并更新清单。清单本身不纳入哈希，空目录也不登记。详见 [工具用法与局限](references/checkpoint-delivery.md)。

## 保存与验证边界

用户指定保留的本地项目目录可以作为交付位置：写入后重新打开源工程、检查依赖并验证清单，说明本地保存的范围即可。不强制使用云盘或额外账户；本地保存不代表已经具备异地备份。

如果运行环境只有随会话清理的临时目录，且没有可用的保留位置，应说明限制并请求必要的保存位置。脚本只能证明所登记文件的内容一致，不能证明 Blender 工程可打开、模型正确或文件将永久保留。

## 当前验证情况

作者已在实际工作中使用此技能。本仓库的可复核检查范围见 [检查记录](https://github.com/FoolishDeveloper5360/agent-skill-workbench/blob/main/docs/VALIDATION.md)；目前未附真实建模案例或效果对比，也未完成跨 Agent、跨系统的完整建模验收。

## 许可

作者：[FoolishDeveloper5360](https://github.com/FoolishDeveloper5360)。本技能及辅助文件采用 [MIT 许可证](LICENSE)。单独安装技能时也会携带许可文本。
