extends Control
## Institutional desk: three layouts, one case model, original procedural UI.
## Godot 4.x host-only prototype. No proprietary fonts/images required.
const CaseState = preload("res://godot/case_state.gd")
const LAYOUTS = ["EXPEDIENTE", "BANDEJA", "VENTANILLA"]

var model: RefCounted
var colors: Dictionary = {}
var mono: Font
var active_layout: int = 0

func _ready() -> void:
	model = CaseState.new()
	var palette_data: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/design/visual_palette.v1.json")
	)
	if typeof(palette_data) == TYPE_DICTIONARY:
		colors = palette_data.get("colors", {})
	var installed_font: SystemFont = SystemFont.new()
	installed_font.font_names = PackedStringArray([
		"DejaVu Sans Mono", "Liberation Mono", "Noto Sans Mono", "Courier New"
	])
	mono = installed_font
	_redraw()

func _ink(role: String) -> Color:
	return Color(str(colors.get(role, "#EEE5CE")))

func _caption(message: String, size: int = 16, role: String = "ink") -> Label:
	var label: Label = Label.new()
	label.text = message
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	label.add_theme_font_override("font", mono)
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", _ink(role))
	return label

func _block(body: Control, bg: String = "paper", outline: String = "slate") -> PanelContainer:
	var box: PanelContainer = PanelContainer.new()
	var style: StyleBoxFlat = StyleBoxFlat.new()
	style.bg_color = _ink(bg)
	style.border_color = _ink(outline)
	style.set_border_width_all(2)
	style.content_margin_left = 16.0
	style.content_margin_right = 16.0
	style.content_margin_top = 14.0
	style.content_margin_bottom = 14.0
	box.add_theme_stylebox_override("panel", style)
	box.add_child(body)
	return box

func _stack(spacing: int = 12) -> VBoxContainer:
	var v: VBoxContainer = VBoxContainer.new()
	v.add_theme_constant_override("separation", spacing)
	return v

func _action_button(title: String, action: String, argument: Variant = null) -> Button:
	var button: Button = Button.new()
	button.text = title
	button.custom_minimum_size = Vector2(0, 39)
	button.focus_mode = Control.FOCUS_ALL
	button.add_theme_font_override("font", mono)
	button.add_theme_font_size_override("font_size", 15)
	button.add_theme_color_override("font_color", _ink("pearl"))
	button.add_theme_color_override("font_hover_color", _ink("pearl"))
	button.add_theme_color_override("font_pressed_color", _ink("paper"))
	for key in ["normal", "hover", "pressed", "focus"]:
		var style: StyleBoxFlat = StyleBoxFlat.new()
		style.bg_color = _ink("coal") if key == "normal" else _ink("slate")
		style.border_color = _ink("pale_yellow") if key == "focus" else _ink("muted")
		style.set_border_width_all(1 if key != "focus" else 2)
		style.content_margin_left = 8.0
		style.content_margin_right = 8.0
		button.add_theme_stylebox_override(key, style)
	button.pressed.connect(_on_command.bind(action, argument))
	return button

func _on_command(action: String, arg: Variant) -> void:
	model.command(action, arg)
	_redraw()

func _on_layout(index: int) -> void:
	active_layout = index
	_redraw() # Pure presentation: never call model.command or advance ticks.

func _section(title: String, text: String, container: VBoxContainer) -> void:
	container.add_child(_caption(title, 18, "ink"))
	container.add_child(_caption(text, 16, "ink"))

func _redraw() -> void:
	for node in get_children():
		remove_child(node)
		node.queue_free()
	var bg: ColorRect = ColorRect.new()
	bg.color = _ink("carbon")
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

	var margin: MarginContainer = MarginContainer.new()
	for side in ["margin_left", "margin_right", "margin_top", "margin_bottom"]:
		margin.add_theme_constant_override(side, 18)
	add_child(margin)
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

	var root: VBoxContainer = _stack(10)
	margin.add_child(root)

	var mast: HBoxContainer = HBoxContainer.new()
	mast.add_theme_constant_override("separation", 12)
	root.add_child(mast)
	var title: Label = _caption("THE DEPUTATION  /  ARCHIVO CENTRAL", 22, "pearl")
	mast.add_child(title)
	mast.add_child(_caption(
		"EXP-0042   |   RELOJ SIMULADO  %02d/30   |   RESTAN %02d MIN" %
		[model.minute, model.remaining()], 16,
		"pale_red" if model.remaining() <= 5 else "pale_yellow"
	))

	var body: HBoxContainer = HBoxContainer.new()
	body.add_theme_constant_override("separation", 10)
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	root.add_child(body)

	var sidebar: VBoxContainer = _stack(14)
	var nav: PanelContainer = _block(sidebar, "coal", "slate")
	nav.custom_minimum_size = Vector2(234, 0)
	nav.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.add_child(nav)
	sidebar.add_child(_caption("SECCIÓN / 01", 16, "paper_aged"))
	for index in range(LAYOUTS.size()):
		var b: Button = _action_button(
			("> " if index == active_layout else "  ") + LAYOUTS[index],
			"inspect_case_status"
		)
		# A view switch does not even invoke the status query.
		for connection in b.pressed.get_connections():
			b.pressed.disconnect(connection["callable"])
		b.pressed.connect(_on_layout.bind(index))
		sidebar.add_child(b)
	sidebar.add_child(_caption("UBICACIÓN", 15, "pale_yellow"))
	sidebar.add_child(_caption(model.room, 18, "pearl"))
	sidebar.add_child(_caption("FASE", 15, "pale_yellow"))
	sidebar.add_child(_caption(model.stage_label(), 16, "pearl"))
	sidebar.add_child(_caption(
		"PERMISO: " + ("EXP-0042 / SÍ" if model.has_permission else "NO CONSTA"),
		15, "pale_green" if model.has_permission else "pale_red"
	))

	var middle: VBoxContainer = _stack(10)
	var paper: PanelContainer = _block(middle, "paper", "paper_aged")
	paper.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	paper.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.add_child(paper)
	if active_layout == 0:
		_render_case(middle)
	elif active_layout == 1:
		_render_tasks(middle)
	else:
		_render_administration(middle)

	var response_column: VBoxContainer = _stack(12)
	var response_panel: PanelContainer = _block(response_column, "paper_aged", "slate")
	response_panel.custom_minimum_size = Vector2(320, 0)
	response_panel.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.add_child(response_panel)
	_render_response(response_column)

	var action_section: VBoxContainer = _stack(6)
	root.add_child(action_section)
	action_section.add_child(_caption("OPERACIONES  /  CADA ACCIÓN MUESTRA SU COSTE EN EL ESTADO", 14, "paper_aged"))
	var commands: GridContainer = GridContainer.new()
	commands.columns = 5
	commands.add_theme_constant_override("h_separation", 7)
	commands.add_theme_constant_override("v_separation", 7)
	action_section.add_child(commands)
	var actions: Array = [
		["IR PATIO", "move", "COURTYARD"],
		["IR REGISTRO", "move", "REGISTRY"],
		["IR ARCHIVO", "move", "ARCHIVE"],
		["LEER CARÁTULA", "read_case_file", null],
		["PEDIR PERMISO", "request_permit", null],
		["LEER ARCHIVO", "read_archive", null],
		["VALIDAR CASO", "validate_case", null],
		["ESPERAR +1", "wait", 1],
		["ESPERAR +3", "wait", 3],
		["CONSULTAR ESTADO", "inspect_case_status", null],
	]
	for item in actions:
		commands.add_child(_action_button(str(item[0]), str(item[1]), item[2]))
	var next_hito: int = 30
	for h in [10, 15, 27, 30]:
		if h > model.minute:
			next_hito = h
			break
	var hito_button: Button = _action_button(
		"ESPERAR AL SIGUIENTE HITO (+%d MIN)" % (next_hito - model.minute),
		"wait", next_hito - model.minute
	)
	action_section.add_child(hito_button)
	root.add_child(_caption(
		"PRUEBA HOST GODOT · ESTADO ÚNICO · SIN GODOT/C64 PARIDAD CERTIFICADA · AUDIO: CUES DOCUMENTADOS",
		13, "paper_aged"
	))

func _render_case(v: VBoxContainer) -> void:
	v.add_child(_caption("FORMULARIO 42-B   ·   COPIA DE TRABAJO", 15, "muted"))
	v.add_child(_caption("EXPEDIENTE EXP-0042", 26, "ink"))
	v.add_child(_caption("----------------------------------------", 16, "ink"))
	v.add_child(_caption(str(model.narrative.get("case_body", "")), 16, "ink"))
	v.add_child(_caption("HECHOS ACREDITADOS: " + ", ".join(model.facts()), 16, "green"))
	if model.has_history:
		v.add_child(_caption("── TESTIMONIO DE ARCHIVO ──", 17, "stamp"))
		v.add_child(_caption(str(model.narrative.get("archive_body", "")), 16, "ink"))
	else:
		v.add_child(_caption("[RESERVADO]  Pendiente de autorización y fase.", 16, "red"))
	v.add_child(_caption("SELLO: " + model.stage_label(), 19,
		"green" if model.stage == "validated" else "stamp"))

func _render_tasks(v: VBoxContainer) -> void:
	v.add_child(_caption("BANDEJA DE TRÁMITES / EXP-0042", 24, "ink"))
	var checklist: Array = [
		["CARÁTULA", model.has_basis, "Registro / identificar motivo"],
		["PERMISO ESPECÍFICO", model.has_permission, "Secretaría / solo EXP-0042"],
		["REVISIÓN ABIERTA", model.stage != "registered", "Archivo / m10"],
		["HISTORIA DOCUMENTAL", model.has_history, "Archivo / leer con permiso"],
		["LISTO PARA VALIDAR", model.has_ready, "Hito institucional / m27"],
		["DISCREPANCIA VALIDADA", model.stage == "validated", "Archivo / acción final"],
	]
	for entry in checklist:
		v.add_child(_caption(
			("[+] " if entry[1] else "[ ] ") + str(entry[0]), 19,
			"green" if entry[1] else "ink"
		))
		v.add_child(_caption("     " + str(entry[2]), 15, "muted"))
	v.add_child(_caption("Cada paso conserva el reloj simulado y su procedencia.", 16, "ink"))

func _render_administration(v: VBoxContainer) -> void:
	var actor: String = "VENTANILLA CENTRAL"
	var role: String = "SIN COMPETENCIA DIRECTA"
	if model.room == "REGISTRY":
		actor = "ELENA ROBLES"
		role = "SECRETARÍA  /  AUTORIZACIONES"
	elif model.room == "ARCHIVE":
		actor = "MARCEL VIDAL"
		role = "ARCHIVERO  /  CUSTODIA"
	v.add_child(_caption("VENTANILLA / ATENCIÓN AL EXPEDIENTE", 16, "muted"))
	v.add_child(_caption(actor, 26, "ink"))
	v.add_child(_caption(role, 18, "stamp"))
	v.add_child(_caption("----------------------------------------", 16, "ink"))
	v.add_child(_caption(str(model.narrative.get("room_descriptions", {}).get(
		model.room, "")), 17, "ink"))
	v.add_child(_caption(
		"COMPETENCIA: " +
		("SOLICITAR PERMISO" if model.room == "REGISTRY" else
		"CONSULTAR EXPEDIENTE" if model.room == "ARCHIVE" else
		"DESPLAZARSE A REGISTRO"), 16, "green"))
	v.add_child(_caption("Las negativas nunca retiran minutos.", 16, "muted"))

func _render_response(v: VBoxContainer) -> void:
	var info: Dictionary = model.explanation()
	var code: String = str(info.get("code", "BOOT"))
	var rejected: bool = (
		code.begins_with("MISSING_") or code.begins_with("INVALID_")
		or code.begins_with("WRONG_") or code == "DEADLINE_EXPIRED"
		or code == "CASE_ALREADY_VALIDATED" or code == "PERMISSION_ALREADY_GRANTED"
	)
	v.add_child(_caption("RESOLUCIÓN / ÚLTIMO ACTO", 15, "muted"))
	v.add_child(_caption(str(info.get("label", code)), 23,
		"red" if rejected else "green"))
	v.add_child(_caption("REF: " + code, 15, "ink"))
	v.add_child(_caption("AUTORIDAD", 14, "muted"))
	v.add_child(_caption(str(info.get("actor", "SISTEMA")), 17, "ink"))
	v.add_child(_caption("MOTIVACIÓN COMUNICADA", 14, "muted"))
	v.add_child(_caption(str(info.get("message", "")), 17, "ink"))
	v.add_child(_caption("SIGUIENTE ACTO", 14, "muted"))
	v.add_child(_caption(str(info.get("next", "Consultar estado")), 16, "green"))
	v.add_child(_caption(
		"QUEDAN %02d MIN (SIMULADOS)" % model.remaining(), 17,
		"red" if model.remaining() <= 5 else "ink"
	))
	v.add_child(_caption("SONIDO EVENTO: " + str(info.get("cue", "silent")), 13, "muted"))
	if model.result() == "validated":
		v.add_child(_caption("[+] CASO VALIDADO / FIN", 20, "green"))
	elif model.result() == "expired":
		v.add_child(_caption("[X] PLAZO VENCIDO / FIN", 20, "red"))
