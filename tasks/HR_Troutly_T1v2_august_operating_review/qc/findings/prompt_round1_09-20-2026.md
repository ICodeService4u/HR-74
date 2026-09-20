# Prompt AutoQC round 1 - 09/20/2026

Archived from the interface on 09/20/2026 by the package owner, verbatim but for the register:
the round's curly quotes and em dashes are ASCII here. One finding, marked major. It landed
before any v2 trajectory had, and the verifiers it read are the synth's twenty on the task
record, since the package's import is not loaded until the task data id is read off the first
export. The verdict is in `../README.md`.

## Outcome-Determining Choices Pinned in the Prompt (consolidated)

The prompt says to use "the BambooHR employee records" and the attached operating-review request
defines only that "A current employee is anyone employed by Troutly on 08/31/2026"; it never says
that the August 31 Master Employee Roster overrides BambooHR. BambooHR has 53 active
non-contractor employee records, including Piper Athanasoulis, Halston Perevalov, and Marguerite
Delacroix-Hahn, whereas the roster has 52 and instead includes Simone Okonkwo and Rafael Ibarra;
the verifier nevertheless requires "52 active employees" from that roster. Add an explicit source
hierarchy for the Staffed Role View - e.g., instruct that the August 31 Master Employee Roster is
authoritative for the employee population and BambooHR is only corroborative - to eliminate the
two defensible, differently scored outputs.
