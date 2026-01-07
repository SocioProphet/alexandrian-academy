# edX Structure Map to Alexandrian Academy Objects

edX conceptual hierarchy:
Course → Section → Subsection → Unit → Component

Mapping:
- Course → CurriculumPlan
- Section/Subsection → UnitMap nodes (module/group nodes)
- Unit → UnitMap leaf nodes
- Component (video/problem/html) → Mnemosyne Forge assets + renderer-specific payloads

Operational notes:
- UnitMap expresses prerequisites and adjacency.
- CurriculumPlan expresses cadence, jurisdiction requirements, pedagogy overlays, and NBA policy hooks.
