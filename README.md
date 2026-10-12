# Growth Play Kit

Everything a new growth play reuses, from the first question to the live workflow. It ships inside `clay-planning-system`, and growth-plays includes that repo as the pinned `kit/` submodule. When the lifecycle changes here, a pin bump brings the change to every play.

Plays, fixtures, and receipts stay in the growth-plays repo. This folder is the part every play shares.

## Structured Approach

Five steps. Ethan signs steps 1 and 2. Everything else runs on its own unless a step needs his approval.

1. **Overview**: define the play's objective, operator, eligible and excluded audiences, timely trigger, stopping rules, destinations, external writes, and success criteria, then have two critics challenge the logic before Ethan signs and locks the scope.
2. **Node Chart**: translate the signed business logic into a fully named Clay workflow graph that shows every decision, branch, stop, input, output, global block, test safeguard, and external write before Ethan signs the build contract.
3. **Test Data**: gather real records for every branch and stopping outcome, record the expected result for each one as a fixture, and verify that the data, agent examples, and test destinations are ready before any node is built.
4. **Build**: start a fresh builder from only the signed packet, implement and test the workflow one block at a time, verify each connected path, and have an independent QC agent record the evidence while pausing only for prompt or external-write approvals.
5. **Confirm**: run every branch against the real test fixtures, review measured cost and all saved outputs, attack the completed build with three independent model families, fix material findings, and publish only after Ethan gives final approval.

After launch, a retro turns each lesson into a checklist line or a block-card change, so the next play starts ahead.

The full walk is [`lifecycle/build-cycle.md`](../lifecycle/build-cycle.md). The gate out of each step is [`lifecycle/phase-gates.md`](../lifecycle/phase-gates.md).

## Create Play Overview Notion Doc

Made when the node chart is signed, without being asked. Later steps update the same page. Five sections: Overview, How It Works, Sample Outputs, Success Criteria, Reference And Considerations. Example: [Closed-Lost Re-engage](https://app.notion.com/p/3f47e66eb0148101ae57ed0cbd10cc8d). Skill: [notion/](notion/SKILL.md).

## Generate Slide For ClayDR Enablement

One 16:9 slide per play: Who We Target, Talk Track, and Considerations. Who We Target is drawn from the signed overview. Talk Track and Considerations are Ethan's words, asked for at step 2. Generator: [slide/](slide/README.md).

## Sets Up SFDC Campaign In Background While You Work

Once the overview is signed, the agent makes the Gong folder and both flows (manual for Tier 1 and Tier 2, auto for Tier 3), then submits the Typeform that creates the Salesforce campaigns. The only question is the play title. The node chart does not wait on it. The build does. Runbook: [campaigns/](campaigns/README.md).

## Naming And The Flow Chart

The chart is named and checked before Ethan sees it, and before any node is created in Clay. [chart/](chart/README.md) holds the rules.

1. **Node Naming**: give each business stage one number and its substeps and outcomes letters, and renumber the whole map together when a stage is split or merged.
2. **Node Design**: decide the business jobs first, so a gate, a cleanup, and a join are separate nodes instead of one broad step.
3. **Flow Chart**: draw the main path down, decisions as diamonds, stops to the left, orange only for writes outside Clay, and green only for Ethan's test blockers, then fail the page if a box hides a decision or a stop.
4. **Chart Writer And Critic**: one agent drafts the chart from the signed overview and the global blocks, and a second agent attacks it before the page is opened for signature.
5. **Native Layout Check**: after the nodes exist in Clay, confirm the wires from the actual ports, because a saved coordinate is not proof the canvas is readable.

## Skills

The skills a play build loads are indexed in [skills/](skills/README.md): adversarial review, GTM and Clay workflow QC, prompt authoring, the Clay workflow CLI, credit and simplification passes, formulas, and the Notion page and slide. The workflow intake, blueprint, builder, and reviewer skills already live in this repo under `skills/`.

## Global Blocks

Pieces every play reuses the same way, so no play rediscovers them: Suppression, Best Ranked Contacts, Route & Score, Gong Enrollment, Action Queue, GTME Copilot Post, Campaign Member, Write Failure, and Test Mode. Each card says what is fixed and what a play fills in. Cards: [blocks/](blocks/README.md).

## Safety Built In

- **Test Mode**: every test sends to Ethan's test seats, never to the real person.
- **Email QC**: after every test send, the exact sent email is checked as the prospect would read it before the next round.
- **Write Gates**: Salesforce, Gong, Terra, Slack, and Notion writes stay off until approved. Nothing publishes without Ethan's approval.

## How An Update Lands

1. Change a card, the skill, the slide, or the campaign runbook in this repo and commit it here.
2. Push this repo.
3. In growth-plays, bring the pin forward with `python3 kit/lifecycle/doctor.py update plays/<play>`.

Until that pin moves, growth-plays still reads `building-blocks/global/`, `templates/growth-play-slide/`, and the installed Notion skill.
