from fastapi import FastAPI
from endpoints import router
from logger import logger
import uvicorn
import models
from database import engine
# Initialize FastAPI app
app = FastAPI()

# Include API endpoints
app.include_router(router)

models.Base.metadata.create_all(bind=engine)

# Main entry point
if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    logger.info("FastAPI server stopped.")