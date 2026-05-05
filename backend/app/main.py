import os,shutil,time
from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import get_settings
from app.api.routes.reconstruction import router
@asynccontextmanager
async def lifespan(app):
 s=get_settings(); os.makedirs(s.UPLOAD_DIR,exist_ok=True)
 if not shutil.which(s.TESSERACT_CMD) and not os.path.exists(s.TESSERACT_CMD): raise RuntimeError('tesseract missing')
 yield
app=FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=get_settings().CORS_ORIGINS,allow_methods=['*'],allow_headers=['*'])
@app.middleware('http')
async def rid(req:Request,call_next):
 req.state.request_id=os.urandom(4).hex(); t=time.time(); r=await call_next(req); r.headers['X-Request-ID']=req.state.request_id; r.headers['X-Process-Time']=str((time.time()-t)*1000); return r
@app.exception_handler(Exception)
async def e500(req:Request,e:Exception): return JSONResponse(status_code=500,content={'error':str(e),'request_id':getattr(req.state,'request_id',None)})
app.include_router(router,prefix='/api')
