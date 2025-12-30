from src.config import settings
from src.models.base import Base
from sqlalchemy import create_engine
from src.routes.user import router
from src.routes.subscription import router as subscription_router
from src.routes.auth import routers as ouath_router
from fastapi import FastAPI
from src.routes.expenses import router as expenses_router
from src.routes.ws_routers import router as websocket_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.services.notifications_service import notification_service
from src.routes.analytics import router as analytics
# from src.services.notifications_service import send_notification

scheduler = AsyncIOScheduler() #создание планировщика задач

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI)) #соединение с бд

Base.metadata.create_all(bind=engine) #создание всех таблиц в бд

app = FastAPI() #точка входа приложения

app.include_router(router=router, prefix='/test')
app.include_router(router=ouath_router)
app.include_router(router=subscription_router)
app.include_router(router=expenses_router)
app.include_router(router=websocket_router)
app.include_router(router=analytics, prefix='/anlytics')

@app.on_event('startup')
def add_cron_job():
    
    scheduler.add_job(notification_service.send_notitfications, 'interval', seconds=1)
    scheduler.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.__main__:app", host='127.0.0.1', port=8000, reload=True, workers=4)
    # запуск приложения с помощью uvicorn
    # host и port берутся из настроек

