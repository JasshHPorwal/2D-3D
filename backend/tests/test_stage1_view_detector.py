import cv2, numpy as np
from app.pipeline.stage1_view_detector import detect_views

def test_detect_views():
 img=np.full((1000,1400,3),255,np.uint8)
 cv2.rectangle(img,(100,50),(500,300),(0,0,0),-1)
 cv2.rectangle(img,(120,600),(520,900),(0,0,0),-1)
 cv2.rectangle(img,(800,620),(1200,920),(0,0,0),-1)
 ok,b=cv2.imencode('.png',img); out=detect_views(b.tobytes(),'t1')
 assert len(set(out.keys()) & {'top','front','side'})>=2
 assert all(v.size>0 for v in out.values())
