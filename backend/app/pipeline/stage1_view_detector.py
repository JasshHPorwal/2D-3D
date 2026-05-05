import os, cv2, numpy as np
from app.core.config import get_settings

class ViewDetectionError(Exception): pass

def _iou(a,b):
 x1=max(a[0],b[0]); y1=max(a[1],b[1]); x2=min(a[2],b[2]); y2=min(a[3],b[3]); inter=max(0,x2-x1)*max(0,y2-y1)
 aa=(a[2]-a[0])*(a[3]-a[1]); bb=(b[2]-b[0])*(b[3]-b[1]); u=aa+bb-inter
 return inter/u if u else 0

def detect_views(image_bytes:bytes, job_id:str='debug')->dict[str,np.ndarray]:
 img=cv2.imdecode(np.frombuffer(image_bytes,np.uint8),cv2.IMREAD_COLOR)
 if img is None: raise ViewDetectionError('decode failed')
 g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); _,t=cv2.threshold(g,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
 cnts,_=cv2.findContours(t,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); h,w=g.shape; min_area=h*w*0.01
 boxes=[]
 for c in cnts:
  if cv2.contourArea(c)>=min_area:
   x,y,bw,bh=cv2.boundingRect(c); boxes.append((x,y,x+bw,y+bh))
 merged=[]
 for b in boxes:
  m=False
  for i,o in enumerate(merged):
   if _iou(b,o)>0.1:
    merged[i]=(min(b[0],o[0]),min(b[1],o[1]),max(b[2],o[2]),max(b[3],o[3])); m=True; break
  if not m: merged.append(b)
 if not merged: raise ViewDetectionError('zero views')
 mx,my=w/2,h/2; out={}
 if len(merged)==2:
  merged=sorted(merged,key=lambda b:(b[0]+b[2])/2); names=['front','side']
  for n,b in zip(names,merged):
   x1,y1,x2,y2=b; p=20; out[n]=img[max(0,y1-p):min(h,y2+p),max(0,x1-p):min(w,x2+p)]
 else:
  for b in merged:
   cx=(b[0]+b[2])/2; cy=(b[1]+b[3])/2
   name='side' if cx>mx and cy>my else 'front' if cx<mx and cy>my else 'top' if cx<mx and cy<my else None
   if name:
    x1,y1,x2,y2=b; p=20; out[name]=img[max(0,y1-p):min(h,y2+p),max(0,x1-p):min(w,x2+p)]
 s=get_settings(); d=os.path.join(s.UPLOAD_DIR,job_id,'debug'); os.makedirs(d,exist_ok=True)
 [cv2.imwrite(os.path.join(d,f'{k}.png'),v) for k,v in out.items()]
 if not out: raise ViewDetectionError('zero views')
 return out
