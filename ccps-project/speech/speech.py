from gtts import gTTS
import os
import uuid

class Speech:
    def __init__(self) -> None:
        pass
    def speak(self, Input):
        try:
            myobj = gTTS(text=Input, lang='en', slow=False, tld="us")
            
            name = uuid.uuid4().hex
            
            name = name[:min(8, len(name))]
            
            filename = f"./tmp/{name}.mp3"
            
            myobj.save(filename)
            
            os.system("mpg123 " + filename)
            
            os.remove(filename)
        except:
            os.remove(filename)
