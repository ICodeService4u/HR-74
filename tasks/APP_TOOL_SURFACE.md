# The platform's tool surface for HR 74, read off the first run set of 09/19/2026

Captured from the `toolbelt_list_tools` result in trajectory `traj_6a2b124f473f458596a5e87edd35a399`
(GPT Sol 5.6, run O1), identical across the nine exports of 09/19/2026. Platform
`Ergon - bamboohr + greenhouse + wiki_js (MCP, auto)`, agent `React Toolbelt Agent (500 steps)`.
The agent starts with a toolbelt of helper tools and pulls each app tool in with
`toolbelt_add_tool` before calling it. A tool is tagged (write) when it changes app or file
state and (read) otherwise; the tag is by name and is what T1's `check_tools()` parses.
HR 79's `APP_TOOL_SURFACE.md` is not in this repository, so the form here is the one the
check reads: one line a tool, the name in backticks, the tag in parentheses.

| App or family | Tools | Writers |
|---|---|---|
| bamboohr | 42 | 13 |
| calendar | 17 | 9 |
| excel | 31 | 27 |
| filesystem | 6 | 0 |
| greenhouse | 37 | 20 |
| mail | 7 | 4 |
| pdfs | 5 | 1 |
| powerpoint | 37 | 29 |
| stirrup | 2 | 0 |
| wiki_js | 39 | 20 |
| word | 31 | 18 |
| total | 254 | 141 |

## The page-create route, as the runs used it

`wiki_js_mcp_wikijs_mcp_create_page` takes one `request` object: `title`, `path` and `content`
required; `description`, `editor` (default markdown), `is_published` (default true),
`is_private` (default false), `locale` (default en) and `tags` optional. It returns
`{"success": true, "page_id": N, "path": ...}`. Nine of nine runs created both pages with it,
ids 11 and 12 after the ten seed pages, every title exact, published by default, path chosen
by the run: seven used the slug of the title, two prefixed it with `operating-review/`.
One run corrected its second page with `wiki_js_mcp_wikijs_mcp_update_page` by id. No run
saved a draft, and no run used the HTML editor. `wiki_js_mcp_wikijs_mcp_get_page` reads a page
back by id with `title`, `path`, `description`, `content` and `isPublished`, which is the
route every run used to verify its own write.

## The catalogue

### bamboohr

- `bamboohr_bamboo_datasets_get_field_options` (read)
- `bamboohr_bamboo_datasets_get_fields` (read)
- `bamboohr_bamboo_datasets_list` (read)
- `bamboohr_bamboo_datasets_query` (read)
- `bamboohr_bamboo_employees_create` (write)
- `bamboohr_bamboo_employees_get` (read)
- `bamboohr_bamboo_employees_get_company_info` (read)
- `bamboohr_bamboo_employees_get_directory` (read)
- `bamboohr_bamboo_employees_update` (write)
- `bamboohr_bamboo_meta_get_countries` (read)
- `bamboohr_bamboo_meta_get_field_options` (read)
- `bamboohr_bamboo_meta_get_fields` (read)
- `bamboohr_bamboo_meta_get_list_fields` (read)
- `bamboohr_bamboo_meta_get_states` (read)
- `bamboohr_bamboo_meta_get_users` (read)
- `bamboohr_bamboo_meta_update_field_options` (write)
- `bamboohr_bamboo_reports_get_custom_report` (read)
- `bamboohr_bamboo_reports_get_custom_reports` (read)
- `bamboohr_bamboo_reports_run_company_report` (read)
- `bamboohr_bamboo_reports_run_custom_report` (read)
- `bamboohr_bamboo_reset_state` (write)
- `bamboohr_bamboo_search_employees` (read)
- `bamboohr_bamboo_search_metadata` (read)
- `bamboohr_bamboo_search_time_off` (read)
- `bamboohr_bamboo_time_off_assign_policy` (write)
- `bamboohr_bamboo_time_off_create_policy` (write)
- `bamboohr_bamboo_time_off_create_request` (write)
- `bamboohr_bamboo_time_off_create_type` (write)
- `bamboohr_bamboo_time_off_estimate_future_balances` (read)
- `bamboohr_bamboo_time_off_get_balances` (read)
- `bamboohr_bamboo_time_off_get_employee_policies` (read)
- `bamboohr_bamboo_time_off_get_policies` (read)
- `bamboohr_bamboo_time_off_get_requests` (read)
- `bamboohr_bamboo_time_off_get_types` (read)
- `bamboohr_bamboo_time_off_get_whos_out` (read)
- `bamboohr_bamboo_time_off_update_balance` (write)
- `bamboohr_bamboo_time_off_update_request_status` (write)
- `bamboohr_clear_database` (write)
- `bamboohr_export_csv` (write)
- `bamboohr_import_csv` (write)
- `bamboohr_list_tables` (read)
- `bamboohr_server_info` (read)

### calendar

- `calendar_v2_batch_create_events` (write)
- `calendar_v2_batch_delete_events` (write)
- `calendar_v2_check_availability` (read)
- `calendar_v2_count_events` (read)
- `calendar_v2_create_event` (write)
- `calendar_v2_delete_event` (write)
- `calendar_v2_duplicate_event` (write)
- `calendar_v2_export_ics` (write)
- `calendar_v2_get_calendar_info` (read)
- `calendar_v2_import_ics` (write)
- `calendar_v2_list_calendars` (read)
- `calendar_v2_list_events` (read)
- `calendar_v2_list_events_by_date_range` (read)
- `calendar_v2_move_event` (write)
- `calendar_v2_read_event` (read)
- `calendar_v2_search_events` (read)
- `calendar_v2_update_event` (write)

### excel

- `excel_v2_add_content_text` (write)
- `excel_v2_add_tab` (write)
- `excel_v2_append_sheets` (write)
- `excel_v2_copy_tab` (write)
- `excel_v2_create_chart` (write)
- `excel_v2_create_spreadsheet` (write)
- `excel_v2_delete_content_cell` (write)
- `excel_v2_delete_spreadsheet` (write)
- `excel_v2_delete_tab` (write)
- `excel_v2_edit_spreadsheet` (write)
- `excel_v2_export_to_csv` (write)
- `excel_v2_fill_formula` (write)
- `excel_v2_filter_tab` (write)
- `excel_v2_find_and_replace` (write)
- `excel_v2_insert_delete_columns` (write)
- `excel_v2_insert_delete_rows` (write)
- `excel_v2_list_files` (read)
- `excel_v2_list_tabs_in_spreadsheet` (read)
- `excel_v2_merge_sheets` (write)
- `excel_v2_pivot_table` (write)
- `excel_v2_read_csv` (read)
- `excel_v2_read_tab` (read)
- `excel_v2_remove_duplicates` (write)
- `excel_v2_reorder_columns` (write)
- `excel_v2_sort_tab` (write)
- `excel_v2_split_sheet_by_value` (write)
- `excel_v2_summarize_tab` (write)
- `excel_v2_text_to_columns` (write)
- `excel_v2_transform_column` (write)
- `excel_v2_transpose` (write)
- `excel_v2_unpivot` (write)

### filesystem

- `filesystem_get_directory_tree` (read)
- `filesystem_get_file_metadata` (read)
- `filesystem_list_files` (read)
- `filesystem_read_image_file` (read)
- `filesystem_read_text_file` (read)
- `filesystem_search_files` (read)

### greenhouse

- `greenhouse_activity_get` (read)
- `greenhouse_applications_advance_stage` (write)
- `greenhouse_applications_create` (write)
- `greenhouse_applications_get` (read)
- `greenhouse_applications_hire` (write)
- `greenhouse_applications_list` (read)
- `greenhouse_applications_reject` (write)
- `greenhouse_candidates_add_note` (write)
- `greenhouse_candidates_add_tag` (write)
- `greenhouse_candidates_create` (write)
- `greenhouse_candidates_get` (read)
- `greenhouse_candidates_search` (read)
- `greenhouse_candidates_update` (write)
- `greenhouse_clear_database` (write)
- `greenhouse_departments_list` (read)
- `greenhouse_export_csv` (write)
- `greenhouse_export_snapshot` (write)
- `greenhouse_feedback_list` (read)
- `greenhouse_feedback_submit` (write)
- `greenhouse_import_csv` (write)
- `greenhouse_jobboard_apply` (write)
- `greenhouse_jobboard_create_post` (write)
- `greenhouse_jobboard_list_jobs` (read)
- `greenhouse_jobs_create` (write)
- `greenhouse_jobs_get` (read)
- `greenhouse_jobs_get_stages` (read)
- `greenhouse_jobs_list` (read)
- `greenhouse_jobs_update` (write)
- `greenhouse_list_tables` (read)
- `greenhouse_offices_list` (read)
- `greenhouse_rejection_reasons_list` (write)
- `greenhouse_reset_state` (write)
- `greenhouse_server_info` (read)
- `greenhouse_sources_list` (read)
- `greenhouse_users_create` (write)
- `greenhouse_users_get` (read)
- `greenhouse_users_list` (read)

### mail

- `mail_forward_mail` (write)
- `mail_list_mails` (read)
- `mail_read_mail` (read)
- `mail_reply_all_mail` (write)
- `mail_reply_mail` (write)
- `mail_search_mail` (read)
- `mail_send_mail` (write)

### pdfs

- `pdfs_create_pdf` (write)
- `pdfs_read_image` (read)
- `pdfs_read_page_as_image` (read)
- `pdfs_read_pdf_pages` (read)
- `pdfs_search_pdf` (read)

### powerpoint

- `powerpoint_v2_add_animation` (write)
- `powerpoint_v2_add_comment` (write)
- `powerpoint_v2_add_image` (write)
- `powerpoint_v2_add_shape` (write)
- `powerpoint_v2_add_slide` (write)
- `powerpoint_v2_add_text_box` (write)
- `powerpoint_v2_add_transition` (write)
- `powerpoint_v2_apply_theme_color` (write)
- `powerpoint_v2_copy_slide` (write)
- `powerpoint_v2_create_deck` (write)
- `powerpoint_v2_delete_comment` (write)
- `powerpoint_v2_delete_deck` (write)
- `powerpoint_v2_delete_shape` (write)
- `powerpoint_v2_duplicate_deck` (write)
- `powerpoint_v2_edit_slides` (write)
- `powerpoint_v2_export_slide_as_image` (write)
- `powerpoint_v2_insert_chart` (write)
- `powerpoint_v2_insert_chart_from_data` (write)
- `powerpoint_v2_insert_table` (write)
- `powerpoint_v2_list_files` (read)
- `powerpoint_v2_merge_decks` (write)
- `powerpoint_v2_modify_image` (read)
- `powerpoint_v2_modify_shape` (read)
- `powerpoint_v2_modify_text_box` (read)
- `powerpoint_v2_move_slide` (write)
- `powerpoint_v2_read_completedeck` (read)
- `powerpoint_v2_read_image` (read)
- `powerpoint_v2_read_individualslide` (read)
- `powerpoint_v2_read_slides` (read)
- `powerpoint_v2_remove_animation` (write)
- `powerpoint_v2_rename_deck` (write)
- `powerpoint_v2_reorder_shape` (write)
- `powerpoint_v2_reorder_slides` (write)
- `powerpoint_v2_set_background` (write)
- `powerpoint_v2_set_slide_layout` (write)
- `powerpoint_v2_set_slide_notes` (write)
- `powerpoint_v2_set_slide_size` (write)

### stirrup

- `stirrup_code_execution_read_image_file` (read)
- `stirrup_code_execution_run_shell` (write)

### wiki_js

- `wiki_js_mcp_wikijs_mcp_assign_user_to_group` (write)
- `wiki_js_mcp_wikijs_mcp_create_asset_folder` (write)
- `wiki_js_mcp_wikijs_mcp_create_comment` (write)
- `wiki_js_mcp_wikijs_mcp_create_group` (write)
- `wiki_js_mcp_wikijs_mcp_create_page` (write)
- `wiki_js_mcp_wikijs_mcp_create_user` (write)
- `wiki_js_mcp_wikijs_mcp_delete_asset` (write)
- `wiki_js_mcp_wikijs_mcp_delete_comment` (write)
- `wiki_js_mcp_wikijs_mcp_delete_group` (write)
- `wiki_js_mcp_wikijs_mcp_delete_page` (write)
- `wiki_js_mcp_wikijs_mcp_delete_user` (write)
- `wiki_js_mcp_wikijs_mcp_flush_page_cache` (write)
- `wiki_js_mcp_wikijs_mcp_get_group` (read)
- `wiki_js_mcp_wikijs_mcp_get_navigation` (read)
- `wiki_js_mcp_wikijs_mcp_get_page` (read)
- `wiki_js_mcp_wikijs_mcp_get_page_history` (read)
- `wiki_js_mcp_wikijs_mcp_get_page_tree` (read)
- `wiki_js_mcp_wikijs_mcp_get_site_info` (read)
- `wiki_js_mcp_wikijs_mcp_get_system_info` (read)
- `wiki_js_mcp_wikijs_mcp_get_user` (read)
- `wiki_js_mcp_wikijs_mcp_list_asset_folders` (write)
- `wiki_js_mcp_wikijs_mcp_list_assets` (read)
- `wiki_js_mcp_wikijs_mcp_list_auth_strategies` (read)
- `wiki_js_mcp_wikijs_mcp_list_comments` (read)
- `wiki_js_mcp_wikijs_mcp_list_groups` (read)
- `wiki_js_mcp_wikijs_mcp_list_locales` (read)
- `wiki_js_mcp_wikijs_mcp_list_pages` (read)
- `wiki_js_mcp_wikijs_mcp_list_tags` (read)
- `wiki_js_mcp_wikijs_mcp_list_users` (read)
- `wiki_js_mcp_wikijs_mcp_move_page` (write)
- `wiki_js_mcp_wikijs_mcp_render_page` (read)
- `wiki_js_mcp_wikijs_mcp_restore_page` (write)
- `wiki_js_mcp_wikijs_mcp_search_pages` (read)
- `wiki_js_mcp_wikijs_mcp_unassign_user_from_group` (write)
- `wiki_js_mcp_wikijs_mcp_update_comment` (write)
- `wiki_js_mcp_wikijs_mcp_update_group` (write)
- `wiki_js_mcp_wikijs_mcp_update_page` (write)
- `wiki_js_mcp_wikijs_mcp_update_user` (write)
- `wiki_js_mcp_wikijs_mcp_whoami` (read)

### word

- `word_v2_add_content_text` (write)
- `word_v2_add_image` (write)
- `word_v2_apply_formatting` (write)
- `word_v2_change_case` (write)
- `word_v2_comments` (read)
- `word_v2_copy_document` (write)
- `word_v2_create_document` (write)
- `word_v2_delete_content_text` (write)
- `word_v2_delete_document` (write)
- `word_v2_document_properties` (read)
- `word_v2_edit_content_text` (write)
- `word_v2_find_and_replace` (write)
- `word_v2_get_document_overview` (read)
- `word_v2_header_footer` (read)
- `word_v2_hyperlinks` (read)
- `word_v2_insert_break` (write)
- `word_v2_insert_content` (write)
- `word_v2_list_files` (read)
- `word_v2_list_formatting` (write)
- `word_v2_modify_image` (read)
- `word_v2_move_content` (write)
- `word_v2_page_margins` (read)
- `word_v2_page_orientation` (read)
- `word_v2_page_size` (read)
- `word_v2_paragraph_formatting` (write)
- `word_v2_read_document_content` (read)
- `word_v2_read_image` (read)
- `word_v2_remove_break` (write)
- `word_v2_table_formatting` (write)
- `word_v2_table_merge_cells` (write)
- `word_v2_table_rows_columns` (read)
