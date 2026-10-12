# Skills For Building A Growth Play

Each skill below is the copy that ships with this kit. The Cursor install may still point at `coding-system` until that symlink is moved here.

## Chart, Names, And Review

| Skill | What it does |
| --- | --- |
| [Node naming](../chart/naming.md) | Assigns one number to each business stage and letters to its substeps and outcomes, and renumbers the whole map after a split or merge. |
| [Node design](../chart/design.md) | Checks that each node is one business job before the chart is named, so cleanup and gates are not buried inside a setup node. |
| [Workflow node graph](../chart/graph/SKILL.md) | Renders the process as a node-and-wire graph and verifies the native Clay layout from the actual ports and wires. |
| [Adversarial review](adversarial-review/SKILL.md) | Sends the overview, chart, or outputs to isolated critics and a judge on a different model family, then keeps only the findings the judge can verify. |
| [QC](qc/SKILL.md) | Runs the final ship check by picking the specialist lanes, reading the evidence, and giving one ship or no-ship judgment. |
| [GTM play QC](gtm-play-qc/SKILL.md) | Pressure-tests who the play selects, when it reaches them, what it implies, and when it should stop, without running the workflow. |
| [Clay workflow QC](clay-workflow-qc/SKILL.md) | Checks pins, bindings, transitions, schemas, and write gates on the Clay graph, read-only. |
| [Workflow change review](workflow-change-review/SKILL.md) | Reviews a proposed workflow edit against the signed chart before the live graph is changed. |
| [Hand-off QC](hand-off-qc/SKILL.md) | Checks a handoff for missing decisions, stale instructions, and steps the next person cannot run. |

## Build, Prompts, And Cost

| Skill | What it does |
| --- | --- |
| [Workflow intake](../../skills/clay-workflow-intake/SKILL.md) | Collects grain, trigger, destinations, branches, and write policy before a workflow blueprint is drafted. |
| [Workflow blueprint planner](../../skills/clay-workflow-blueprint-planner/SKILL.md) | Turns that brief into a workflow blueprint with triggers, nodes, routes, and acceptance checks. |
| [Workflow action planner](../../skills/clay-workflow-action-planner/SKILL.md) | Maps each tool or agent node to a concrete Clay action and records any unresolved action or model id. |
| [Autonomous builder](../../skills/clay-workflow-autonomous-builder/SKILL.md) | Applies a valid blueprint through the Clay CLI and reads the graph back, without deleting or publishing on its own. |
| [Build reviewer](../../skills/clay-workflow-build-reviewer/SKILL.md) | Compares the built graph with the plan for broken bindings, missing outcomes, draft-versus-live confusion, and credit exposure. |
| [Run and publish planner](../../skills/clay-workflow-run-and-publish-planner/SKILL.md) | Sets sample size, credit ceilings, external-write gates, and the publish approval before a run or a publish. |
| [Prompt authoring](clay-prompt-authoring/SKILL.md) | Drafts a Claygent prompt with Ethan, runs the adversarial pass, and keeps the prompt in draft until the fixture runs pass. |
| [Quality assessment](clay-quality-assessment/SKILL.md) | Scores Clay outputs against the expected fields and evidence, and separates a wording note from a failed result. |
| [Formulas](clay-formulas/SKILL.md) | Writes Clay formulas for gates and cleanup so a known rule does not become an agent call. |
| [Workflows CLI](workflows-cli/SKILL.md) | Runs graph, node, trigger, and code commands through `clay workflows` instead of the Clay UI. |
| [Optimize credits](workflows-optimize-credits-cli/SKILL.md) | Finds the expensive nodes and replaces an LLM step with a cheaper deterministic check when the rule is already known. |
| [Simplify](workflows-simplify-cli/SKILL.md) | Merges redundant nodes and cuts steps that do not change the business outcome. |
| [Platform troubleshooting](clay-platform-troubleshooting/SKILL.md) | Diagnoses a failed Clay run from the trace and names the platform limit before changing the play. |

## Page, Slide, And Campaign

| Skill | What it does |
| --- | --- |
| [Notion one-pager](../notion/SKILL.md) | Writes or refreshes the internal five-section Notion page once the node chart is signed, on the same page every later phase. |
| [Slide](../slide/README.md) | Generates the ClayDR enablement slide from the overview's Slide section. |
| [Slide making](slide-making/SKILL.md) | Lays out a Clay deck when the deliverable is more than the single enablement slide. |
| [Campaign setup](../campaigns/README.md) | Makes the Gong folder, both flows, and the Salesforce campaigns in the background after the overview is signed. |
