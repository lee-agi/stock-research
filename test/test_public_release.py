"""Public release contracts for the stock-research community edition."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "stock-research"
VERSION = "0.1.0"


class TestPublicPackageContract(unittest.TestCase):
    """Verify the public package is portable, clean, and consistently versioned."""

    def test_required_release_files_exist(self) -> None:
        required = (
            REPO_ROOT / "AGENTS.md",
            REPO_ROOT / "README.md",
            REPO_ROOT / "LICENSE",
            REPO_ROOT / "pyproject.toml",
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "LICENSE",
            SKILL_ROOT / "agents" / "openai.yaml",
            SKILL_ROOT / "references" / "data-quality.md",
            SKILL_ROOT / "references" / "safety.md",
            SKILL_ROOT / "references" / "valuation.md",
            SKILL_ROOT / "references" / "workflows.md",
            SKILL_ROOT / "scripts" / "plan_stock_research.py",
            SKILL_ROOT / "scripts" / "validate_research_packet.py",
        )
        for path in required:
            self.assertTrue(path.is_file(), msg=f"missing required file: {path}")

    def test_versions_are_synchronized(self) -> None:
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        pyproject_text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        agents_text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn(f'version: "{VERSION}"', skill_text)
        self.assertIn(f'version = "{VERSION}"', pyproject_text)
        self.assertIn(f"v{VERSION}", agents_text)
        self.assertIn(f"v{VERSION}", readme_text)

    def test_public_skill_excludes_private_overlays_and_artifacts(self) -> None:
        blocked_markers = (
            "/Users/",
            "Lee's",
            "Lee ",
            "Futu",
            "#invest-report",
            "Weixin",
            "BBAE",
            ".clawdbot",
            "trading-data-adapters",
            "stock-analysis",
        )
        forbidden_names = {
            ".DS_Store",
            ".pytest_cache",
            "__pycache__",
            "decision.log",
            ".learnings",
        }

        for path in SKILL_ROOT.rglob("*"):
            self.assertNotIn(path.name, forbidden_names)
            if path.is_file() and path.suffix in {".md", ".py", ".yaml", ".yml", ".json", ".toml"}:
                text = path.read_text(encoding="utf-8")
                for marker in blocked_markers:
                    self.assertNotIn(marker, text, msg=f"private marker {marker!r} in {path}")

    def test_skill_is_concise_and_research_only(self) -> None:
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(skill_text.splitlines()), 500)
        self.assertIn("Never place or transmit a trade", skill_text)
        self.assertIn("不得下单或传输交易指令", skill_text)
        self.assertIn("not personalized investment advice", skill_text)
        self.assertIn("非个性化投资建议", skill_text)


class TestResearchPacketValidator(unittest.TestCase):
    """Exercise the deterministic publication-safe research gate."""

    @property
    def script(self) -> Path:
        return SKILL_ROOT / "scripts" / "validate_research_packet.py"

    def run_validator(self, packet: dict[str, object]) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as handle:
            json.dump(packet, handle)
            handle.flush()
            return subprocess.run(
                [sys.executable, str(self.script), handle.name, "--json"],
                capture_output=True,
                text=True,
                check=False,
            )

    def valid_packet(self) -> dict[str, object]:
        return {
            "question": "Is the current valuation supported by fundamentals?",
            "scope": {"symbols": ["ACME"], "market": "US", "horizon": "12 months"},
            "as_of": "2026-08-30T09:30:00-04:00",
            "sources": [
                {
                    "publisher": "Example issuer",
                    "url": "https://example.com/investors/report",
                    "published_at": "2026-08-20",
                    "fetched_at": "2026-08-30T09:20:00-04:00",
                }
            ],
            "valuation": {
                "methods": ["reverse DCF", "peer multiples"],
                "assumptions": ["10% revenue CAGR", "15% operating margin"],
                "range": "$80-$105",
            },
            "risks": ["Demand slowdown", "Margin compression"],
            "recommendation": {
                "stance": "watch",
                "confidence": "medium",
                "trigger": "Guidance supports the base case",
                "invalidation": "Two quarters below the margin floor",
            },
            "disclaimer": "Research only; not personalized investment advice.",
        }

    def test_valid_packet_passes(self) -> None:
        result = self.run_validator(self.valid_packet())
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])

    def test_missing_valuation_fails_closed(self) -> None:
        packet = self.valid_packet()
        del packet["valuation"]
        result = self.run_validator(packet)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("valuation", result.stdout)

    def test_order_payload_fields_are_rejected(self) -> None:
        packet = self.valid_packet()
        packet["recommendation"]["quantity"] = 100  # type: ignore[index]
        packet["recommendation"]["order_type"] = "market"  # type: ignore[index]
        result = self.run_validator(packet)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("quantity", result.stdout)
        self.assertIn("order_type", result.stdout)


class TestPlanningScript(unittest.TestCase):
    """Verify the offline planner emits a bilingual evidence-first checklist."""

    def test_planner_output_is_bilingual_and_has_no_order_action(self) -> None:
        script = SKILL_ROOT / "scripts" / "plan_stock_research.py"
        result = subprocess.run(
            [
                sys.executable,
                str(script),
                "--symbols",
                "NVDA",
                "AMD",
                "--market",
                "US",
                "--mode",
                "multi_compare",
                "--question",
                "Compare AI compute exposure",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Evidence-first research plan", result.stdout)
        self.assertIn("证据优先研究计划", result.stdout)
        self.assertIn("Direct trading action / 直接交易动作: 0", result.stdout)


if __name__ == "__main__":
    unittest.main()
