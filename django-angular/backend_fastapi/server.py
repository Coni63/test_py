from fastapi import Depends, FastAPI
import uvicorn

from auth import can_edit, can_read
from auth.jwt_model import JWTToken

app = FastAPI()


@app.get("/sample/my-api/")
async def root(user_info: JWTToken = Depends(can_read)):
    print(user_info)
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True, workers=2)