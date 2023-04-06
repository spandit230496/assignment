from fastapi import FastAPI,UploadFile,Response, Request, Header
import uvicorn
import json
from fastapi.responses import StreamingResponse
import os

app=FastAPI()

#api to upload video 
@app.post("/file/upload")
def upload(file:UploadFile):
    data=json.load(file.file.read())
    return {"content":data,"filename":file.filename}

#api to download a video
@app.get("/download/{video_name}")
async def download_video(video_name: str, response: Response):
    video_path = f"/path/to/videos/{video_name}.mp4"
    if not os.path.exists(video_path):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Video not found"}
    
    response.headers["Content-Disposition"] = f"attachment; filename={video_name}.mp4"
    response.headers["Content-Type"] = "video/mp4"
    with open(video_path, "rb") as video_file:
        video_data = video_file.read()
    return video_data
    
#api to stream a video
@app.get("/video/{name}")
async def stream_video(name: str):
    video_path = f"/path/to/videos/{name}"
    if not os.path.exists(video_path):
        return Response(content="Video not found", status_code=404)

    def stream():
        with open(video_path, mode="rb") as file:
            while True:
                video_chunk = file.read(1024*1024) # read 1 MB chunk of the video
                if not video_chunk:
                    break # end of file
                yield video_chunk # stream the chunk to the client

    return StreamingResponse(stream(), media_type="video/mp4")






if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)