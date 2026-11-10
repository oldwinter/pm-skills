# PM Skills 中文化档案

同步上游后先读本档案，再处理新增或变更内容。

## 项目定位

- 上游项目：`phuryn/pm-skills`
- 中文 fork：`oldwinter/pm-skills`
- 当前同步上游 commit：`9af7bfd`（v2.3.0，2026-11-08）
- 主要安装面：Claude Code/Cowork marketplace、Codex plugin、skills 目录
- 其他 plugin 清单：9 个 plugin 同时提供 `.claude-plugin/plugin.json` 与 `.cursor-plugin/plugin.json`，根目录提供对应 marketplace 清单
- 中文 runtime 入口：9 个 plugin 下的 72 个 `*/skills/*/SKILL.md`

## 中文化目标

每个产品管理 skill 增加中文执行导读，覆盖中文请求的路由、产出边界和验证方向；保留 PM framework 名称、公式、字段、命令、文件路径、模板结构和英文精确术语，避免改变工作流契约。法律、隐私和合规类 skill 只提供中文操作导读，不把内容表述为实时法律意见。

## 安装与交付

```text
claude plugin marketplace add oldwinter/pm-skills
codex plugin marketplace add oldwinter/pm-skills
```

然后从 `pm-skills` 安装需要的 9 个 plugin；plugin 内实际读取中文 fork 的 72 个 `SKILL.md` runtime 入口。

## 迁移说明

`pm-ai-shipping` 的三个 skill 与五个命令已迁移到上游 `phuryn/product-engineering` 的 `ai-shipping` 插件；本仓库只保留迁移指引与中文说明，不再包含可执行内容。

## 同步后检查

- `git diff --check`
- `rg -n '^(<<<<<<<|=======|>>>>>>>)$' .`
- `python validate_plugins.py`
- 9 个 plugin manifest 与 72 个 `SKILL.md` 的目录、frontmatter 和引用保持一致
