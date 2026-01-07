# LOM → Alexandrian Academy Mapping (Interoperability Contract)

## Why this matters
We treat IEEE LOM-style metadata as an interoperability surface: it allows export/import with learning platforms while preserving our provenance, governance, and jurisdictional constraints. We do not aim to reproduce every legacy field; instead we map the "load-bearing" educational semantics into our canon objects and keep the rest as optional extensions.

## Our canonical objects in scope
- CurriculumPlan (program-level intent + jurisdiction/pedagogy profile)
- UnitMap (graph of learning nodes + relationships)
- AssessmentPlan (evaluation schema + mastery thresholds)
- EvidenceBundle (provenance anchors and artifacts)

We assume these are the “truth containers.” LOM becomes a translation layer, not the authority.

---

## IEEE LOM categories → Our fields (field-by-field)

### 1) General
- LOM.General.Identifier → header.object_id (and/or external_ids[])
- LOM.General.Title → learning_object.title
- LOM.General.Language → learning_object.language
- LOM.General.Description → learning_object.description
- LOM.General.Keyword → learning_object.keywords[]
- LOM.General.Coverage → learning_object.coverage (jurisdictional + topical), prefer standards links

### 2) LifeCycle
- LOM.LifeCycle.Version → learning_object.version (also ChangeSet references)
- LOM.LifeCycle.Status → header.state (sandbox|canon)
- LOM.LifeCycle.Contribute (role, entity, date) → attribution[] + provenance (Moirai ChangeSet)
  - Under MIT, attribution still matters for accountability/provenance/credit/governance.

### 3) Meta-Metadata
- LOM.MetaMetadata.Identifier → header.object_id (if LOM identifier is primary), else external_ids[]
- LOM.MetaMetadata.Contribute → attribution[] (editor/curator roles)
- LOM.MetaMetadata.MetadataSchema → header.schema_id or schema_ref

### 4) Technical
- LOM.Technical.Format → artifacts[].mime_type
- LOM.Technical.Location → artifacts[].uri (only for non-sensitive public URIs; otherwise internal pointers)
- LOM.Technical.Requirement → policy/parameters constraints (runtime/device/accessibility)
- LOM.Technical.Duration → learning_object.duration_seconds

### 5) Educational
This is where our pedagogy profiles anchor.
- LOM.Educational.LearningResourceType → learning_object.resource_type
- LOM.Educational.InteractivityType → learning_object.interactivity_type
- LOM.Educational.InteractivityLevel → learning_object.interactivity_level
- LOM.Educational.SemanticDensity → learning_object.semantic_density
- LOM.Educational.IntendedEndUserRole → learning_object.audience.roles[]
- LOM.Educational.Context → learning_object.context (grade bands, environments)
- LOM.Educational.TypicalAgeRange → learning_object.audience.age_range
- LOM.Educational.Difficulty → learning_object.difficulty
- LOM.Educational.TypicalLearningTime → learning_object.typical_learning_time_minutes
- LOM.Educational.Description → learning_object.pedagogy_notes
- LOM.Educational.Language → learning_object.language (if distinct)

### 6) Rights
- LOM.Rights.Cost → rights.cost = "none"
- LOM.Rights.CopyrightAndOtherRestrictions → rights.license = "MIT"
- LOM.Rights.Description → rights.notice + attribution guidance
We treat the platform as community-owned; permissive license does not remove provenance requirements.

### 7) Relation
- LOM.Relation.Kind → UnitMap edges (prerequisite, isPartOf, references, etc.)
- LOM.Relation.Resource.Identifier → node_id or external_refs[]
We prefer explicit typed edges in UnitMap.

### 8) Annotation
- LOM.Annotation.Entity/Date/Description → EvidenceBundle notes + Moirai ChangeSet justification entries

### 9) Classification
- LOM.Classification.Purpose → standards linkage (STD::*), taxonomy tags, jurisdiction profile references
- LOM.Classification.TaxonPath → standards.registry entries or domain taxonomies

---

## Minimal LOM export subset (recommended)
When exporting, include:
- Identifier, Title, Description, Language
- Educational: type, difficulty, typical time
- Rights: MIT
- Relation: prerequisites / part-of
Everything else is optional.

---

## Constraints we enforce that LOM does not
- Evidence anchoring (Ariadne’s Thread)
- Jurisdiction profiles (US-PA now, extensible)
- Canon promotion via ChangeSets (Moirai Ledger)
