---
name: 📦 Dependency Proposal
about: Propose and evaluate a new dependency using the project framework
title: "[Dependency]: "
labels: dependencies
assignees:
---

### Assessment Status (select exactly one)

- [ ] Assessment is ongoing, issue text will be replaced with updated information.
- [ ] ASsessment is finished, issue text will not be changed, anymore.

### Problem and Expected Benefit

What problem are we solving, and why is this dependency needed?

### Baseline Eligibility (all must be checked)

- [ ] The package has a clear license statement.
- [ ] The license is compatible with our AGPL-3.0 project license.
- [ ] The package has at least one formal release.
- [ ] The package uses or clearly documents semantic versioning.
- [ ] The package shows active development and release activity in the past 12 months.
- [ ] The proposed version has no known unpatched critical security issues.

Evidence (links to license, release history, advisories, etc.):

### Impact Factor (select exactly one)

- [ ] 0 - Not influenceable (for example, required peer dependency).
- [ ] 1 - Optional or minor dependency with low product impact.
- [ ] 2 - Utility dependency with locally limited scope.
- [ ] 3 - Utility dependency with potentially wider scope.
- [ ] 4 - Supports a minor feature relevant to some users.
- [ ] 5 - Supports a major feature relevant to many users.
- [ ] 6 - Supports a major feature relevant to most users.
- [ ] 7 - Key architectural dependency.

### Discovery

#### Search Criteria

- Must: …
- Should: …
- May: …

#### Candidates Considered

| Candidate | Link | Why Included |
|-----------|------|--------------|
|           |      |              |
|           |      |              |
|           |      |              |

### Assessment

Fill in measured values and resulting ranking scores.

| Metric                     | Candidate A | Candidate B | Candidate C |
|----------------------------|-------------|-------------|-------------|
| Project Age (months)       | xyz (S)     | xyz (S)     | xyz (S)     |
| Project Size (LoC)         | xyz (S)     | xyz (S)     | xyz (S)     |
| Development Activity       | xyz (S)     | xyz (S)     | xyz (S)     |
| Release Activity           | xyz (S)     | xyz (S)     | xyz (S)     |
| Community Activity         | xyz (S)     | xyz (S)     | xyz (S)     |
| Issue Handling (%)         | xyz (S)     | xyz (S)     | xyz (S)     |
| **Assessment Score (sum)** | **SUM**     | **SUM**     | **SUM**     |

### Exploration (required for impact factor >= 4 or close assessment scores)

- [ ] Not required (impact factor <= 3 and clear winner from assessment)
- [ ] Required and completed

Research questions (framed numerically):

- …
- …
- …

Prototype links (branch/repository/PR): …

Prototype results:

| Criterion        | Candidate A | Candidate B | Candidate C |
|------------------|-------------|-------------|-------------|
| Assessment Score | xyz (S)     | xyz (S)     | xyz (S)     |
|                  | xyz (S)     | xyz (S)     | xyz (S)     |
| **Final Score**  | **SUM**     | **SUM**     | **SUM**     |

### Final Decision

- Chosen dependency: …
- Chosen version: …
- Rationale: …

### Adoption and Maintenance Plan

- Migration or rollback strategy: …
- Owner or maintainer: …
- Monitoring plan (security updates, release checks): …

### Approvals

- [ ] Technical review completed
- [ ] License review completed
- [ ] Security review completed (if required)
- [ ] Architecture approval completed (if required)
