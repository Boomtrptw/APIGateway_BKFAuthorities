from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import appsetting
from controller.api_bkf_system import router as api_bkf_system

app = FastAPI(
    title="API IMES",
    version="1.0.0",
    description="Intelligence Manufacturing Execution System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_bkf_system)

if __name__ == "__main__":
    if appsetting.host == "0.0.0.0":
        # uvicorn.run("main:app", host=appsetting.host, port=appsetting.port, reload=True, ssl_keyfile=appsetting.sslKeyFile, ssl_certfile=appsetting.sslCertFile)
        uvicorn.run("main:app", host=appsetting.host, port=appsetting.port, reload=True)
    else:
        uvicorn.run("main:app", host=appsetting.host, port=appsetting.port, reload=True)
