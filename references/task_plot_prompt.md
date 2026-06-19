Use case: infographic-diagram
Asset type: TaskBeacon task flow diagram
Primary request: Create a clean, publication-ready task flow diagram as a timeline collection for the behavioral task described below.

Task: Balloon Analogue Risk Task (BART)
Construct: risk taking / decision making
Rows/conditions:
- Blue balloon: lower reward, +5 per pump, max pump profile 24
- Yellow balloon: medium reward, +10 per pump, max pump profile 12
- Orange balloon: higher reward, +20 per pump, max pump profile 6

Timeline phases:
- Blue balloon: Fixation (+; 0.8 s; no response) -> Decision (blue balloon + score; press space pump or right cash) -> Pump loop (space; balloon grows; +5; repeat until cash or pop) -> Outcome (Cash: bank score OR Pop: lose trial score; 1.0 s) -> Feedback (earned score; 1.0 s)
- Yellow balloon: Fixation (+; 0.8 s; no response) -> Decision (yellow balloon + score; press space pump or right cash) -> Pump loop (space; balloon grows; +10; repeat until cash or pop) -> Outcome (Cash: bank score OR Pop: lose trial score; 1.0 s) -> Feedback (earned score; 1.0 s)
- Orange balloon: Fixation (+; 0.8 s; no response) -> Decision (orange balloon + score; press space pump or right cash) -> Pump loop (space; balloon grows; +20; repeat until cash or pop) -> Outcome (Cash: bank score OR Pop: lose trial score; 1.0 s) -> Feedback (earned score; 1.0 s)

Visual requirements:
- White background, landscape orientation, crisp dark text, restrained condition accent colors.
- One horizontal row per condition or representative trial type.
- Each row contains 5 participant-screen snapshots connected by a subtle arrow.
- Each screen snapshot shows the visible stimulus or feedback, not internal variable names.
- Use gray participant-screen boxes, thin black arrows, consistent row spacing, and subtle row separators.
- Use a small loop marker around the pump phase to show repeated pumping.
- Show the outcome phase as a compact branch inside one snapshot: Cash / Pop.
- Place timing labels under each screen in compact text.
- Place condition labels at the left of each row.
- Use short labels only; avoid paragraphs inside the image.
- Make all text legible at normal document preview size.
- Leave a clean blank header band across the top 15-18% of the image. This band is reserved for a fixed title, `Construct: ...` subtitle, and TaskBeacon logo lockup that will be added after generation.

Accuracy constraints:
- Do not invent phases, stimuli, condition names, keys, rewards, or timings.
- Do not add people, lab equipment, decorative scenes, logos, or unrelated icons.
- Do not draw the task title, construct subtitle, any logo, watermark, brand mark, or `TaskBeacon` text inside the generated image.
- Draw only the timeline content below the blank header band.
- If a detail is unknown, omit it rather than guessing.
- Preserve these exact terms where used: BART, Blue, Yellow, Orange, space, right, +5, +10, +20, max 24, max 12, max 6, 0.8 s, 1.0 s, Cash, Pop, Feedback.
- Show `space` as pump and `right` as cash out.

Style:
TaskBeacon scientific infographic style: clean vector-like raster image, organized spacing, gray screen boxes, restrained color accents, and a blank header-safe area.
