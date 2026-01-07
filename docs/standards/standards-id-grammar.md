# Standards Identifier Grammar (v1)

Goal: stable, globally unique identifiers for standards nodes so we can:
- tag UnitMap nodes/edges and AssessmentPlan items deterministically,
- do jurisdictional crosswalks,
- avoid collisions when multiple standard sets exist.

## Canonical ID format

STD::<COUNTRY>::<JURISDICTION>::<STANDARD_SET>::<VERSION>::<PATH>

Where:
- COUNTRY: ISO 3166-1 alpha-2 (e.g., US)
- JURISDICTION: regional code (e.g., PA). Subregions are allowed later (e.g., PA.PhiladelphiaSD)
- STANDARD_SET: short stable token for the standard set (e.g., PA-ACADEMIC, PA-ELA, PA-MATH, NGSS)
- VERSION: semver-like or published revision token (e.g., 2025.1, v1)
- PATH: colon-delimited hierarchy tokens (no spaces; use '-' for punctuation)

Example:
STD::US::PA::PA-ELA::v1::K:Reading:FoundationalSkills:RF.1.1

## Constraints
- IDs are case-sensitive, but we default to uppercase for COUNTRY/JURISDICTION and stable tokens.
- PATH must be deterministic and derived from the authoritative published structure.
- If the authoritative standard already has a code (e.g., "RF.1.1"), that code must appear in PATH.

## Crosswalk conventions
Crosswalk entries use:
XWALK::<FROM_STD_ID>::TO::<TO_STD_ID>

Example:
XWALK::STD::US::PA::PA-ELA::v1::K:Reading:RF.1.1::TO::STD::US::PA::PA-ACADEMIC::v1::ELA:K:RF.1.1
