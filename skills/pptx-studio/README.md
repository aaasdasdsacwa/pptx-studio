# PPTX Studio

面向多种用途生成、修改或检查 PowerPoint。从主题、大纲、文档、数据、图片或已有稿件出发，根据目的与受众组织整份演示，完成逐页规划、视觉设计、素材整合和可编辑文件制作。

工作汇报、经营分析、产品销售、教学培训、学术答辩、技术交流、公开演讲、品牌作品集、文化与个人叙事等是可组合的用途示例，不是固定分类。内容、版式、图标、图片、图表、风格和修复是按需调用的能力；用户可以直接要求生成完整 PPT，无需先勾选模块。

## 安装与调用

将**整个 `pptx-studio` 文件夹**复制到客户端支持的技能目录，保留子目录结构。以支持项目级 `.agents/skills` 的客户端为例，在你的项目目录执行：

```powershell
New-Item -ItemType Directory -Force '.agents/skills' | Out-Null
Copy-Item -LiteralPath '下载位置/skills/pptx-studio' -Destination '.agents/skills/pptx-studio' -Recurse
```

macOS / Linux：

```sh
mkdir -p .agents/skills
cp -R 下载位置/skills/pptx-studio .agents/skills/
```

把“下载位置”换成实际解压或克隆的位置；若目标已安装旧版本，先备份再更新，避免残留旧文件。客户端的发现、刷新及启用方式以其说明为准。

支持 `$名称` 调用的客户端可以输入：

> 使用 $pptx-studio，将这份项目材料整理成一份管理层决策汇报，总共 10 页，沿用附件品牌。

> 使用 $pptx-studio，面向高中生做一份有关光合作用的课件，包含示意图和练习，参考提供的教材。

> 使用 $pptx-studio，根据论文及其图表制作学术答辩，保留研究限制和引用。

> 使用 $pptx-studio，将这些照片和故事做成一份文化分享，暖色、摄影为主，加入适量讲述备注。

> 使用 $pptx-studio，只完善第 3 页图标或修复局部排版，保留其余页面和原文。

> 使用 $pptx-studio，只检查第 1–8 页，给出带页码和对象位置的问题清单，不修改文件。

## 运行条件

Skill 由支持 Agent Skills 的 AI Agent 执行，需要 Agent 能读写文件并使用至少一种 PPTX 编辑工具。它提供工作流程和辅助检查，不是独立运行的一键制作软件。

- 两个附带脚本使用 Python 3.10+ 标准库，无第三方 Python 依赖。
- 制作或修改还需要环境中可用的演示编辑工具或库。配置方法见 [backends.md](references/backends.md)。
- 素材检索或下载需要对应工具和网络；离线时可复用获准素材，缺少官方 Logo 时应明确说明。
- 查看实际效果需要能直接打开或渲染最终 PPTX 的工具。结构检查通过不等于视觉验证完成。

以下命令从**本文件所在的 Skill 目录**运行，不依赖外层仓库：

```sh
python scripts/plan.py --list
python scripts/plan.py --operation create --topic "Museum visit" --purpose "Public education" --audience "Families" --style-hint "Photographic" --target-slide-count 8 --duration-minutes 15
python scripts/inspect_pptx.py input.pptx --slides 1-8 --output outputs/preflight.json
```

`plan.py` 只记录明确选择与制作需求，JSON 版本为 2，用途和风格允许自由文本；成品总页数与源文件页数分别记录。它不自动生成页面。`inspect_pptx.py` 只读检查，报告可能包含源文件文字。退出码与能力边界见 [verification.md](references/verification.md)。

## 资源与扩展

- [SKILL.md](SKILL.md)：Agent 入口、完整生成与局部编辑。
- [完整生成流程](references/generation.md)：材料、主线、逐页规划、视觉系统与演讲备注。
- [场景适配](references/scenarios.md)：不同目的的结构与证据标准，支持跨场景组合。
- [图标来源与选型](references/icon-sourcing.md)：检索关键词、风格选择和语义对照。
- [构图配方](references/layout-recipes.md)：时间轴、比较、流程、架构的可调整布局。
- [示例说明](examples/README.md)：公开合成样例与验证边界。

本目录可独立放入技能合集的 `skills/pptx-studio`，无需外层仓库的测试、开发工具或临时输出。开发源代码见 [项目仓库](https://github.com/aaasdasdsacwa/pptx-studio)。指引及脚本采用 [MIT](LICENSE.txt)；第三方素材保留各自许可。
