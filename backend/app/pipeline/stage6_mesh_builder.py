import numpy as np, trimesh
from app.models.schema import *

def _mesh_for_feature(f:GeometricFeature):
 if f.type==FeatureType.BOX:
  m=trimesh.creation.box(extents=[f.dimensions_mm.get('x',1),f.dimensions_mm.get('y',1),f.dimensions_mm.get('z',1)])
 elif f.type in {FeatureType.CYLINDER,FeatureType.BORE,FeatureType.BOSS}:
  m=trimesh.creation.cylinder(radius=f.dimensions_mm.get('radius',1),height=f.dimensions_mm.get('height',1),sections=64)
  if f.axis=='X': m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
  elif f.axis=='Z': m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
 else:
  m=trimesh.creation.box(extents=[1,1,1])
 m.apply_translation(f.position_mm); return m

def build_mesh(spec:GeometrySpec):
 try:
  adds=[_mesh_for_feature(f) for f in spec.features if f.operation==CSGOperation.ADD]
  subs=[_mesh_for_feature(f) for f in spec.features if f.operation==CSGOperation.SUBTRACT]
  result=adds[0] if adds else trimesh.creation.box(extents=[spec.overall_width_mm,spec.overall_height_mm,spec.overall_depth_mm])
  for m in adds[1:]: result=trimesh.boolean.union([result,m])
  for m in subs: result=trimesh.boolean.difference([result,m])
 except Exception:
  result=trimesh.creation.box(extents=[spec.overall_width_mm,spec.overall_height_mm,spec.overall_depth_mm])
 trimesh.repair.fix_winding(result); trimesh.repair.fill_holes(result); result.merge_vertices();
 result.visual.vertex_colors=[180,180,185,255]
 return result
