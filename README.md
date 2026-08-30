# Evidence-First Stock Research / 证据优先股票研究

Turn a stock question into an auditable research view with dated sources, explicit valuation, falsifiable theses, downside analysis, and strict no-trade boundaries. / 将股票问题转化为可审计的研究观点，包含带日期的来源、明确估值、可证伪论点、下行分析和严格的禁止交易边界。

This repository contains the public community edition of the `stock-research` Agent Skill. It is designed for Agent Skills-compatible hosts and agents that can read `SKILL.md`; host-specific behavior should be verified before claiming compatibility. / 本仓库包含 `stock-research` Agent Skill 的公开社区版本，面向兼容 Agent Skills 的宿主及能够读取 `SKILL.md` 的 Agent；声明兼容性前应验证具体宿主行为。

## What it provides / 提供的能力

- Evidence ledger with source tiers, timestamps, and conflict handling. / 包含来源分级、时间戳和冲突处理的证据账本。
- Mandatory valuation and bear, base, and bull reasoning. / 强制估值以及熊市、基准和牛市推演。
- Falsifiable theses with triggers and invalidation conditions. / 包含触发条件和失效条件的可证伪论点。
- Deterministic research-packet validation. / 确定性的研究数据包验证。
- Research-only output with no broker credentials or trade execution. / 仅研究输出，不涉及券商凭证或交易执行。

## Install / 安装

After registry publication, install from GitHub with: / registry 发布后，可从 GitHub 安装：

```bash
npx skills add lee-agi/stock-research --skill stock-research
```

Install from ClawHub with: / 从 ClawHub 安装：

```bash
clawhub install stock-research-first-principles
```

## Verify / 验证

```bash
python3 test/test_public_release.py
python3 skills/stock-research/scripts/plan_stock_research.py \
  --symbols NVDA AMD \
  --market US \
  --mode multi_compare
```

## Safety / 安全

This Skill does not place trades, request credentials, or produce executable order payloads. Outputs are general research, not personalized investment advice; data may be delayed or wrong, and investing can result in loss of capital. / 本 Skill 不下单、不索取凭证，也不生成可执行订单载荷；输出属于一般研究，而非个性化投资建议；数据可能延迟或错误，投资可能损失本金。

## Version history / 版本历史

- `v0.1.0` (2026-08-30): Initial public community edition. / 首个公开社区版本。
