from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/sample/my-api/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True, workers=2)