# Repository Guidance / 仓库指南

## Scope / 范围

This repository owns the public, portable, research-only `stock-research` Agent Skill. Personal paths, private channels, broker readiness, account state, and trade execution belong outside this repository. / 本仓库负责公开、可移植、仅研究的 `stock-research` Agent Skill；个人路径、私人频道、券商准备度、账户状态和交易执行均不属于本仓库。

## Development / 开发

- Follow test-driven development: add or update a failing test before changing behavior. / 遵循测试驱动开发：改变行为前先新增或更新失败测试。
- Keep tests in the repository-root `test/` directory. / 将测试放在仓库根目录的 `test/` 目录。
- Keep the published Skill bilingual when Chinese text is present. / 发布 Skill 中出现中文时必须配套英文。
- Keep `SKILL.md` below 500 lines and move detail into one-level `references/`. / 保持 `SKILL.md` 少于 500 行，并把细节移入一层 `references/`。
- Never add credentials, private paths, account values, broker payloads, or executable order fields. / 不得加入凭证、私人路径、账户市值、券商载荷或可执行订单字段。
- Update this file, `README.md`, `pyproject.toml`, and Skill metadata for every feature release. / 每次功能发布都更新本文件、`README.md`、`pyproject.toml` 和 Skill metadata。

## Verification / 验证

```bash
python3 test/test_public_release.py
python3 -m compileall -q skills/stock-research/scripts
```

## Version history / 版本历史

- `v0.1.0` (2026-08-30): Initial public community edition with evidence-first research, valuation, safety, and deterministic validation. / 首个公开社区版本，包含证据优先研究、估值、安全和确定性验证。
