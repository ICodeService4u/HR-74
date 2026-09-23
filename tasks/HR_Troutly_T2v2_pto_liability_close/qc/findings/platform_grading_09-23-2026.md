# Row 1 on the platform, 09/23/2026 - what the graded dump holds

Row 1 was pasted alone, rows 2 to 13 left empty, and graded on a Gemini run.

## Measured

- **The AST gate.** The first paste was refused before it ran: `permanently banned import: os`.
  The engine imported os only to read a quiet flag. It imports json and re now, and the builder
  holds every row file to that allow-list with a control.
- **An empty code box stops the grading.** Rows 2 to 13 each read `missing check fn`, and the
  pane printed `Cannot compute score: 12 verifier(s) had errors`.
- **The dump carries no Wiki.js table.** Target database apps held both wiki services,
  `svc_4c45ff31af7f439fb8c7936f85f90964` and `svc_4a38acf9625d44b5a1aa6ba9fd6d1060`. Row 1's
  details listed 57 tables, every one BambooHR or Greenhouse:

  activities, application_answers, applications, audit_log, balance_adjustments,
  candidate_addresses, candidate_attachments, candidate_educations, candidate_email_addresses,
  candidate_employments, candidate_phone_numbers, candidate_social_media_addresses,
  candidate_tags, candidate_website_addresses, candidates, custom_field_values, custom_reports,
  degrees, departments, disciplines, emails, emergency_contacts, employee_policies, employees,
  hiring_team, interview_kit_questions, interview_step_default_interviewers, interview_steps,
  job_departments, job_offices, job_openings, job_post_question_options, job_post_questions,
  job_posts, job_stages, jobs, list_field_options, notes, offices, prospect_pool_stages,
  prospect_pools, rejection_reasons, schools, scorecard_attributes, scorecard_questions,
  scorecards, source_types, sources, tags, time_off_balances, time_off_policies,
  time_off_requests, time_off_types, user_departments, user_emails, user_offices, users

  No pages, pageHistory, comments or groups; tags and users are Greenhouse's. Row 1 read
  `no pages table in this snapshot`, `page_rows` 0, and failed.
- **The pane shows a verifier's stdout.** Every note the engine printed reached the pane.

## What it settles

The 09/21/2026 grading failed every wiki row and no BambooHR row because the dump never held
the wiki. It was not the service picked on the form and not `has_table`.

## What was done

With no pages table in the dump, the rows read the page off the run's own Wiki.js calls: the last
create or update under the title, or on the page's id, that the app answered with success, and
the app's own get_page reply. A refused call, another title, another page's id and the run's
prose are not read. Two pages created under the title fail, as on the table route. Where the dump
does hold a pages table, it decides and the record is not read. Fifteen scenarios and six
controls hold that route: 793 of 793 verdicts on 61 snapshots, 79 of 79 controls red. The row
files run to 231 to 234 lines, over the skill's 200; the builder's cap is 240, with the reason in
the builder.

## Still open

Whether a graded ctx carries `trajectory`, and in what shape. Row 1's details print
`trajectory: N messages, keys [...]` and `Wiki.js calls on the page: [...]`, so the next grading
says both. If it reads 0 messages, a code verifier cannot see the page, and the wiki rows belong
on the platform's Trajectory verifier, an LLM judge over the run's tool calls and outputs.
