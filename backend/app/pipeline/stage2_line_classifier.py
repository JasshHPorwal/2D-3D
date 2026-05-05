import cv2, numpy as np, math
from app.models.schema import DetectedLine, LineType
def detect_and_classify_lines(view_crops):
 out={}
 for n,img in view_crops.items():
  g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); b=cv2.bilateralFilter(g,9,75,75); m=np.median(b); lo=int(max(0,0.66*m)); hi=int(min(255,1.33*m)); e=cv2.Canny(b,lo,hi)
  l=cv2.HoughLinesP(e,1,np.pi/180,25,minLineLength=int((img.shape[0]**2+img.shape[1]**2)**0.5*0.03),maxLineGap=8)
  lines=[]
  if l is not None:
   for z in l[:,0]:
    x1,y1,x2,y2=map(float,z); pts=np.linspace([x1,y1],[x2,y2],15); vals=[g[int(max(0,min(g.shape[0]-1,p[1]))),int(max(0,min(g.shape[1]-1,p[0])))]<128 for p in pts]; d=sum(vals)/15
    t=LineType.SOLID if d>0.75 else LineType.DASHED if d>0.3 else LineType.CENTER
    lines.append(DetectedLine(x1=x1,y1=y1,x2=x2,y2=y2,line_type=t))
  out[n]=lines
 return out
