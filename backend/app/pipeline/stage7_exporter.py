import os
from app.core.config import get_settings
from app.models.schema import MeshStats

def export_glb(mesh,job_id:str):
 s=get_settings(); p=f"{s.UPLOAD_DIR}/{job_id}"; os.makedirs(p,exist_ok=True); gp=f"{p}/model.glb"
 mesh.export(gp,file_type='glb')
 if not os.path.exists(gp) or os.path.getsize(gp)==0: raise RuntimeError('glb export failed')
 e=mesh.bounding_box.extents
 stats=MeshStats(vertex_count=len(mesh.vertices),face_count=len(mesh.faces),bbox_x_mm=float(e[0]),bbox_y_mm=float(e[1]),bbox_z_mm=float(e[2]),is_watertight=bool(mesh.is_watertight),volume_mm3=float(mesh.volume) if mesh.is_watertight else None)
 return gp,stats
