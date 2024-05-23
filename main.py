import uvicorn
from fastapi import FastAPI, Request
from app.controllers.revenue_controller import revenue_router
from app.controllers.user_controller import user_router
from app.controllers.expense_controller import expense_router
from app.controllers.visualization_controller import visualization_router
from app.middlewares.log import setup_logging, log_requests

# Set up logging at the startup of the application
setup_logging('app.log')

app = FastAPI()


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    return await log_requests(request, call_next)

app.include_router(user_router, prefix='/user')
app.include_router(revenue_router, prefix='/revenue')
app.include_router(expense_router, prefix='/expense')
app.include_router(visualization_router, prefix='/visualization')

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
