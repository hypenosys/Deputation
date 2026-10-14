# THE DEPUTATION — Narrative Voice and Flavor Bible v0.1

**Genre:** *horror administrativo sobrio con ironía seca y un fondo trágico*. Not a sketch comedy or a police conspiracy thriller. The institution does not need a villain: a plausible chain of small, defensible refusals can produce an indefensible outcome. Moments of quiet procedural competence should give relief. The player is not mocked for seeking clarification.

## Premise

Iria Valls, hired on a temporary investigative assignment, must reconcile two mutually inconsistent records before EXP-0042 is closed. A document says a neighborhood's appeals have been processed; a second record may show they were never admitted. She can visit Courtyard, Registry and Archive; request case-scoped permission; gather admissible evidence; and validate a discrepancy under a **30-minute simulated procedural window**. An internal deadline does not erase truth, but it can make truth administratively useless.

There is no heroic hacker bypass, no omniscient villain and no supernatural entity in M1. The antagonist is the asymmetry between **what occurred, what can be proved and what officials are permitted to acknowledge**. A grant of authorization means something materially useful; a refusal always tells the player what can be corrected. The risk of failure is social: a case may close unchallenged while the people affected receive a form letter declaring there was no irregularity.

## Narrative voices

| Person | Role and motivation | Speech rule |
| --- | --- | --- |
| **Iria Valls** | Player investigator; wants a document trail admissible before time expires | Brief internal notes, never fabricates a truth the player has not observed |
| **Elena Robles** | Secretary; wants a defensible authorization ledger so she is not blamed for an illegal disclosure | Precise, polite, procedural; can grant a narrow permission but not general access |
| **Marcel Vidal** | Archivist; wants preservation and chain of custody respected | Concise, dry; speaks in dates, shelf references, and conditions |
| **Núria Soler** | Registry clerk; wants to process requests while a system intermittently fails | Short, weary, humane; reports observable incidents rather than secret motives |
| **Damià Ferrer** | Case supervisor; fears a visible audit failure more than a private error | Administrative euphemisms; never omniscient |
| **Affected families** | Absent at the counter but present through the consequences of the file | Never reduced to expendable quest loot; no invented private details in status feedback |

All names/roles are fictional. Actor motivation is **authored context**, not implemented NPC social AI.

## Sample prose: legal clarity with unsettling implication

- **Case file, first read:** “EXP-0042. Entrada recibida. Asiento válido. Motivo de revisión: dos fechas de recepción no coinciden. La discrepancia consta; su significado, no.”
- **Elena, request denied `MISSING_CASE_BASIS`:** “Puedo autorizar un expediente. No puedo autorizar una intención. Traiga primero la carátula del caso.”
- **Elena, permission granted:** “Autorizado para EXP-0042. Este sello no abre ningún otro archivo.”
- **Marcel, archive not ready `INVALID_CASE_STAGE`:** “Está aquí, sí. Pero todavía no está en revisión. Conservar algo no significa poder mostrarlo.”
- **Marcel, evidence disclosed:** “La hoja anterior dice que llegó el día 12. Esta dice que no llegó nunca. Ambas llevan sello.”
- **Iria, `MISSING_READY`:** “Tengo las piezas. No la constancia de que puedan encajar.”
- **Registry incident (M2 proposed, not ghost):** “La conexión funciona lo suficiente para emitir un error. No para registrar una solución.”
- **Success `CASE_VALIDATED`:** “EXP-0042. Discrepancia acreditada. El expediente permanece abierto a las consecuencias.”
- **Expiry `DEADLINE_EXPIRED`:** “Plazo vencido. El hecho no cambia. Su admisibilidad, sí.”

## Editorial rules

1. **Truth discipline:** never reveal another actor's motive as fact through a denial reason. Distinguish `observed`, `reported`, `inferred` and `officially recorded`.
2. **No comedy against vulnerable people.** Humor comes from forms, language and contradictions of authority.
3. **No fake ambiguity in actionable feedback:** flavor can be disturbing, but a denial must state who, why, remaining minutes and one viable next action.
4. **Small prose, long consequence:** keep dialogue to 1–2 lines in PETSCII target; longer text may be paginated voluntarily without costing simulation time.
5. **Three registers:** printed form (neutral), official dialogue (cautiously defensive), Iria's marginal notes (human, uncertain).
6. **Conditional scenes only:** authored flavor triggers require validated causal event IDs; presentation never grants permission or changes a case stage by itself.

## Emotional trajectory

Competence → friction → discovery → a costly correction → relief or irreversible closure. The game must present a meaningful choice before escalation, not trap the player with an unknowable rule.
