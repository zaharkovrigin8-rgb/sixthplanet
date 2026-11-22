# SixthPlanet — Living World (Massive Update)

Status: design and implementation plan  
Target branch: `feature/living-world-massive`  
Design pillars: RimWorld-style colony simulation + Kenshi-style autonomous open world.

## Product vision

The planet must continue to exist when the player is not looking at it. The player begins as a small settlement and can eventually become a regional power. Factions, settlements, caravans, trade, exploration, conflict and colony life must form one connected simulation. The update must extend the existing game rather than replace its identity, visual language, controls or established systems.

## Core gameplay loop

1. Keep the colony alive: food, water, shelter, health, morale and production.
2. Learn about the region: rumors, scouts, map discoveries and encounters.
3. Build relationships: trade, favors, treaties, reputation and rivalries.
4. Expand influence: establish outposts, secure routes and claim strategic sites.
5. Face consequences: shortages, raids, faction wars, shifting borders and diplomatic reactions.
6. Grow from a vulnerable settlement into a power that changes the regional balance.

## Systems and implementation phases

### Phase 0 — Compatibility and technical foundation
- Audit the current game state model, update loop, save/load flow, UI patterns and existing mechanics before changing gameplay.
- Record current save format and create a backward-compatible migration layer with a schema version.
- Add a single world simulation coordinator; avoid independent timers mutating shared state.
- Separate simulation data from rendering and UI.
- Add seeded random generation and reproducible simulation steps where practical.
- Add debug logging/diagnostics and a lightweight regression checklist.
- Preserve existing saves, tutorial, achievements, menus and the current visual style.

Acceptance: an existing save loads unchanged; a new save works; pause/speed controls remain correct; no duplicate world timers are created.

### Phase 1 — Faction simulation and diplomacy
- Introduce faction records: stable ID, name, identity, color/emblem, leader, home settlement, population/strength, treasury, needs, goals and disposition.
- Track bilateral relations, reputation, trust, fear, grievances and active treaties.
- Actions change relations: trade, aid, trespass, theft, attacks, completing contracts and defending allies.
- Diplomacy actions: establish contact, trade agreement, non-aggression pact, alliance, tribute/demand and declare war.
- AI faction goals: survive, expand, secure resources, retaliate, trade or weaken a rival.
- Show faction dossier, relations and a readable event history.

Acceptance: at least three AI factions have distinct goals; relations change from player actions and AI events; treaties have clear effects and can expire or be broken.

### Phase 2 — Regional world map and territorial control
- Add a strategic map with discovered/undiscovered locations, terrain, routes and faction borders.
- Location types: settlements, outposts, ruins, resource sites, hazards and points of interest.
- Store ownership, controlling faction, local danger, resources, population and strategic value.
- Borders change only through explicit simulation events: founding, conquest, abandonment, treaty or uprising.
- Fog of war: unknown locations become known through exploration, scouts, travelers and purchased information.
- Map UI must be usable on mobile and desktop.

Acceptance: locations persist in saves; exploration reveals information; ownership changes are visible and logged.

### Phase 3 — Expeditions, squads and caravans
- Create expedition parties from available colonists, with supplies, equipment, leader and destination.
- Model travel time, route danger, fatigue, provisions, encounters and return journey.
- Expeditions can scout, explore ruins, gather, rescue survivors, negotiate, trade and establish outposts.
- Caravans move between settlements and carry goods; routes can be threatened or blockaded.
- Encounters resolve through meaningful choices, skills, equipment and faction relations.
- Provide clear departure, travel, encounter and return reports.

Acceptance: a party can leave, travel, encounter events, consume supplies and return with persistent results; interrupted or failed expeditions do not duplicate or lose units.

### Phase 4 — Colonist depth and social simulation
- Extend existing colonists rather than replacing them: personality traits, skills, needs, health, relationships and memories.
- Add social links: friendship, rivalry, family/romance only if compatible with the game's tone and current systems.
- Morale responds to food, safety, work, victories, losses, living conditions and social events.
- Jobs and roles influence colony production and expedition effectiveness.
- Events should be legible and avoid excessive notification spam.

Acceptance: colonist traits affect behavior/outcomes; social and morale changes persist; existing colonists and saves remain valid.

### Phase 5 — Economy, production and trade
- Define a canonical resource catalog and item valuation; avoid duplicate resource definitions.
- Each settlement has stocks, production, consumption, needs and treasury.
- Trade prices respond to scarcity, abundance, danger, distance and faction relations, with sensible bounds.
- Add contracts: deliver goods, escort a caravan, supply an ally, recover an item or provide aid.
- Trade routes can become unsafe; shortages can affect settlement behavior and diplomacy.
- Make every transaction auditable in the event log.

Acceptance: trade changes inventories and currency exactly once; prices respond to supply/demand; contracts have deadlines, rewards and failure consequences.

### Phase 6 — Conflict, raids and territorial expansion
- Distinguish hostility, raids, skirmishes, sieges and full faction wars.
- Threat depends on local power, faction goals, relations, route access and recent events.
- Add warning/intelligence signals so attacks are not arbitrary.
- Resolve battles using squad strength, skills, equipment, terrain, supplies and morale; use existing tactical combat if present.
- Outcomes: casualties, prisoners if supported, loot, damaged sites, tribute, occupation, liberation or border changes.
- Add defensive structures/outposts only where compatible with the current building system.

Acceptance: wars have causes and consequences; a settlement can defend itself; victory/defeat changes relations, resources or control in a persistent, understandable way.

### Phase 7 — UX, onboarding, balance and release
- Add a World/Factions screen, map overlays, expedition panel, diplomacy panel and event log using existing UI conventions.
- Teach the new systems through contextual tutorial steps, not a wall of text.
- Add settings for simulation intensity/notifications if performance requires it.
- Balance resource flow, travel times, AI aggression and event frequency.
- Test mobile layout, desktop layout, save migration, long-running simulation and reload behavior.
- Update the in-game version/changelog and website update notes only after implementation is stable.

Acceptance: each new system can be discovered in-game; no critical overflow or blocked controls on mobile; long sessions remain stable; release notes match actual behavior.

## Shared data model (proposed)

- `world`: schemaVersion, seed, simulationTick, locations, routes, discoveredLocationIds.
- `factions`: stable IDs and faction state.
- `relations`: normalized faction-pair records with score, trust, grievances and treaties.
- `settlements`: owner, population, stocks, production, consumption, treasury and defenses.
- `expeditions`: party IDs, origin, destination, route, supplies, progress, status and current encounter.
- `caravans`: route, cargo, guards, progress and status.
- `contracts`: issuer, objective, deadline, reward, status and outcome.
- `worldEvents`: timestamp/tick, type, participants, location, cause and outcome.

Exact field names and integration points must be adapted to the existing code after the Phase 0 audit. Do not duplicate existing colonist, inventory, time, map or event systems.

## Technical rules

1. One authoritative simulation clock; pause and speed controls apply to all world systems.
2. Stable IDs for factions, settlements, locations, parties and events.
3. All world changes go through explicit state transitions; UI must not mutate simulation state ad hoc.
4. Save migrations are additive and versioned; unknown/missing fields receive safe defaults.
5. Simulation work is budgeted per tick; distant/off-screen activity can be abstracted without stopping the world.
6. Random outcomes use the world seed where possible, enabling reproducible bug reports.
7. Important events are recorded once and can be inspected by the player.
8. Feature flags or staged activation should allow systems to be tested independently.

## First implementation milestone

Complete Phase 0 before adding gameplay systems. Deliver:
- a codebase map and dependency notes;
- a save schema/migration proposal grounded in the current implementation;
- a list of existing systems to reuse;
- a prioritized integration plan with concrete files/functions;
- a regression checklist.

Then implement the faction data model and a minimal faction-status UI as the first playable vertical slice. Do not rewrite the main game file wholesale or remove existing mechanics.
