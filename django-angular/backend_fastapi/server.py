from fastapi import Depends, FastAPI
import uvicorn

from auth import verify_token

# from auth import security

app = FastAPI()


@app.get("/sample/my-api/")
async def root(user_info: dict = Depends(verify_token)):
    print(user_info)
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True, workers=2)