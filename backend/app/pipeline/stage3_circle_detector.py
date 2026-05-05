import cv2, numpy as np
from app.models.schema import DetectedCircle, LineType
def detect_circles(view_crops):
 out={}
 for n,img in view_crops.items():
  g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); b=cv2.GaussianBlur(g,(5,5),1.5); md=min(g.shape[:2])
  cs=cv2.HoughCircles(b,cv2.HOUGH_GRADIENT,1.2,minDist=max(8,md*0.08),param1=50,param2=28,minRadius=max(3,int(md*0.01)),maxRadius=int(md*0.45))
  found=[]
  if cs is not None:
   for c in np.round(cs[0]).astype(int):
    cx,cy,r=map(float,c); dens=[]
    for a in np.linspace(0,2*np.pi,8,endpoint=False):
      x=int(np.clip(cx+(r+2)*np.cos(a),0,g.shape[1]-1)); y=int(np.clip(cy+(r+2)*np.sin(a),0,g.shape[0]-1)); dens.append(g[y,x]<128)
    d=sum(dens)/len(dens); t=LineType.SOLID if d>0.75 else LineType.DASHED if d>0.3 else LineType.CENTER
    found.append(DetectedCircle(cx=cx,cy=cy,radius_px=r,line_type=t,view=n))
  ded=[]
  for c in sorted(found,key=lambda q:q.radius_px,reverse=True):
   if not any((c.cx-o.cx)**2+(c.cy-o.cy)**2<25 for o in ded): ded.append(c)
  out[n]=ded
 return out
