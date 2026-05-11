---
name: AAS template compliance issues
description: IDTA template semanticId mismatches and structural issues in current AASX files
type: feedback
---

When validating AAS instances against IDTA templates, watch for these specific issues:

1. **semanticId URI mismatch** — The IDTA template for "Digital Nameplate v3.0" uses semanticId `https://admin-shell.io/idta/nameplate/3/0/Nameplate`, but the CRX10iA instance uses the same URI — this is correct *if* the instance matches the template structure exactly. However, the CRX10iA_Type.json uses `0173-1#01-AHX837#002` for TechnicalData which *is* the correct eCLASS-based semanticId per the IDTA 02003-2-0 template. Always verify against the actual template JSON.

2. **SubmodelElementCollection vs List confusion** — In CRX10iA_Type.json, `TechnicalPropertyAreas` is modeled as a `SubmodelElementList` with `typeValueListElement="SubmodelElementCollection"`, which is correct per IDTA 02003-2-0. However, the nested `Customer` entry is a `SubmodelElementCollection`, not a list element — this is correct.

3. **Missing eCLASS reference in CRX10iA_001.json** — The instance file only has Nameplate submodel but is missing the TechnicalData, HandoverDocumentation, and CapabilityDescription submodels that the type shell defines. The instance should inherit or explicitly reference these.

4. **Template qualifiers missing** — IDTA templates include `TemplateQualifier` entries with cardinality constraints (e.g., `One`, `ZeroToOne`, `OneToMany`). The CRX10iA files do not include these qualifiers, making them less interoperable.

5. ** supplementalSemanticIds should reference eCLASS/VDI standards** — Many properties in CRX10iA files use non-standard URIs (e.g., `https://admin-shell.io/dfki/aas-hybrid-mcp/TechnicalData/MaxTcpSpeed/1/0`). These should either be:
   - Mapped to official IDTA/eCLASS URIs, or
   - Defined as ConceptDescriptions in the AAS with proper dataSpecifications

**Why:** The IDTA templates are mature specifications (v3.0 for nameplate, v2.0 for technical data). Deviating from their exact semanticId URIs and structure reduces interoperability with other AAS implementations, especially AASX Package Explorer and BaSyx.

**How to apply:** Before adding new AAS instances:
1. Read the corresponding IDTA template JSON (in `idta_templates/`)
2. Copy the exact `semanticId` values from the template
3. Include all `qualifiers` with `TemplateQualifier` type
4. Use only official eCLASS/VDI/IEC semanticIds where specified
5. Define custom ConceptDescriptions in the AAS if a property lacks a standard URI
