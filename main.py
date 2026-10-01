from fastapi import FastAPI

app = FastAPI(title="Support KPI Engine")


@app.get("/")
def health_check():
    return{"status": "ok"}
