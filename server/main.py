from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import util

app = FastAPI(title="Bangalore House Price Prediction API", version="1.0.0")

# Enable CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model on startup
@app.on_event("startup")
async def startup_event():
    util.load_saved_artifacts()

# Serve  main HTML page at root
@app.get("/")
async def read_root():
    return FileResponse('../client/app.html')

# Serve individual static files directly 
@app.get("/app.css")
async def get_css():
    return FileResponse('../client/app.css')

@app.get("/app.js") 
async def get_js():
    return FileResponse('../client/app.js')

@app.get("/get_location_names")
async def get_location_names():
    return {
        'locations': util.get_location_names()
    }

@app.post("/predict_home_price")
async def predict_home_price(
    total_sqft: float = Form(...),
    location: str = Form(...),
    bhk: int = Form(...),
    bath: int = Form(...)
):
    estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
    return {
        'estimated_price': estimated_price
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)