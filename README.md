# PPTX Studio

项目仓库：[aaasdasdsacwa/pptx-studio](https://github.com/aaasdasdsacwa/pptx-studio)

一个面向多种用途的 PowerPoint 生成与编辑 Skill。根据主题、文档、数据、大纲、图片或已有演示稿，完成需求理解、内容组织、逐页规划、视觉设计、素材整合、可编辑文件制作与检查。也可以只修改指定页面或检查已有文件。

它采用 [Agent Skills](https://agentskills.io/specification) 的目录结构，由支持技能的 AI Agent 执行。它提供选择流程、专业操作指引和辅助检查脚本；不是脱离 Agent 和 PPTX 编辑工具的一键转换程序。

## 面向多种用途

按演示的目的、受众和材料组织内容：工作汇报、经营分析、产品介绍、销售提案、教学培训、学术答辩、技术交流、公开演讲、品牌展示、作品集、文化与个人叙事等，都可以采用不同的结构与视觉表达。它们是可组合的应用例子，不是只能从中选择的固定分类。

**用途、视觉风格和能力模块分别决定。** 教学不必套商业汇报结构，技术内容不必使用固定蓝色，摄影故事也不必填满图标。用户给出的品牌、版式和自由需求优先。

完整生成流程见 [generation.md](skills/pptx-studio/references/generation.md)，不同用途的内容处理见 [scenarios.md](skills/pptx-studio/references/scenarios.md)。这些指引覆盖制作方法，不代表每个行业或客户端已经完成效果验证。

## 使用体验

需求已经清楚时，直接执行：

> 使用 $pptx-studio，根据这份材料做一份面向管理层的 12 页汇报，说明问题、依据、备选方案和需要决定的事项，沿用附件品牌样式。

生成需求不必先选能力模块，也可以直接描述主题、受众和效果：

> 使用 $pptx-studio，给初中生制作一份有关火山的 20 分钟课件，结合示意图和练习，图片以提供的素材为主。

> 使用 $pptx-studio，将这些照片和采访文字整理成一份社区记忆分享，画面为主、暖色、少字，保留真实姓名和时间的原始写法。

Agent 根据上下文区分“完整生成 / 修改现有稿 / 只做检查”。生成时会组织内容、规划页面角色与整体风格，再按需使用相关能力。需要局部完善时，可以选择以下能力，也可以自由描述其他要求：

1. **内容与逻辑**：梳理主线、观点、证据与讲述顺序。
2. **版式与构图**：时间轴、流程、比较、层次、关系图及空间布局。
3. **图标增强**：增加或替换图标，核对图标与文字的语义、动作和状态。
4. **图片与配图**：相关照片、插图、真实截图、裁剪、标注与来源。
5. **数据图表**：数量图表和横向对照表，保留真实数值、单位和口径。
6. **视觉风格**：字体、色彩、间距、留白以及参考模板的延续。
7. **问题修复**：重叠、溢出、资源缺失、重复图层等具体故障。

这些是能力模块，不是七种固定的 PPT 类型。“图标 + 版式”只加载对应指引；“仅检查、不修改”会生成问题报告。用户已经指定需求时，不会强制重复选择菜单，也不会默认要求每页都加图标。

## 安装

获取仓库代码：

```sh
git clone https://github.com/aaasdasdsacwa/pptx-studio.git
cd pptx-studio
```

将完整的 [`skills/pptx-studio`](skills/pptx-studio) 文件夹安装到客户端支持的技能目录，保留 `SKILL.md`、`references/`、`scripts/` 等相对位置。安装与启用位置以所用客户端的说明为准；`agents/openai.yaml` 是可选的客户端显示元数据。

提交到技能合集时，只需加入这个完整文件夹。目录内的 [独立使用说明](skills/pptx-studio/README.md) 可直接随 Skill 分发，无需外层仓库。项目级开发测试仍保留在本仓库。

例如，使用支持项目级 `.agents/skills` 目录的客户端时，可以在自己的项目中执行：

```sh
mkdir -p .agents/skills
cp -R path/to/this-repo/skills/pptx-studio .agents/skills/
```

PowerShell 对应操作：

```powershell
New-Item -ItemType Directory -Force .agents/skills | Out-Null
Copy-Item -LiteralPath 'path/to/this-repo/skills/pptx-studio' -Destination '.agents/skills/pptx-studio' -Recurse
```

支持 `$名称` 调用方式的客户端可以输入 `$pptx-studio`；其他客户端按其技能调用方式启用。当前环境中创建仓库目录不等于已完成客户端安装。

## 运行条件与边界

- Agent 需要有可用的文件读写和 PPTX 编辑能力；可使用已安装的编辑库或原生演示软件工具。
- 附带的两个辅助脚本只需要 Python 3.10+ 标准库，无强制模型、连接器、付费 API 或网络依赖。
- 图片检索、品牌资源下载、生成式配图取决于 Agent 所在环境的工具与权限。
- 原生视觉检查需要能直接打开或渲染最终 PPTX 的软件。缺少该能力时，必须明确报告未完成视觉验证。
- 当前以本地 PPTX 为主要对象，未封装 Google Slides 专属 API。

## 示例

更多情景见 [examples/requests.md](examples/requests.md)。

```text
根据论文和实验图表，制作一份 15 分钟的学术答辩，保留方法、对照条件、局限和引用，不虚构实验结果。
```

```text
根据提供的月度数据，做一份可独立阅读的经营分析，图表与表格可编辑，保留单位和统计口径。
```

```text
将我的作品和项目说明整理成一份视觉设计作品集，突出实际贡献，采用编辑设计风格，不套技术架构模板。
```

```text
只优化第 5 页的图片与文字布局，其他页不改，正文一字不改，沿用现有品牌样式。
```

## 辅助脚本

在仓库根目录运行以下命令。安装技能后，将命令中的路径换成安装目录下的对应脚本。

查看方向：

```sh
python skills/pptx-studio/scripts/plan.py --list
```

记录用户已明确的选择：

```sh
python skills/pptx-studio/scripts/plan.py --operation edit --source input.pptx --directions icons layout --slides 1-16 --slide-count 60 --output outputs/plan.json
```

这会生成选择记录，不会自动修改 `input.pptx`，也不会把自然语言交给一个简单的关键词分类器。自然语言理解由 Agent 负责。

完整生成任务也可以记录自由用途、受众、风格和交付约束：

```sh
python skills/pptx-studio/scripts/plan.py --operation create --topic "Community history" --purpose "Storytelling and public education" --audience "Families" --style-hint "Warm photographic style" --duration-minutes 15 --target-slide-count 10 --output outputs/plan.json
```

计划 JSON 使用版本 2，增加 `brief` 字段。`--slide-count` 是已有文件的页数，`--target-slide-count` 是期望的成品总页数，含封面和结束页（如有）；不会根据时长擅自换算页数，也不会把用途限定为预设类别。

只读检查已有文件：

```sh
python skills/pptx-studio/scripts/inspect_pptx.py input.pptx --slides 2 --output outputs/preflight.json
```

检查包括：重复对象 ID、同位置的重复文字候选、表格段落与额外文本框叠加、文字对象边界交叠、对象越界、内部关系目标文件缺失，以及选中页面里图片或超链接使用的关系编号缺失。分组坐标和实际幻灯片顺序会被解析；有效外部链接不会被当成本地缺失文件，也不会被自动下载。

这些是结构与近似几何检查，不能识别所有字体替换、文字实际换行、旋转和 SmartArt 问题；部分合法设计也可能被标为候选。报告始终写明 `visual_verification.status = not_checked`，需要直接查看最终 PPTX 才能评价实际显示效果。报告含源文件文字，公开分享前应检查内容。

退出码：`0` 为没有结构错误，`1` 为发现结构错误（或 `--strict` 下的警告），`2` 为输入/选择等执行错误。`0` 不代表美观或原生渲染验证通过。脚本只检查，不自动删除图层。

## 目录与扩展

```text
skills/pptx-studio/
  SKILL.md                  入口、方向选择、执行与交付约定
  README.md                 独立安装与调用说明
  agents/openai.yaml        可选客户端元数据
  references/directions.json 方向目录的机器可读来源
  references/generation.md  完整生成流程与逐页规划
  references/scenarios.md   不同用途的结构与证据标准
  references/*.md           各方向及共享验证/后端说明
  references/icon-sourcing.md 图标来源、检索与语义对照
  references/layout-recipes.md 四类可调整构图配方
  scripts/plan.py           显式选择记录
  scripts/inspect_pptx.py   只读结构检查
  examples/                 公开合成样例、前后文件与验证说明
examples/                    使用请求
evals/                      人工行为评估情景
tests/                      合成文件回归测试
tools/validate_skill.py     仓库结构与引用检查
```

新增用途通常无需修改程序枚举：依据自由需求组合结构与能力即可。需要沉淀特有的内容组织经验时，补充 `scenarios.md` 的对应说明。增加新的能力模块时，才在 `directions.json` 注册 ID 和指引路径，并补充入口与评估情景。已有约定尽量放在共享文件中。

## 本地检查与质量状态

```sh
python tools/validate_skill.py
python -m unittest discover -s tests -v
```

自动测试覆盖自由用途与风格记录、成品总页数、时长校验、方向组合、明确选择不扩展范围、非法页码、只检查操作、真实坐标变换、重复文字层、表格叠字、缺失资源、只读约束和 CLI 退出码。合成 OOXML 测试用于验证解析逻辑，不作为可视化展示样张。

[evals/scenarios.json](evals/scenarios.json) 是供 Agent 试用的人工行为评估用例。自动测试通过不等于这些自然语言情景已经完成模型评估，也不等于各个方向都能在所有客户端中稳定产出。

实际运行与结果记录方法见 [evals/README.md](evals/README.md)。公开的 [三页前后样例](skills/pptx-studio/examples/README.md) 单独记录 Agent 执行结果、渲染工具和限制，不冒充独立评测或全部情景通过。

设计参考与本项目的取舍见 [design-notes.md](evals/design-notes.md)。

打包安装目录与完整源代码：

```sh
python tools/package_skill.py
```

`dist/pptx-studio-skill.zip` 可用于分发技能文件夹；`dist/pptx-studio-source.zip` 包含 README、测试和开发工具。打包范围为明确列出的公开路径，排除本地测试输出与缓存。

仓库附带 GitHub Actions 检查配置；只有推送到 GitHub 并实际运行后，才能确认远端 CI 的结果。

## 开源与发布

代码与技能指引采用 [MIT License](LICENSE)。仓库不包含客户原始 PPT、私人截图、官方品牌 Logo 或第三方字体包。公开样例中的第三方图标保留对应来源和许可声明；以后添加素材时分别核对其分发条件。

目标仓库为 `aaasdasdsacwa/pptx-studio`。后续更名时，同步修改技能文件夹、frontmatter、辅助工具中的路径及示例调用。只有实际上传成功后，远程仓库才会包含本地新增或修改的文件。

发布或升级后，继续用自有或可公开的演示文稿完成单方向和多方向试用，并在目标演示软件里复核最终 PPTX。公开样例用于展示可检查的结果，不代表所有客户端或复杂文件均已验证。
