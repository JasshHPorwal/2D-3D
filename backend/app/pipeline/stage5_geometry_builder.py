from app.models.schema import *

def build_geometry(parsed_views:dict[str,ParsedView])->GeometrySpec:
 w=h=d=100.0
 if 'front' in parsed_views:
  f=parsed_views['front']; w=max([abs(l.x2-l.x1) for l in f.lines]+[w])/max(f.px_per_mm,1e-6); h=max([abs(l.y2-l.y1) for l in f.lines]+[h])/max(f.px_per_mm,1e-6)
 if 'side' in parsed_views:
  s=parsed_views['side']; d=max([abs(l.x2-l.x1) for l in s.lines]+[d])/max(s.px_per_mm,1e-6)
 feats=[GeometricFeature(type=FeatureType.BOX,operation=CSGOperation.ADD,position_mm=(0,0,0),dimensions_mm={'x':w,'y':h,'z':d},label='Base solid')]
 for v in parsed_views.values():
  for c in v.circles:
   r=c.radius_px/max(v.px_per_mm,1e-6); axis='Y' if c.view=='top' else 'Z' if c.view=='front' else 'X'; inside=True
   op=CSGOperation.SUBTRACT if inside else CSGOperation.ADD
   ft=FeatureType.BORE if op==CSGOperation.SUBTRACT else FeatureType.CYLINDER
   ht={'X':w,'Y':h,'Z':d}[axis]
   feats.append(GeometricFeature(type=ft,operation=op,position_mm=(c.cx/v.px_per_mm,c.cy/v.px_per_mm,0),dimensions_mm={'radius':r,'height':ht},axis=axis,label=f"Hole Ø{2*r:.0f}mm" if op==CSGOperation.SUBTRACT else f"Boss Ø{2*r:.0f}mm"))
 add=[f for f in feats if f.operation==CSGOperation.ADD]; sub=[f for f in feats if f.operation==CSGOperation.SUBTRACT]
 return GeometrySpec(overall_width_mm=w,overall_height_mm=h,overall_depth_mm=d,features=add+sub)
