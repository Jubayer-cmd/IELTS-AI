from fastapi import FastAPI

app = FastAPI(title="IELTS Mock Test", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "IELTS Mock Test API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
