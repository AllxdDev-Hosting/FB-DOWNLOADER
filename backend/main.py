from time import time
from fastapi import FastAPI, Request, __version__
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] if you want to be specific
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""
@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}

@app.post("/fetch")
async def fetch_video(data: dict):
    url = data.get("url")
    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://getsave.net",
        "referer": "https://getsave.net/en",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64)",
        "x-requested-with": "XMLHttpRequest"
    }
    payload = f"url={url}"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://getsave.net/proxy.php",
            data=payload,
            headers=headers
        )
    return response.json()
