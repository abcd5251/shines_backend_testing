import openai
from elevenlabs import generate, play, set_api_key, save
from elevenlabs import Voice, VoiceSettings
from dotenv import load_dotenv
load_dotenv()
import time 
import tiktoken
import os
import re
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
set_api_key(os.getenv("ELEVEN_API_KEY")) 

COMPLETIONS_MODEL = "gpt-3.5-turbo"

CATEGORY_LIST = "[NFT, Ethereum, GameFi, Layer2, ZK]"

INSTRUCTION = f"""
You are a proficient Web3 specialist, Given input, your task is to categorize the given input into one of the following five categories: {CATEGORY_LIST}. Only the category name should be output. And only choose category in this list.
Example,
### Input :
Title : 開箱 The Sandbox 全球總部，元宇宙其實沒我們想像那麼遙遠｜直接採訪核心團隊！Alpha Season 3 火熱進行中
Description : 這次 The Sandbox 官方還特別送出 2 張價值 500 SAND 幣的 Alpha Pass NFT
只要在影片下方留包含「一起來玩 Alpha Season 3」的留言並「告訴我們你最喜歡哪個體驗」例如: 一起來玩 Alpha Season 3! 我最喜歡XXXXXXXX
我們就會在 9/30 抽出 2 位幸運的觀眾空投 Alpha Pass NFT 🔥🔥
記得回來確認你有沒有中獎！我們會再跟你拿地址/註冊信箱
註：
1. 抽中後需完成 KYC 才能獲得 Alpha Pass NFT
2. 需在10/31前在 Alpha Season 3 升到 LV5（不難）才能解鎖 500 SAND 獎勵
-
如果你以為 The Sandbox 就是個元宇宙「遊戲」
如果你以為 Play to Earn 全都不靠譜
如果你以為元宇宙 Metaverse 還離我們很遠
你都必須看這部影片！

目前 The Sandbox 第三季重磅推出
除了有超過 90 款不同的體驗
還能邊玩邊賺 Alpha Pass 
最多獲得 500 SAND 的獎勵
新註冊的玩家更有機會獲得 1 x 1 LAND！
有興趣的觀眾們可以點擊下方連結

### Output:
GameFi
\n\n\n
Here is the input:\n
"""
SUMMARIZATION_PROMPT = """
You are now a YouTuber, given content below, please summarize this content, get the important points of it. And provide me with a verbal transcript version. Please only return the transcript.
"""

def num_tokens_from_string(string: str, encoding_name = COMPLETIONS_MODEL) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def preprocess(text):
    text = text.replace('\n', ' ').replace('/',' ').replace('..','')
    text = re.sub('\s+', ' ', text)
    return text

def openai_model(query):
    messages = [{"role":"system","content": INSTRUCTION}]
    messages.append({"role":"user", "content": query})
    num_token = num_tokens_from_string(messages[0]["content"] + messages[1]["content"])
    print("total token spend for prompt :" ,num_token)

    while True:
        try : 
            response = openai.ChatCompletion.create(
                            model = COMPLETIONS_MODEL,
                            messages = messages,
                            temperature = 0.8,
                            max_tokens = 4096 - num_token - 13
                        )
            break
        except Exception as err:
            print(err)
            time.sleep(0.1)
    answer = response.choices[0].message['content']
    return answer

def generate_audio(content: str, gender : int):
    
    if gender == 0:
        tone = "Emily"
    else:
        tone = "Adam"
    audio = generate(
        text= content,
        # voice=Voice(
        # voice_id='EXAVITQu4vr4xnSDxMaL',
        # settings=VoiceSettings(stability=0.4, similarity_boost=1, style=1, use_speaker_boost=True)
        # ),
        voice=tone,
        model='eleven_multilingual_v2'
    )
    return audio
    #save(audio,f"./audio/audio_{audio_number}.mp3")

def get_summarization(text : str):
    messages = [{"role":"system","content": SUMMARIZATION_PROMPT}]
    messages.append({"role":"user", "content": text})
    num_token = num_tokens_from_string(messages[0]["content"] + messages[1]["content"])
    print("total token spend for prompt :" ,num_token)

    while True:
        try : 
            response = openai.ChatCompletion.create(
                            model = COMPLETIONS_MODEL,
                            messages = messages,
                            temperature = 0.8,
                            max_tokens = 4096 - num_token - 13
                        )
            break
        except Exception as err:
            print(err)
            time.sleep(0.1)
    answer = response.choices[0].message['content']
    return answer


