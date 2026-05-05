from enum import Enum
from pydantic import BaseModel, ConfigDict

class LineType(str, Enum): SOLID='SOLID'; DASHED='DASHED'; CENTER='CENTER'
class FeatureType(str, Enum): CYLINDER='CYLINDER'; BOX='BOX'; CHAMFER='CHAMFER'; SLOT='SLOT'; BOSS='BOSS'; BORE='BORE'; FILLET='FILLET'
class CSGOperation(str, Enum): ADD='ADD'; SUBTRACT='SUBTRACT'
class ViewRegion(BaseModel): model_config=ConfigDict(from_attributes=True); name:str; bbox:tuple[int,int,int,int]
class DetectedLine(BaseModel): model_config=ConfigDict(from_attributes=True); x1:float; y1:float; x2:float; y2:float; line_type:LineType
class DetectedCircle(BaseModel): model_config=ConfigDict(from_attributes=True); cx:float; cy:float; radius_px:float; line_type:LineType; view:str
class DimensionAnnotation(BaseModel): model_config=ConfigDict(from_attributes=True); value_mm:float; is_diameter:bool; position_px:tuple[float,float]; view:str
class ParsedView(BaseModel): model_config=ConfigDict(from_attributes=True); view_name:str; region:ViewRegion; lines:list[DetectedLine]=[]; circles:list[DetectedCircle]=[]; dimensions:list[DimensionAnnotation]=[]; px_per_mm:float=1.0
class GeometricFeature(BaseModel): model_config=ConfigDict(from_attributes=True); type:FeatureType; operation:CSGOperation; position_mm:tuple[float,float,float]; dimensions_mm:dict[str,float]; axis:str='Y'; label:str=''
class GeometrySpec(BaseModel): model_config=ConfigDict(from_attributes=True); overall_width_mm:float; overall_height_mm:float; overall_depth_mm:float; features:list[GeometricFeature]
class MeshStats(BaseModel): model_config=ConfigDict(from_attributes=True); vertex_count:int; face_count:int; bbox_x_mm:float; bbox_y_mm:float; bbox_z_mm:float; is_watertight:bool; volume_mm3:float|None
class StageResult(BaseModel): model_config=ConfigDict(from_attributes=True); stage:str; success:bool; duration_ms:float; error:str|None=None
class ReconstructionResult(BaseModel): model_config=ConfigDict(from_attributes=True); job_id:str; status:str; glb_path:str|None=None; stages:list[StageResult]=[]; mesh_stats:MeshStats|None=None; geometry_spec:GeometrySpec|None=None
