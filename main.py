from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def get_status():
    return {"message": "API Patrick Travel opérationnelle 🚀"}