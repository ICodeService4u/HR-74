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

## The second grading, the same day: the route measured

Row 1 with the trajectory route, pasted alone, rows 2 to 13 empty, graded on a Gemini run:

- The AST gate passed `import json`.
- A graded ctx carries `trajectory`: 96 messages, keys `content`, `function_call`,
  `reasoning_content`, `role`, `thinking_blocks`, `tool_call_id`, `tool_calls`. That is the
  export's message shape, which the scenarios use.
- `Wiki.js calls on the page: [('create_page', '11'), ('cp_get_page', 11)]`: a create under the
  title the app answered with success and page id 11, then the app's get_page reply for page 11.
  The label is the tool name's last eleven characters, so `get_page` prints as `cp_get_page`.
- `PASSED - published=True`, `page_rows` 1.

## The third grading, the same day: a figure row

Rows 1 and 2 on the same run. Row 1 passed again. Row 2 read the run's page off the same create and
get_page of page 11 and failed, correctly: the page states a total of $111,320.02 against
$92,739.54, and lines of $14,159.95, $52,936.57, $11,121.71, $10,957.01 and $22,144.78, with
1,757.87 hours. `figures_read` 16, `page_rows` 1. The figure reader works on the platform as it does
in the battery: the stated total is read, and the bare numbers in the title and purpose lines are
read too and match nothing. Rows 3 to 13 run the same code.
