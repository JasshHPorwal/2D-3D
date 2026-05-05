import pytesseract
try:
    import open3d as o3d
except Exception:
    o3d = None
import open3d as o3d, pytesseract
from fastapi import APIRouter,UploadFile,File,HTTPException,Depends
from fastapi.responses import FileResponse
from app.core.config import get_settings, Settings
from app.services.pipeline_service import run_pipeline_async,get_job
router=APIRouter()
@router.post('/reconstruct')
async def reconstruct(drawing:UploadFile=File(...),s:Settings=Depends(get_settings)):
 if drawing.content_type not in {'image/png','image/jpeg'}: raise HTTPException(400,'Unsupported mime type')
 b=await drawing.read();
 if len(b)>s.MAX_UPLOAD_MB*1024*1024: raise HTTPException(413,'File too large')
 return await run_pipeline_async(b)
@router.get('/jobs/{job_id}')
def job(job_id:str):
 r=get_job(job_id)
 if not r: raise HTTPException(404,'Job not found')
 return r
@router.get('/jobs/{job_id}/model.glb')
def model(job_id:str):
 r=get_job(job_id)
 if not r or r.status!='COMPLETED' or not r.glb_path: raise HTTPException(404,'model not found')
 return FileResponse(r.glb_path,media_type='model/gltf-binary',filename='model.glb')
@router.get('/health')
def health(): return {'status':'ok','tesseract':str(pytesseract.get_tesseract_version()),'open3d':o3d.__version__}
