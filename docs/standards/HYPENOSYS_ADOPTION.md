# Hypenosys standard — adoption and gap register

Requested reference: https://dev.hypenosys.com/documentacion

**Access result:** the published standard could not be retrieved from the available browser environment on 2026-10-14. This document **does not** claim exact compliance or substitute inferred requirements for the authoritative text. Review this file against the live standard before merging the PR.

## Provisional engineering conventions

- Maintain an explanatory root README with setup, architecture, project status and links.
- Use authored source and provenance metadata with stable IDs.
- Maintain documentation separately from generated/data fixtures and implementations.
- Require isolated feature branches and a reviewed PR; do not commit directly into master.
- Ship a deterministic validator and negative unit tests. Gate PRs with CI.
- Keep explicit evidence distinctions: documented != implemented != host-tested != VICE-observed != C64 Ultimate-observed.
- Link all documents with relative paths; preserve existing LICENSE and .gitignore.
- No unlicensed third-party audiovisual material, ROMs or original binary assets.

## Unverified standard-specific items

- Mandatory repo tree, issue/PR templates and labels.
- Naming/language/versioning conventions defined by Hypenosys.
- Required development, design, QA and review approvals.
- Release and security compliance requirements.

Once the documentation becomes reachable, add an evidence-backed crosswalk of each obligation to exact files/tests and close this gap in a separate change.
