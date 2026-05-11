---
name: AAS template compliance
description: IDTA template compliance status of AASX JSON files in aasx-dev-templates/
type: feedback
last_reviewed: "2026-05-11"
---

All compliance issues from 2026-05-08 have been resolved.

## Current template compliance

### TechnicalData (IDTA 02003 v2.0)
- **CRX10iA, UR3e, UR20**: `administration.templateId: "https://admin-shell.io/idta-02003-2-0"`, `semanticId` = ModelReference on `0173-1#01-AHX837#002` (eClass)
- `TechnicalProperties` is a `SubmodelElementList` with `semanticIdListElement: "0173-1#02-ABL358#002/0173-1#01-AHX773#002"`
- Properties grouped into `MechanicalProperties`, `EnvironmentalProperties`, `SafetyProperties`
- Every leaf property has `semanticId` + `description`
- Custom DFKI semanticIds resolved via ConceptDescriptions (`aas-hybrid-mcp-concept-descriptions.json`, IEC61360)

### TechnicalData for AGV (IDTA 02047 v1.0)
- **MiR100, MiR250**: `templateId: "https://admin-shell.io/idta-02047-1-0"`, `semanticId` = ModelReference on `https://admin-shell.io/idta/SubmodelTemplate/technicaldataagv/1/0`
- Structure matches template: `GeneralInformation` → `SpecificDescriptions` → `DataSheet` → `TypeAndApplicationInformation` / `TechnicalParameters`

### Facility Information (DFKI custom)
- **Hall3, Hall4**: `templateId: "https://admin-shell.io/dfki/facility-information/1/0"`, `semanticId` = ExternalReference
- Template: `DFKI_Facility_Information_Template.json`
- Properties: `Area` (m²), `PrimaryUse` (MultiLanguage), `PowerConnection` (kV)
- ConceptDescriptions: `aas-hybrid-mcp-concept-descriptions.json` (Facility section)

### Nameplate (IDTA 02006 v3.0), HandoverDocumentation (IDTA 02004 v2.0), CapabilityDescription (IDTA 02020 v1.0), HierarchicalStructures
All instances use the correct `templateId` and `semanticId` values from their respective IDTA templates.

## Design decisions
- **TemplateQualifier in instances**: Not used. Qualifiers define template cardinality constraints; they are only relevant in the template definition, not in an instance that already satisfies those constraints.
- **DFKI custom semanticIds**: DFKI-specific properties use `https://admin-shell.io/dfki/aas-hybrid-mcp/{Domain}/{Property}/1/0` URIs with matching IEC61360 ConceptDescriptions. This is the correct pattern for non-standard properties.
- **Units in idShort**: Units are NOT embedded in `idShort` (e.g., `Reach`, not `Reach_mm`). Units are defined in the ConceptDescription (`modelType: "DataSpecificationIec61360"` → `unit: "mm"`).
