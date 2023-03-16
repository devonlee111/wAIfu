import pyaudio
import wave

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

class recorder():
	def __init__(self, output_file):
		self.recording = False
		self.output_file = output_file

	def start(self):
		if self.recording: return
		try:
			self.frames = []
			self.stream = p.open(format=FORMAT,
							channels=CHANNELS,
							rate=RATE,
							input=True,
							frames_per_buffer=CHUNK,
							stream_callback=self.callback)
			print("Stream active:", self.stream.is_active())
			print("start Stream")
			self.recording = True
		except:
			raise

	def stop(self):
		if not self.recording: return
		self.recording = False
		print("Stop recording")
		self.stream.stop_stream()
		self.stream.close()

		wf = wave.open(self.output_file, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(self.frames))
		wf.close

	def callback(self, in_data, frame_count, time_info, status):
		self.frames.append(in_data)
		return in_data, pyaudio.paContinue
