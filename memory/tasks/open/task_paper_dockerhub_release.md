---
name: Task — Paper §07 Docker Hub TODO: Resolve Before Submission
description: Replace the literal "TODO: push to Docker Hub" in §07 with an actual image URL, or rephrase if the image is not yet published.
type: task
status: open
priority: medium
---

## Summary

§07 v2 Ingestion Plugin contains the following text visible in the PDF:

> "The v2 plugin image is TODO: push to Docker Hub
> (`dfkibasys/aas-neo4j-kafka-connect-plugin:7.9.1-2.0.0`)."

This is a plain TODO embedded in the paper text — it will appear verbatim in the published
PDF if not resolved before submission.

## Subtasks

### T1 — Publish Docker Hub image (deployment action)

Push the v2 plugin image to Docker Hub under:
`dfkibasys/aas-neo4j-kafka-connect-plugin:7.9.1-2.0.0`

This is a deployment task outside the paper itself. Requires Docker Hub account access
under the `dfkibasys` organisation.

### T2 — Update §07 text after publish

Once the image is published, replace the TODO sentence in `07-ingestion-plugin.tex`:

Current:
```
The v2 plugin image is TODO: push to Docker Hub (\texttt{dfkibasys/aas-neo4j-kafka-connect-plugin:7.9.1-2.0.0}).
```

Replace with:
```
The v2 plugin image is available at \texttt{dfkibasys/aas-neo4j-kafka-connect-plugin:7.9.1-2.0.0}.
```

### T2-alt — If image cannot be published before submission

Remove the Docker Hub sentence entirely, or replace with:
```
The v2 plugin image will be published to Docker Hub (\texttt{dfkibasys/aas-neo4j-kafka-connect-plugin}) alongside the final release.
```

## Acceptance Criteria

- No literal "TODO" text in any `.tex` file included in the PDF
- §07 sentence either names a live Docker Hub URL or uses forward-looking language
- Paper builds without errors

## References

- `paper/etfa2026/claim_audit.md` row B1
- §07 `07-ingestion-plugin.tex` line 5
