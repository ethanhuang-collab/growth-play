# Naming And The Flow Chart

These files decide how a growth play's node chart is named, split, drawn, and checked. Apply them while writing `workflow-plan.md`, before Ethan sees the page and before any node is created in Clay.

| Piece | What it does |
| --- | --- |
| [naming.md](naming.md) | Gives each business stage one number and its executable substeps letters, then keeps those addresses unique when the graph is split, merged, or renumbered. |
| [design.md](design.md) | Splits nodes by business job before naming them, so a gate, a cleanup, and a join are not hidden inside one broad step. |
| [graph/SKILL.md](graph/SKILL.md) | Draws the workflow as a node graph and checks the live Clay canvas by its real ports and wires, not by saved coordinates alone. |
| [The Node Chart Format](../../docs/workflow-lifecycle.md) | Sets the house Mermaid chart: main path down, decisions as diamonds, stops to the left, orange for external writes, green for test blockers, and at most 25 boxes. |
| [chart_check.py](../../lifecycle/chart_check.py) | Fails a chart that breaks the format, collapses an unregistered block, or hides a decision or a stop inside a box. |
| [Chart writer](../../lifecycle/briefs/chart-writer.md) and [chart critic](../../lifecycle/briefs/chart-critic.md) | One agent drafts the signed chart from the overview and the global blocks, and a second agent attacks that draft before Ethan signs it. |
