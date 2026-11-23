# SixthPlanet — WAR 3.0: Большие войны цивилизаций

Status: implementation plan; Phase 0 audit required before gameplay changes
Target branch: `feature/war-3-massive`
Base branch: `feature/living-world-massive`
Scope: Massive
Product rule: extend existing SixthPlanet systems; do not replace the game's identity, mechanics, save data, UI language or art direction.

## Vision

Make faction conflict a persistent, systemic part of the living world. AI civilizations should be able to develop grievances, prepare for war, mobilize forces, campaign, fight, besiege settlements, negotiate and recover. Wars must emerge from and feed back into diplomacy, population, economy, settlements, routes and world events.

The player may influence the world but should not need to manually trigger every AI decision.

## Non-negotiable integration rules

1. Audit the current code before implementing. The existing main game is reported to live in `game.html`; confirm current paths and code structure on this branch.
2. Reuse existing faction, diplomacy, settlement, colonist, inventory/resource, map, time, combat and event systems wherever present. Never create parallel sources of truth.
3. Do not rewrite the main game file wholesale. Make small, reviewable, staged changes.
4. Preserve current gameplay, tutorial, achievements, menus, responsive layout and visual style.
5. Use the authoritative simulation clock. Pause and speed controls must affect war simulation consistently.
6. Additive, versioned save migration only. Existing saves must continue to load.
7. Stable IDs for factions, armies, battles, sieges and war events.
8. UI displays simulation state; state transitions happen in simulation logic, not ad-hoc UI handlers.
9. AI and battle calculations must be budgeted and deterministic from the world seed where practical.
10. No patch notes, website publication or release claims until the feature is implemented and tested.

## Phase 0 — Codebase audit and compatibility

- Map the actual files and functions for game state, faction/diplomacy, settlement ownership, colonists/squads, combat, resources, world map, event log, save/load and simulation tick.
- Identify whether tactical combat exists and whether it can be reused. If absent, define an abstract battle resolver that respects current character stats and equipment.
- Record current save schema and implement/test a migration proposal before adding persistent war fields.
- Identify the existing UI components, styles, mobile breakpoints and notification pattern.
- Produce a concrete integration map naming existing functions and exact extension points.
- Add a regression checklist for new game, old save, reload, pause, speed controls and mobile UI.

Acceptance:
- Existing save loads without loss or reset.
- New save initializes valid empty war state.
- No duplicate timers or competing simulation clocks.
- Existing gameplay remains unchanged when no war is active.

## Phase 1 — War domain model

Introduce only the minimum new persistent records required, adapting names to existing conventions:

- wars: stable ID, attacker/defender IDs, casus belli/reason, start tick, status, war goals, participants, score and history references.
- armies: stable ID, owner faction, commander/leader if supported, unit/member references, location/route, strength, morale, supplies, movement state and current orders.
- battles: stable ID, war ID, location, participants, start/end tick, inputs, outcome, casualties and event reference.
- sieges: stable ID, war ID, besieging army, settlement, defenders, progress, blockade/supply state and status.
- occupations/control changes: settlement or region, previous owner, new controller, cause, start tick and resolution state.
- war event records: tick, type, participants, location, cause and outcome.

Do not duplicate colonists, inventory, faction identity, settlement ownership or world event records if those already exist.

Acceptance:
- All records use stable IDs and validate references.
- Empty/default state is safe for old saves.
- Save/load round-trip preserves active and completed conflicts.

## Phase 2 — Strategic AI and causes of war

- Derive potential conflicts from existing relations, grievances, territory/resource interests, faction goals and recent events.
- Add an explicit preparation phase: mobilization, treasury allocation, recruitment or squad assembly only through existing systems.
- Add declaration rules and cooldowns to prevent constant war flipping.
- Support defensive alliances and allied entry only if the current diplomacy model can represent them cleanly.
- Make AI consider relative strength, supply, distance, active wars and internal stability.
- Expose clear reasons for declarations and peace decisions in the event log.

Acceptance:
- AI can declare a justified war and explain why.
- AI avoids impossible or endlessly repeated declarations.
- Existing diplomacy actions continue to work.

## Phase 3 — Armies, movement and strategic orders

- Build armies from existing squads/colonists/units; do not invent a second population.
- Support rally, defend, patrol, march, reinforce, retreat and disband orders where compatible.
- Use existing world routes/map if available; otherwise integrate movement with the smallest possible extension.
- Movement consumes time and supplies; dangerous routes can trigger encounters.
- Prevent duplicated units, double assignment and impossible simultaneous orders.
- Abstract distant/off-screen movement to reduce CPU cost.

Acceptance:
- Armies travel between valid locations, persist through reload and respond to pause/speed.
- Units cannot belong to two active armies at once.
- Interrupted movement resolves safely.

## Phase 4 — Battles and aftermath

- Use existing tactical combat if it exists; otherwise implement a deterministic abstract resolver.
- Inputs: unit count/composition, existing stats/skills/equipment, commander bonuses if supported, morale, supplies, terrain and fortification.
- Outcomes: victory, defeat, retreat, casualties, injuries, equipment/resource losses and prisoners only if supported by current game systems.
- Avoid instant annihilation and make battle reports explain decisive factors.
- Record each battle exactly once.

Acceptance:
- Same seeded inputs produce reproducible results.
- Losses are applied once and correctly to existing units/inventory.
- Battle outcome affects war score, morale, relations and local control.

## Phase 5 — Sieges and settlement control

- Armies can besiege eligible settlements and establish a blockade.
- Siege progress depends on defenders, fortifications, supplies, time and relief forces.
- Defenders can hold, negotiate, sally or be relieved where supported.
- Storming is a distinct high-risk resolution, not an automatic capture.
- Settlement ownership changes through one authoritative ownership transition.
- Occupation may be temporary; resistance, liberation or negotiated transfer can resolve it.
- Destruction/damage must use existing building/site systems; do not fabricate building damage where none exists.

Acceptance:
- A settlement can be defended, besieged, relieved and captured.
- Ownership, population, stocks and faction relations remain consistent.
- No duplicate settlement or orphaned population records.

## Phase 6 — Logistics, economy and civilian consequences

- Armies consume existing food/resources and ammunition only if ammunition exists in the current resource catalog.
- Supply routes use existing trade/route systems; blockades affect them through shared state.
- War spending affects existing faction treasury/economy, if present.
- Shortages can lower morale and force retreat; avoid hard-locking the player colony.
- Civilian harm, refugees or displacement are optional only if compatible with existing population/location models.
- All resource transactions are atomic and logged once.

Acceptance:
- No resource duplication or negative-stock exploits.
- Supply shortage has understandable effects.
- Existing colony survival systems remain functional during war.

## Phase 7 — Diplomacy, peace and post-war state

- Peace proposals, ceasefire and surrender.
- War goals determine valid settlement terms.
- Terms may include status quo, tribute/reparations, territory transfer or liberation only when supported by existing economy/territory systems.
- Calculate war exhaustion/war score from meaningful events, not elapsed time alone.
- Apply treaty and ownership changes once.
- Add post-war cooldowns and recovery effects.

Acceptance:
- War can end through negotiated peace, surrender or another explicit valid condition.
- Terms are visible before acceptance.
- Faction relations and territorial state update consistently.

## Phase 8 — Player UX, balancing and release

- Add a Wars/Conflicts panel using the current SixthPlanet UI patterns.
- Conflict overview: parties, cause, goals, duration, strength, score and status.
- Army details: location, composition, commander, morale, supplies and orders.
- Battle and siege reports with clear outcomes.
- Strategic map overlays only if the existing map supports them; mobile-first controls and readable fallback list.
- Notifications are prioritized and configurable if needed.
- Add contextual tutorial hints, not a separate replacement tutorial.
- Test long-running simulation, multiple simultaneous wars, old saves, new saves, reloads, pause/speed and mobile layout.
- Update in-game version/changelog and main website patch journal only after verified implementation and gameplay testing.

Acceptance:
- Player can understand who is fighting, why, where and with what consequences.
- UI remains usable on mobile and desktop.
- No critical errors, duplicate events, save corruption or runaway AI loops.
- Release notes describe only features that are actually present.

## Recommended implementation order

1. Phase 0 audit.
2. Phase 1 war records and save migration.
3. Phase 2 AI war decisions.
4. Phase 3 armies and movement.
5. Phase 4 battle resolver.
6. Phase 5 sieges and capture.
7. Phase 6 logistics.
8. Phase 7 peace.
9. Phase 8 interface, balance and release.

Build each phase as a playable vertical slice with tests before proceeding. Do not attempt all systems in one giant edit.

## Test matrix

- Fresh game / legacy save / save after migration.
- Save-load during mobilization, march, battle, siege and peace negotiation.
- Pause and every supported simulation speed.
- One war / multiple wars / allied participants / faction eliminated.
- Army with missing leader / insufficient supplies / invalid route.
- Settlement owner changes / liberation / interrupted siege.
- Resource shortage / blockade / route reopening.
- Mobile narrow viewport / desktop viewport.
- Long simulation with many factions and no duplicate event generation.

## First deliverable

Complete Phase 0 and publish a code-grounded audit report in this repository before changing gameplay code. The report must name actual files/functions, current systems to reuse, migration details, implementation touchpoints and regression tests. If repository access or file retrieval prevents verification, record that limitation instead of guessing.
