extends Node
## Original, generated-at-runtime placeholder cues. No samples or licenses.
## The ambience is presentation only: it NEVER calls the case model.
const RATE: int = 22050
var enabled: bool = true
var elapsed: float = 0.0
var player: AudioStreamPlayer
var playback: AudioStreamGeneratorPlayback

func _ready() -> void:
	var stream: AudioStreamGenerator = AudioStreamGenerator.new()
	stream.mix_rate = float(RATE)
	stream.buffer_length = 0.35
	player = AudioStreamPlayer.new()
	player.stream = stream
	player.volume_db = -21.0
	add_child(player)
	player.play()
	playback = player.get_stream_playback() as AudioStreamGeneratorPlayback

func _process(delta: float) -> void:
	if not enabled:
		return
	elapsed += delta
	if elapsed >= 2.4:
		elapsed = fmod(elapsed, 2.4)
		cue("clock_tick") # Real-time ambience does not advance simulated minutes.

func cue(kind: String) -> void:
	if not enabled or playback == null or kind == "silent" or kind == "room_tone":
		return
	if kind == "footstep_paper":
		kind = "paper"
	var duration: float = 0.12
	var hz: float = 190.0
	if kind == "stamp":
		duration = 0.13
		hz = 102.0
	elif kind == "stamp_double":
		duration = 0.20
		hz = 105.0
	elif kind == "clock_stop":
		duration = 0.29
		hz = 325.0
	elif kind == "clock_tick":
		duration = 0.075
		hz = 690.0
	elif kind == "denial":
		duration = 0.11
		hz = 205.0
	elif kind == "paper":
		duration = 0.14
		hz = 95.0
	var frames: int = mini(playback.get_frames_available(), int(float(RATE) * duration))
	for i in range(frames):
		var t: float = float(i) / float(RATE)
		var envelope: float = pow(maxf(0.0, 1.0 - t / duration), 2.0)
		var n: float = float(((i * 1103515245 + 12345) & 0x7fffffff) % 1024) / 512.0 - 1.0
		var oscillator: float = sin(TAU * hz * t)
		var sample: float = 0.0
		match kind:
			"paper":
				sample = 0.20 * n * envelope
			"stamp":
				sample = (0.30 * oscillator + 0.22 * n) * envelope
			"stamp_double":
				sample = (0.30 * oscillator + 0.22 * n) * (envelope if t < 0.07 or t > 0.11 else 0.0)
			"clock_tick":
				sample = 0.21 * n * envelope
			"clock_stop":
				sample = 0.24 * sin(TAU * (hz - 490.0 * t) * t) * envelope
			"denial":
				sample = (0.16 * oscillator + 0.10 * n) * envelope
			_:
				sample = 0.10 * oscillator * envelope
		playback.push_frame(Vector2(sample, sample))
