import openai
import azure.cognitiveservices.speech as speechsdk


class ChatBot:
    def __init__(self, API_KEY):
        openai.api_key = API_KEY

    def query_chat(self, chat_history):
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat_history
        )
        chat_history.append({
            "role": "assistant",
            "content": completion.choices[0].message["content"]
        })
        return chat_history, completion.choices[0].message["content"]

    def user_chat(self, text, chat_history):
        message = {
            "role": "user",
            "content": text
        }
        chat_history.append(message)
        return chat_history


class VoiceBot(ChatBot):
    def __init__(self, openai, azure):
        super().__init__(openai)
        self.speech_config = speechsdk.SpeechConfig(subscription=azure, region='westus')

    def get_speech(self, chat_history):
        recognized_text = ""
        self.speech_config.speech_recognition_language = "en-US"
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
        speech_recognition_result = speech_recognizer.recognize_once_async().get()
        recognized_text = speech_recognition_result.text
        chat_history = self.user_chat(recognized_text, chat_history)
        return chat_history, recognized_text

    def speak_response(self, chat_history):
        chat_history, response = self.query_chat(chat_history)

        speech_config = speechsdk.SpeechConfig(subscription='90e2389be77e483cbeb7b7f32c0e9be7', region='westus')
        speech_config.speech_synthesis_voice_name = "en-US-SteffanNeural"
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        result = speech_synthesizer.speak_text_async(response).get()

        return chat_history, response















