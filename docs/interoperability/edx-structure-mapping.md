# edX/OLX Structure → Alexandrian Academy Mapping

## Why this matters
edX-style courseware expresses pedagogy as a hierarchy of containers and components. Our model expresses pedagogy as a graph (UnitMap) plus governing envelopes (CurriculumPlan/AssessmentPlan) with provenance and jurisdiction constraints. This mapping makes import/export possible without losing governance semantics.

---

## edX high-level hierarchy (conceptual)
Common levels:
- Course
- Section
- Subsection
- Unit
- Component (HTML, Video, Problem, Discussion, etc.)

edX also uses:
- "sequential" for subsections
- "vertical" for units
- "block" for components

---

## Mapping to our objects

### Course → CurriculumPlan
- Course metadata → CurriculumPlan.learning_program fields
- Course run parameters → policy parameter sheet references
- Course-level standards → CurriculumPlan.standards_coverage[]

### Section/Subsection/Unit → UnitMap nodes (typed)
We map each structural element into a node with type:
- node.type ∈ {section, subsection, unit, component}
Edges are explicit:
- is_part_of
- precedes (ordered sequencing)
- prerequisite_of (mastery gating)

### Component → Artifact + Learning node
For media and interactive blocks:
- The raw content becomes artifacts[] in EvidenceBundle or Mnemosyne Forge
- The learning semantics become a UnitMap node with resource_type:
  - video
  - reading
  - problem
  - discussion
  - lab
  - project

### Grading/Problems → AssessmentPlan
- Problem sets, item banks, rubrics → AssessmentPlan items
- Mastery thresholds → AssessmentPlan.mastery_policy

---

## Export guidance (minimal viable)
To export to edX-like systems, we generate:
- a hierarchical view derived from UnitMap (topological + stable ordering)
- components as packaged artifacts (video + captions + HTML)
- problem definitions from AssessmentPlan where applicable

---

## Import guidance (minimal viable)
When importing:
- preserve original identifiers in external_ids[]
- store raw OLX as an artifact for provenance
- create UnitMap nodes for each block
- store grading logic in AssessmentPlan where representable, else as artifacts
