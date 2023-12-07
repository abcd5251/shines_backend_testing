import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
import io
from pydantic import BaseModel
import uvicorn

from modules.get_yt_info import get_yt_channel_data, get_tag_info
from modules.save_channel_links import save_channel_links
from modules.utils import generate_audio, get_summarization

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/audio", StaticFiles(directory="audio"), name="audio")

# middleware
app.add_middleware(
    CORSMiddleware, 
    allow_credentials=True, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

class search_channel_respond(BaseModel):
    search_query : str
    page :int

class save_channel_videos(BaseModel):
    username : str

class tag_respond(BaseModel):
    tag_num : int
    page : int

class Summarization(BaseModel):
    content:str


@app.post("/search_channel_respond/")
async def search_channel_respond(item: search_channel_respond):
    try:
        yt_meta_data = get_yt_channel_data(item.search_query, item.page)
        yt_meta_data_json = yt_meta_data.to_json(orient="records")
        return JSONResponse(content={"code": 0, "data": yt_meta_data_json}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"code": 1, "error": str(e)}, status_code=500)
    
@app.post("/save_channel_videos/")
async def save_channel_videos(item: save_channel_videos):
    save_channel_links(item.username)
    #os.remove(save_place)

@app.post("/tag_respond/")
async def tag_respond(item: tag_respond):
    try:
        yt_meta_data = get_tag_info(item.tag_num, item.page)
        yt_meta_data_json = yt_meta_data.to_json(orient="records")
        return JSONResponse(content={"code": 0, "data": yt_meta_data_json}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"code": 1, "error": str(e)}, status_code=500)

@app.get("/get_audio/")
async def get_audio(content : str, gender : int, audio_number: int):
    audio = generate_audio(content, gender, audio_number)
    
    #audio_path = f"audio/audio_{audio_number}.mp3"
    return StreamingResponse(io.BytesIO(audio), media_type="audio/mp3")
    #return FileResponse(audio_path, media_type="audio/mp3")

@app.get("/get_image/")
async def get_image(image_number: int):
    if image_number not in {1, 2, 3}:
        raise HTTPException(status_code=404, detail="Image not found")

    image_path = f"images/Avatar_{image_number}.png"

    return FileResponse(image_path, media_type="image/png")

@app.get("/get_mp4/")
async def get_mp4():
    mp4_file_path = "path/to/your/local/file.mp4"  # Replace with the actual path to your MP4 file

    if os.path.exists(mp4_file_path):
        with open(mp4_file_path, "rb") as mp4_file:
            mp4_content = mp4_file.read()

        return StreamingResponse(io.BytesIO(mp4_content), media_type="video/mp4", headers={"Content-Disposition": "inline; filename=example.mp4"})
    else:
        return {"error": "Generate failed"}

@app.post("/Summarization/")
async def Summarization(item: Summarization):
    try:
        summarization_text = get_summarization(item.content)
        return JSONResponse(content={"code": 0, "data": summarization_text}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"code": 1, "error": str(e)}, status_code=500)
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)