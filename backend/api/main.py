from fastapi import FastAPI
from infrastructures.fastapi.middlewares.need import register_middleware
# import router for each module


# add open telemetry

#from common.errors import


# import middlewares

version = "v1"

description = """
A REST API for a recommend restful api service.

This REST API is able to;
...
    """

version_prefix =f"/rec-api/{version}"

app = FastAPI(
    title="Restful-API-Rec",
    description=description,
    license_info={"name": "...", "url": "..."},
    contact={
        "name": "Duc Tung Le",
        "url": "https://github.com/herolava259",
        "email": "elementalhero259@gmail.com"
    },
    term_of_service= "https://exmaple.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc"
)

# ex: add health checks

@app.get(f"{version_prefix}/health", tags=["Health"])
async def health_check():
    return {"status": "I'm an API Ninja"}



# add errors, exceptions

# add middlewares
register_middleware(app)

# add api routers