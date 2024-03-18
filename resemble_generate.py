from resemble import Resemble
response_one = Resemble.v2.clips.create_sync(
    project_uuid="p4p4p4p",
    voice_uuid="e4e4e4e",
    body="Hello world, this is my AI Voice",
    title="Hello World",
    sample_rate=44100,
    output_format="wav",
    include_timestamps=True)
response_voice = Resemble.v2.voices.create('AI Scott')
voice_uuid = response_voice['item']['uuid'] 
name = 'audio.wav'
text = 'This is a test'
is_active = True
emotion = 'neutral'
with open("path/to/audio.wav", 'rb') as file:
    response = Resemble.v2.recordings.create(voice_uuid, file, name, text, is_active, emotion)
Resemble.v2.voices.build(response['item']['uuid'])