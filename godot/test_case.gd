extends SceneTree
## Integration smoke: actual Godot GDScript state + desk scene, not Python.
const CaseState = preload("res://godot/case_state.gd")

func _check(condition: bool, description: String) -> bool:
	if not condition:
		printerr("GODOT_TEST_FAIL: " + description)
		quit(1)
	return condition

func _initialize() -> void:
	call_deferred("_exercise")

func _exercise() -> void:
	var s = CaseState.new()
	if not _check(s.result() == "ongoing" and s.minute == 0, "initial state"): return
	if not _check(s.command("move", "REGISTRY") == "MOVED" and s.minute == 2, "move +2"): return
	var denied_before: Dictionary = s.snapshot()
	if not _check(s.command("request_permit") == "MISSING_CASE_BASIS", "denied permit"): return
	if not _check(s.snapshot() == denied_before, "denial must not change state"): return
	if not _check(s.command("read_case_file") == "CASE_FILE_READ" and s.minute == 3, "case read"): return
	if not _check(s.command("request_permit") == "PERMIT_GRANTED" and s.has_permission, "case permit"): return
	if not _check(s.command("move", "ARCHIVE") == "MOVED" and s.minute == 7, "move +3"): return
	denied_before = s.snapshot()
	if not _check(s.command("read_archive") == "INVALID_CASE_STAGE", "early review denial"): return
	if not _check(s.snapshot() == denied_before, "early review rejection time unchanged"): return
	if not _check(s.command("wait", 3) == "WAITED" and s.stage == "archive_review", "m10 stage"): return
	if not _check(s.command("read_archive") == "ARCHIVE_READ" and s.minute == 11, "history read"): return
	if not _check(s.command("wait", 4) == "WAITED" and s.has_review, "m15 REVIEW"): return
	if not _check(s.command("wait", 12) == "WAITED" and s.has_ready, "m27 READY"): return
	if not _check(s.command("validate_case") == "CASE_VALIDATED", "case validation"): return
	if not _check(s.minute == 28 and s.result() == "validated", "validates in m28"): return
	denied_before = s.snapshot()
	if not _check(s.command("move", "REGISTRY") == "CASE_ALREADY_VALIDATED", "terminal case guard"): return
	if not _check(s.snapshot() == denied_before, "terminal refusal unchanged"): return
	if not _check(s.command("inspect_case_status") == "STATUS_VIEWED", "read-only status after closure"): return

	var fail = CaseState.new()
	if not _check(fail.command("move", "REGISTRY") == "MOVED", "failure case movement"): return
	if not _check(fail.command("read_case_file") == "CASE_FILE_READ", "failure case basis"): return
	if not _check(fail.command("request_permit") == "PERMIT_GRANTED", "failure case permit"): return
	if not _check(fail.command("move", "ARCHIVE") == "MOVED", "failure case archive"): return
	if not _check(fail.command("wait", 3) == "WAITED", "failure m10"): return
	if not _check(fail.command("read_archive") == "ARCHIVE_READ", "failure history"): return
	if not _check(fail.command("wait", 19) == "WAITED" and fail.result() == "expired", "expire at m30"): return
	denied_before = fail.snapshot()
	if not _check(fail.command("validate_case") == "DEADLINE_EXPIRED", "expiry refusal"): return
	if not _check(fail.snapshot() == denied_before, "expiry unchanged"): return

	var desk = load("res://godot/Desk.tscn").instantiate()
	root.add_child(desk)
	await process_frame
	var current: Dictionary = desk.model.snapshot()
	desk._on_layout(1)
	desk._on_layout(2)
	desk._on_layout(0)
	if not _check(desk.model.snapshot() == current, "layout switching must not mutate world"): return
	var count: int = desk.find_children("*", "Button", true, false).size()
	if not _check(count >= 13, "three tabs and ten action controls must render"): return
	print("GODOT_CASE_PASS: win=m28, loss=m30, denials idempotent, 3 view switches read-only, buttons=" + str(count))
	quit(0)
