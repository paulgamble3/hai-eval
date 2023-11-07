import base64


sample_config = {
      "phoneNumber": "",
      "model": "llama70b-sft-gpt4-annotated-checklist-10-25",
      "supportModel": "llama",
      "llmStreaming": True,
      "ttsStreaming": True,
      "supportEngines": [
        "dob-verification-engine",
        "identity-verification-engine"
      ],
      "template": "neel_v2",
      "tts": "eleven_labs_soft_gentle",
      "asr": "dg-phonecall",
      "scriptId": "01ef5e83-257f-4879-a428-7450986c868f",
      "patientName": "Lily Adams",
      "otherSettings": {
        "USE_LLAMA_V2_PROMPT_FORMAT": False,
        "USE_FOLLOW_UPS_IN_KICKOUT_PROMPT": False
      }
    }

sample_encoding = base64.b64encode(str(sample_config).encode("utf-8")).decode("utf-8")

print(sample_encoding)
