# **wAIfu**

AI powered waifu

## **Requirements**

### **Environments**

**Ubuntu**: This has been verified to work on Ubuntu 22.04

**Note**: Currently this requires an X Window environment, and wont function on headless systems

### **Hardware**

**GPU**: It is recommended to run on an Nvidia GPU as the models will take a long time to run on CPU.

### **Software**

**Python**: This has been tested to work on python version 3.10.9

**[Whisper](https://github.com/openai/whisper)**: Whisper is used for the transcription process and needs to be installed in your environment

**[Coqui AI](https://github.com/coqui-ai/TTS)**: Coqui AI is used for synthesizing the AI's speech [WIP]

**[OpenAI](https://platform.openai.com/overview)**: You require an OpenAI API key which you can aquire on their site for chat generation

**PortAudio (Ubuntu)**: PortAudio may be required for python to be able to record your microphone

## **Installation**

**Conda**: It is recommended to use conda (anaconda/Miniconda) to manage your environment.

Install wAIfu: `git clone --recursive https://github.com/devonlee111/wAIfu.git`

Install [Whisper](https://github.com/openai/whisper) and [TorToise](https://github.com/neonbjb/tortoise-tts)

Install PortAudio (Ubuntu): `sudo apt install portaudio19-dev`

- version may or may not be different based on time and distribution

Install requirements: `pip install -r requirements.txt`

Install Coqui AI: Coqui has been provided as a submodule already
```
cd wAIfu/src/TTS
make system-deps
make install
```

## **Usage**

1. Copy your OpenAI API key into the `src/openai_key` file to be able to make API calls.

2. Ensure that you have a microphone and audio playback device or you will not be able to interact or hear the program.

3. Run waifu.py `python waifu.py`.

4. Begin recording by pressing the "r" key and press "r" again to end recording.

5. Talk to your waifu when recording

6. Watch the magic happen.

## **How it Works**


WIP
