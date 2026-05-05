import re, cv2, numpy as np, pytesseract
from app.models.schema import DimensionAnnotation

def read_dimensions(view_crops):
 dims={}; scales={}
 for vn,img in view_crops.items():
  g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); inv=255-g
  cnts,_=cv2.findContours(inv,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  ann=[]
  for c in cnts:
   a=cv2.contourArea(c)
   if 50<a<3000:
    x,y,w,h=cv2.boundingRect(c); x0=max(0,x-10); y0=max(0,y-10); x1=min(g.shape[1],x+w+10); y1=min(g.shape[0],y+h+10)
    roi=g[y0:y1,x0:x1]
    txt=pytesseract.image_to_string(roi,config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789.Ø⌀φO')
    raw=txt.strip(); num=re.sub(r'[^0-9.]','',raw)
    if not num: continue
    v=float(num)
    if v==0: continue
    ann.append(DimensionAnnotation(value_mm=v,is_diameter=bool(re.match(r'^[Ø⌀φO]',raw)),position_px=(float(x+w/2),float(y+h/2)),view=vn))
  dims[vn]=ann
  lines=cv2.HoughLinesP(cv2.Canny(g,50,150),1,np.pi/180,20,minLineLength=30,maxLineGap=5)
  lens=[]
  if lines is not None:
   for l in lines[:,0]:
    x1,y1,x2,y2=l; ang=abs(np.degrees(np.arctan2(y2-y1,x2-x1)))
    if ang<5 or abs(ang-90)<5: lens.append(float(np.hypot(x2-x1,y2-y1)))
  scales[vn]=(max(lens)/max([d.value_mm for d in ann])) if lens and ann else 5.9
 return dims,scales
