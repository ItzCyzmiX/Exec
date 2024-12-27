from random import randint
import subprocess
import os

from pydantic import BaseModel
from fastapi import FastAPI # type: ignore

app = FastAPI()
LANGUAGES = {
    "python": {
        "ext": "py",
        "runCMD": ["python"]
    },
    "javascript": {
        "ext": "js",
        "runCMD": ["node"]
    }
}

class Exec:
    def __init__(self):
        pass

    @classmethod
    def run(self, code: str, language: str) -> str:
        if language in LANGUAGES:
            code_file = ""
            path = f"{language}_temp_{randint(0, 1000)}.{LANGUAGES[language]['ext']}"
            code_file = os.path.join(path)
            with open(code_file, "w") as f:
                f.write(code)
            
            result = subprocess.run(LANGUAGES[language]["runCMD"] + [code_file], capture_output=True, text=True)
            os.remove(path)
            return result.stdout

        else:
            return "Invalid Language"
    
    @classmethod
    def get_langs(self):
        return list(LANGUAGES.keys())

class CODEOBJ(BaseModel):
    code: str
    language: str


@app.get('/getlangs')
async def get_langs():
    return {
        "languages": Exec.get_langs()
    }

@app.post('/exec')
async def main(codeObj: CODEOBJ):
    res = Exec.run(codeObj.code, codeObj.language)
    
    if res != "Invalid Language":
        return {
            "success": True,
            "stdout": res
        }
    else: 
        return {
            "success": False,
            "stdout": "",
            "error": res
        }
