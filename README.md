# **wAIfu**

AI powered waifu.

This is customizable, audio based, chat bot that makes use of a number of different AI/ML to be able to listen to you and respond in kind.

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

Install CoquiTTS: Coqui has been provided as a submodule already
```
cd wAIfu/src/TTS
make system-deps
make install
```

## **Configuration**

Within the `config.json` file, there are a number of fields that you can configure to tailor the experience

`openAIKey`: This is required for operation as it is needed to make API calls to OpenAI. You just need to enter the API key generated for your OpenAI account.

`promptFile`: This contains the path to the prompt file you wish to use. The prompt file should contain a priming prompt telling the AI how you want it to respond/behave. There are a variety of ways to specify this prompt and how it is structured may yield different outputs. You may need to play around with it.

`aiName`: Name of the AI. This is mostly just used for adding context to the text based logs of the chat. If you mention a name for the AI in the prompt file, this should match.

`userName`: Name of the user (you). Like the `aiName` this is also just for adding context. If you want the AI to refer to you by name directly, it needs to be specified somewhere in the priming prompt in the prompt file.

`whisperModel`: Which model you want whisper to use. `tiny(.en)`, `base(.en)`, `small(.en)`, `medium(.en)`, `large`. larger models may be more accurate, but may take longer to process your voice.

`coquiSpeechModel`: Which model you want Coqui to use for generating speech. More information on the available models/how to list them can be found on the [coqui github](https://github.com/coqui-ai/TTS) or in their [docs](https://tts.readthedocs.io/en/latest/). You can also train your own or fine tune a model to use if you want.

`cloneVoiceFile`: Only works with Coqui's `tts_models/multilingual/multi-dataset/your_tts` model. It uses Coqui's YourTTS model to attempt to clone a speaker from a given recording file.

## **Usage**

1. Copy your OpenAI API key into the `openAIKey` field in the `src/config.json` file to be able to make API calls.

2. Customize your prompt in the prompt file `src/prompt.txt`

3. Customize the rest of the configs as you wish

4. Ensure that you have a microphone and audio playback device or you will not be able to interact or hear the program.

5. Run waifu.py `python waifu.py`.

6. Begin recording by pressing the "r" key and press "r" again to end recording.

7. Talk to your waifu when recording

8. Watch the magic happen.

## **How it Works**

wAIfu integrates 3 seperate AI models to detect your speech, generate a response to what you said, and then generate speech based on its response.

It first starts by recording your voice and transcribing your speech. This is done through the use of OpenAI's Whisper AI to analyze what you said and transcribe your words into text.

Once OpenAI's Whisper has finished transcribing your speech, it is sent to OpenAI's GPT3.5 chat engine, along with the primer prompt, and some chat history via OpenAI's API, where it will generate a response to send back.

Finally, the text response from GPT3.5 is passed onto CoquiTTS, an AI that can generate or clone speech of the given text using a number of different models. The speech is then played back to the user (you), thus completing a single response to the conversation.
