---
name: AAS type/instance separation
description: Robot AAS architecture - Type shell vs Instance shell separation
type: project
---

**AAS Structure for Robots:**

| Shell | Purpose | Content |
|-------|---------|---------|
| **CRX10iA_Type** (Type) | All robots of this type | Nameplate (ManufacturerName, ProductDesignation, ProductFamily, Country), TechnicalData (Reach, Payload, Weight, Repeatability), HandoverDocumentation (manuals), CapabilityDescription (capabilities) |
| **CRX10iA_001** (Instance) | Single robot instance | Nameplate (SerialNumber, YearOfConstruction, DateOfManufacture only) |

**Key Rule:** Submodels that describe *what the robot type is* go into the type shell; submodels that describe *which instance* go into the instance shell.

**Current Status (2026-05-08):**
- ✅ CRX10iA_Type.json: 4 submodels (Nameplate, TechnicalData, HandoverDocumentation, CapabilityDescription)
- ✅ CRX10iA_001.json: 1 submodel (Nameplate with instance-specific data only)
- ✅ `derivedFrom` correctly links instance to type via `urn:aas:crx10ia:type`

**Fixes Applied (2026-05-08):**
1. TechnicalData semanticId: `0173-1#01-AHX837#002` (eCLASS, ModelReference auf Submodel im eCLASS-System)
2. TechnicalData supplementalSemanticId: `https://api.eclass-cdp.com/0173-1-01-AHX837-002` (korrigiert)
3. HandoverDocumentation semanticId: `0173-1#01-AHF578#003` (eCLASS, ModelReference auf Submodel im eCLASS-System)
4. CapabilityDescription semanticId: `https://admin-shell.io/idta/SubmodelTemplate/CapabilityDescription/1/0` (IDTA template URI, ModelReference auf das SubmodelTemplate)
5. Nameplate semanticId (Instanz): `https://admin-shell.io/idta/nameplate/3/0/Nameplate` (IDTA Spezifikation, ExternalReference wie im Originaltemplate)

**Warum ModelReference vs ExternalReference?**

Gemäß AAS-Spezifikation (nach IDTA):

| Referenztyp | Ziel | Keys | Beispiel |
|-------------|------|------|----------|
| **ModelReference** | Element *innerhalb* eines AAS/Modells | Key-Kette (Submodel, Property, etc.) | `Submodel → Property` |
| **ExternalReference** | Element *außerhalb* der AAS (externes System) | Meist ein Key (GlobalReference) | `GlobalReference → eCLASS-ID` |

**In den IDTA Templates (Original):**

1. **Nameplate (Digital Nameplate v3.0)** → `ExternalReference` auf `https://admin-shell.io/idta/nameplate/3/0/Nameplate`
   - Spezifikations-URL, keine konkrete Submodel-Instanz im AAS

2. **TechnicalData (IDTA 02003)** → `ModelReference` mit `Submodel` Key auf `0173-1#01-AHX837#002`
   - eCLASS-basierte Submodel-ID (ModelReference verweist auf ein Submodel im eCLASS-System)

3. **HandoverDocumentation (IDTA 02004)** → `ModelReference` mit `Submodel` Key auf `0173-1#01-AHF578#003`
   - Ebenfalls eCLASS-basierte Submodel-ID

4. **CapabilityDescription (IDTA 02020)** → `ModelReference` mit `Submodel` Key auf `https://admin-shell.io/idta/SubmodelTemplate/CapabilityDescription/1/0`
   - Verweis auf das SubmodelTemplate in der IDTA-Registry

**Unser Konsens (alles wie im Originaltemplate):**
- CRX10iA_Type.json + CRX10iA_001.json: Alle semanticIds entsprechen den IDTA Templates exakt
- TechnicalData/HandoverDoc/CapabilityDesc: `ModelReference` auf eCLASS/IDTA Submodel IDs
- Nameplate: `ExternalReference` auf IDTA Spezifikations-URL

**Why:** This separation allows:
- Template-based robot models (create new instance from type)
- Versioning: Update type definition → all instances inherit (where applicable)
- Instance-specific data isolated (serial numbers, manufacturing dates)
- Efficient queries: Type shell queries return common properties; instance queries return unique identifiers

**How to apply:** When adding new robot instances:
1. Copy relevant submodel definitions from type shell
2. Replace generic values with instance-specific ones (SerialNumber, DateOfManufacture, etc.)
3. Keep shared values identical (ManufacturerName, ProductDesignation, TechnicalPropertyAreas)
4. Do NOT duplicate HandoverDocumentation or CapabilityDescription in instance shell
5. Use `derivedFrom` to establish link to type AAS
