# Change impact and failure diagnosis

Collect only evidence relevant to the request. Prefer the repository's current
contract and saved candidate over broad source-store searches. Keep raw customer
data and credentials out of exported reviews; use minimal approved records.

## Inventory by identity

For each node record the stable logical ID, platform ID if available, current
name/address, intended stage, lifecycle, executable type, consumers and contract.
Record group/header membership separately from execution. If only names are
available, flag identity ambiguity; do not claim safe rename matching.

Inspect both the execution graph and data-reference graph. They can differ:
code can reference a node outside the visible path, branches can rejoin, and a
shared prompt or schema may affect several consumers without changing edges.

| Surface | Inspect when changed |
| --- | --- |
| Node removal/merge | Input bindings, output-source paths, depends-on lists, edges, routes, terminals, expected paths, fixtures, battle-test targets, stage/group membership. |
| Schema/code/prompt | Required versus optional fields, null/empty behavior, source versions, exact consumers, changed-node and connected-path proof. |
| Name/address | Display name versus label fields, name-keyed outputs/lookups, transition strings, diagnostics, stage/group titles, current diagrams and instructions. |
| Stage move | Remove old membership, add new membership, reject accidental multiple ownership, regenerate affected headings/map. |
| Layout/group | Section/lane anchors, all nearby wires and cards, port order, native group boundaries, crossings and title placement. |
| Shared configuration | Every affected node and consumer; current dependency selections and material differences. |

Do not repair A→B→C by assuming A→C is valid after B is removed. Identify which
fields C needed from B and where they will now come from. If the answer is not
established, propose alternatives and retain the unresolved decision. Do not
silently delete failed checks to make a candidate pass.

## Common causes to distinguish

1. **Partial mutation:** only one representation changed; downstream contracts
   or current documentation were omitted.
2. **Identity mismatch:** an applier matched by mutable name; a rename created a
   new node, or a same-name content edit was skipped. Prove the actual path.
3. **Wrong rule:** a generic checker rejected a current project exception, or
   a generator inferred business stages from executable node count.
4. **Wrong evidence:** saved positions, historical tests or the wrong
   draft/published link were presented as current native acceptance.
5. **Concurrent drift:** another writer changed the shared target after the
   candidate was prepared. Compare snapshots/receipts; do not infer a race just
   because there were several agents.
6. **Platform limitation:** native ports or group restrictions prevent the
   proposed presentation. Distinguish unavailable capability from a bad design.

For a retrospective, give each finding its symptom, expected behavior,
evidence, causal confidence, status (fixed/partial/open), smallest correction
and check. An offline reproduction establishes a possible mechanism; only
matching historical evidence attributes that mechanism to a specific incident.

## Application and proof handoff

The skill prepares a review, not an automatic transaction. When implementation
is independently authorized, use or extend the existing supported apply path:

1. Compare the current target with the candidate's base and last synchronized
   version. Preserve unrelated changes; one writer integrates a workflow.
2. Apply scoped changes by stable identity. A name existing is not proof that
   code, bindings, schema or display state match. Validate the complete
   resulting candidate before applying; incomplete intermediate patches are
   not releasable artifacts.
3. Read back actual fields, references, names, groups and positions. Handle
   partial application explicitly. Do not blindly roll back a stale whole graph
   over another writer's work; reconcile using fresh state and ownership.
4. Use existing material hashes where available. Pure display edits invalidate
   presentation evidence; executable changes invalidate the changed node and
   affected path evidence. Operational name changes count as executable changes.
5. Verify semantic decisions and current naming separately from native geometry
   and runtime. A single-node replay does not prove downstream connectivity;
   a successful write response does not prove saved content or native execution.
6. Record source commit, target draft/snapshot, readback match, checks, remaining
   unknowns and publication state separately. Link to the same state inspected.

A writer lease is cooperative coordination unless the platform enforces it.
Do not assume it excludes UI writers or provides compare-and-swap. Existing
approval gates for run cost, external writes and publication remain separate.

## Efficient review

Prefer captured real workflow metadata and inputs. Use small labeled synthetic
cases for edge conditions missing from the real corpus. Define expected
outcomes independently of checker results. Include positive controls for
approved gaps, multi-outcome gates, independent lane depth and project bridges.
Do not mistake a reproduction script exiting successfully for a workflow pass.

Parallelize independent read-only review or isolated node tests against one
pinned candidate. Integrate through one owner and perform affected connected
path checks. No prescribed agent count or nested review team is required.
