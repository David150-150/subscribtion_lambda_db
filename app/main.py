import atexit

# Scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import models
from app.db import engine
from app.routers.auth import router as auth_router
from app.routers.customer import router as customer_router
from app.routers.product import router as product_router
from app.routers.schedule import router as schedule_router
from app.routers.subscription import router as subscription_router
from app.routers.transaction import router as transaction_router
from app.routers.transaction_details import router as transaction_details_router
from app.routers.transaction_failure import router as transaction_failures_router

# Lambda simulation
from app.utils.lambda_func import lambda_handler

# Routers


# ---------------- Initialize the app ---------------- #
app = FastAPI(
    title="Subscription API",
    version="1.0.0",
    description="Backend Subscription API. Handles Authentication, Customer, Product,Subscription, Schedule, Transaction, Transaction_Detail, Transaction_Failure, Lambda_Func.",
    contact={"name": "Intern Project", "phone": "+233 260867967"},
)

# ---------------- DB Table Creation ---------------- #
models.Base.metadata.create_all(bind=engine)

# ---------------- CORS Configuration ---------------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (customize in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Include All Routers ---------------- #
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(customer_router, prefix="/customer", tags=["Customer"])
app.include_router(product_router, prefix="/product", tags=["Product"])
app.include_router(transaction_router, prefix="/transaction", tags=["Transaction"])
app.include_router(
    transaction_details_router,
    prefix="/transaction-detail",  # ✅ change to hyphen and singular
    tags=["Transaction Details"],
)

app.include_router(
    transaction_failures_router,
    prefix="/transaction_failures",
    tags=["Transaction Failures"],
)
app.include_router(schedule_router, prefix="/schedule", tags=["Schedule"])
app.include_router(subscription_router, prefix="/subscription", tags=["Subscription"])


# ---------------- Lambda Simulation Endpoint ---------------- #
@app.get("/lambda", tags=["Lambda Simulation"])
def simulate_lambda():
    result = lambda_handler({}, {})
    encoded_body = jsonable_encoder(result["body"])
    return JSONResponse(status_code=result["statusCode"], content=encoded_body)


# ---------------- Lambda Scheduler ---------------- #
def run_lambda_on_schedule():
    result = lambda_handler({}, {})
    print("Lambda ran automatically — result:")
    print(result)


scheduler = BackgroundScheduler()
scheduler.add_job(run_lambda_on_schedule, "interval", seconds=60)  # Run every 60 seconds
# scheduler.add_job(run_lambda_on_schedule, "interval", minutes=30) # Run every 30 minutes
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
