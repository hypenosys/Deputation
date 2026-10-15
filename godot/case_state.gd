extends RefCounted
## Godot host-only EXP-0042 reference model. No Godot-to-ABBI parity claim.
## All world facts below come from res://data/world/vertical_slice.v1.json.
const DEADLINE: int = 30
const PERMISSION: String = "ARCHIVE_CASE_0042"

var minute: int = 0
var room: String = "COURTYARD"
var stage: String = "registered"
var has_basis: bool = false
var has_history: bool = false
var has_review: bool = false
var has_ready: bool = false
var has_permission: bool = false
var last_code: String = "BOOT"

var world: Dictionary = {}
var feedback_catalog: Dictionary = {}
var narrative: Dictionary = {}

func _init() -> void:
	world = _load("res://data/world/vertical_slice.v1.json")
	feedback_catalog = _load("res://data/design/feedback_catalog.json")
	narrative = _load("res://data/design/narrative_content.v1.json")
	assert(world.get("schema", "") == "deputation.world.v1")
	assert(world.get("case", {}).get("deadline_minute", 0) == DEADLINE)

func _load(path: String) -> Dictionary:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) == TYPE_DICTIONARY:
		return parsed as Dictionary
	push_error("Missing or invalid narrative resource: " + path)
	return {}

func remaining() -> int:
	return maxi(0, DEADLINE - minute)

func result() -> String:
	if stage == "validated":
		return "validated"
	if minute >= DEADLINE:
		return "expired"
	return "ongoing"

func stage_label() -> String:
	if stage == "validated":
		return "VALIDADO"
	if stage == "archive_review":
		return "REVISIÓN EN ARCHIVO"
	return "REGISTRADO"

func facts() -> Array[String]:
	var k: Array[String] = []
	if has_basis: k.append("CASE_BASIS")
	if has_history: k.append("HISTORY")
	if has_review: k.append("REVIEW")
	if has_ready: k.append("READY")
	return k

func snapshot() -> Dictionary:
	return {
		"minute": minute, "room": room, "stage": stage,
		"permissions": [PERMISSION] if has_permission else [],
		"knowledge": facts(),
		"outcome": result()
	}

func _advance(amount: int) -> void:
	for i in range(amount):
		minute += 1
		if minute == 10 and stage == "registered":
			stage = "archive_review"
		if minute == 15:
			has_review = true
		if minute == 27:
			has_ready = true

func _room_data() -> Dictionary:
	for entry in world.get("rooms", []):
		if entry.get("symbol", "") == room:
			return entry
	return {}

func _target_room(id: int) -> String:
	for entry in world.get("rooms", []):
		if int(entry.get("id", -1)) == id:
			return str(entry.get("symbol", ""))
	return ""

func _reject(code: String) -> String:
	last_code = code
	return code

func command(action: String, argument: Variant = null) -> String:
	# Closure means no mutating action may change a completed/expired case.
	if action == "inspect_case_status":
		last_code = "STATUS_VIEWED"
		return last_code
	if result() == "validated":
		return _reject("CASE_ALREADY_VALIDATED")
	if result() == "expired":
		return _reject("DEADLINE_EXPIRED")

	if action == "move":
		var data: Dictionary = _room_data()
		var exits: Array = data.get("exits", [])
		var costs: Array = data.get("travel_minutes", [])
		for index in range(exits.size()):
			if _target_room(int(exits[index])) == str(argument):
				_advance(int(costs[index]))
				room = str(argument)
				last_code = "MOVED"
				return last_code
		return _reject("INVALID_EXIT")

	if action == "wait":
		var delta: int = int(argument)
		if delta < 1 or delta > 30:
			return _reject("INVALID_WAIT")
		_advance(delta)
		last_code = "WAITED"
		return last_code

	if action == "read_case_file":
		if room != "REGISTRY":
			return _reject("WRONG_ROOM")
		if has_basis:
			return _reject("FILE_ALREADY_READ")
		has_basis = true
		_advance(1)
		last_code = "CASE_FILE_READ"
		return last_code

	if action == "request_permit":
		if room != "REGISTRY":
			return _reject("WRONG_ROOM")
		if has_permission:
			return _reject("PERMISSION_ALREADY_GRANTED")
		if not has_basis:
			return _reject("MISSING_CASE_BASIS")
		has_permission = true
		_advance(1)
		last_code = "PERMIT_GRANTED"
		return last_code

	if action == "read_archive":
		if room != "ARCHIVE":
			return _reject("WRONG_ROOM")
		if not has_permission:
			return _reject("MISSING_CASE_PERMISSION")
		if stage != "archive_review":
			return _reject("INVALID_CASE_STAGE")
		if has_history:
			return _reject("FILE_ALREADY_READ")
		has_history = true
		_advance(1)
		last_code = "ARCHIVE_READ"
		return last_code

	if action == "validate_case":
		if room != "ARCHIVE":
			return _reject("WRONG_ROOM")
		if stage != "archive_review":
			return _reject("INVALID_CASE_STAGE")
		if not has_history:
			return _reject("MISSING_HISTORY")
		if not has_ready:
			return _reject("MISSING_READY")
		_advance(1)
		stage = "validated"
		last_code = "CASE_VALIDATED"
		return last_code

	return _reject("UNKNOWN_ACTION")

func explanation() -> Dictionary:
	var result_data: Dictionary = narrative.get("results", {}).get(last_code, {})
	for entry in feedback_catalog.get("denials", []):
		if entry.get("code", "") == last_code:
			return {
				"actor": str(entry.get("actor", "SISTEMA")),
				"label": str(result_data.get("label", "DENEGADO")),
				"message": str(entry.get("visible_reason", "No disponible")),
				"next": str(entry.get("next_action", "Consultar estado")),
				"cue": "denial",
				"code": last_code
			}
	return {
		"actor": str(result_data.get("actor", "SISTEMA")),
		"label": str(result_data.get("label", last_code)),
		"message": str(result_data.get("message", "Acción registrada.")),
		"next": str(result_data.get("next", "Consultar estado")),
		"cue": str(result_data.get("cue", "silent")),
		"code": last_code
	}
