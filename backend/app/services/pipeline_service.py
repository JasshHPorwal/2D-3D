import asyncio,time,os
from uuid import uuid4
from app.models.schema import *
from app.core.config import get_settings
from app.pipeline.stage1_view_detector import detect_views
from app.pipeline.stage2_line_classifier import detect_and_classify_lines
from app.pipeline.stage3_circle_detector import detect_circles
from app.pipeline.stage4_dimension_reader import read_dimensions
from app.pipeline.stage5_geometry_builder import build_geometry
from app.pipeline.stage6_mesh_builder import build_mesh
from app.pipeline.stage7_exporter import export_glb
_jobs:dict[str,ReconstructionResult]={}

async def run_pipeline_async(image_bytes:bytes)->ReconstructionResult:
 job_id=uuid4().hex[:12]; os.makedirs(f"{get_settings().UPLOAD_DIR}/{job_id}",exist_ok=True); stages=[]
 try:
  loop=asyncio.get_running_loop()
  t=time.time(); views=await loop.run_in_executor(None,detect_views,image_bytes,job_id); stages.append(StageResult(stage='view_detection',success=True,duration_ms=(time.time()-t)*1000))
  t=time.time(); lines=await loop.run_in_executor(None,detect_and_classify_lines,views); stages.append(StageResult(stage='line_classification',success=True,duration_ms=(time.time()-t)*1000))
  t=time.time(); circles=await loop.run_in_executor(None,detect_circles,views); stages.append(StageResult(stage='circle_detection',success=True,duration_ms=(time.time()-t)*1000))
  t=time.time(); dims,ppm=await loop.run_in_executor(None,read_dimensions,views); stages.append(StageResult(stage='dimension_reading',success=True,duration_ms=(time.time()-t)*1000))
  parsed={k:ParsedView(view_name=k,region=ViewRegion(name=k,bbox=(0,0,v.shape[1],v.shape[0])),lines=lines.get(k,[]),circles=circles.get(k,[]),dimensions=dims.get(k,[]),px_per_mm=ppm.get(k,1.0)) for k,v in views.items()}
  t=time.time(); spec=await loop.run_in_executor(None,build_geometry,parsed); stages.append(StageResult(stage='geometry_building',success=True,duration_ms=(time.time()-t)*1000))
  t=time.time(); mesh=await loop.run_in_executor(None,build_mesh,spec); stages.append(StageResult(stage='mesh_construction',success=True,duration_ms=(time.time()-t)*1000))
  t=time.time(); glb,stats=await loop.run_in_executor(None,export_glb,mesh,job_id); stages.append(StageResult(stage='glb_export',success=True,duration_ms=(time.time()-t)*1000))
  res=ReconstructionResult(job_id=job_id,status='COMPLETED',glb_path=glb,stages=stages,mesh_stats=stats,geometry_spec=spec)
 except Exception as e:
  stages.append(StageResult(stage='pipeline',success=False,duration_ms=0,error=str(e))); res=ReconstructionResult(job_id=job_id,status='FAILED',stages=stages)
 _jobs[job_id]=res; return res

def get_job(job_id:str): return _jobs.get(job_id)
