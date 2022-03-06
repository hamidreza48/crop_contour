def crop_contour(img):
    blur1 = cv2.medianBlur(img, 15)
    blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)
    _, im_bw = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours,_ = cv2.findContours(im_bw.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    
    if len(contours) >= 1:
      cnt = max(contours, key=cv2.contourArea)
      print(cv2.contourArea(cnt))
      if cv2.contourArea(cnt) > 2000:
        x, y, w, h = cv2.boundingRect(cnt)
        # cv2.rectangle(img, (x,y),(x+w,y+h),(255,0,255),2)
        # img = img[y:y + h, x:x + w]
    ((x, y), radius) = cv2.minEnclosingCircle(cnt)
    # cv2.circle(img, (int(x), int(y)), int(radius), (255, 0, 255), 2)
    M = cv2.moments(cnt)
    center_x = int(M['m10'] / M['m00'])
    center_y = int(M['m01'] / M['m00'])
    # cv2.circle(img, (center_x,center_y), 130, (255, 255, 255), 1)
    # cv2_imshow(img)
    print(center_x, center_y)
    center_x = int(M['m10'] / M['m00'])
    center_y = int(M['m01'] / M['m00'])
    # cv2.circle(img, (center_x,center_y), 130, (255, 255, 255), 1)
    print('shape', img.shape[0], img.shape[1])
    radius = int(max(img.shape[0], img.shape[1]))
    print('radius' , radius)
    x = int(center_x+radius)
    y = int(center_y)
    d = 1
    t = math.pi/180*d
    
    while True:
      while inRect((x,y), img.shape[1], img.shape[0])==False or img[y,x] == 0 :
        d = d + 1
        if d > 360:
          break
        t = math.pi/180*d
        x = int(center_x+radius*math.cos(t))
        y = int(center_y-radius*math.sin(t))
      
      if inRect((x,y), img.shape[1], img.shape[0])==True and img[y,x] != 0:
        print('pixel', img[y,x])
        break
     
      radius = radius - 3
      d = 0
      t = math.pi/180*d
      x = int(center_x+radius*math.cos(t))
      y = int(center_y-radius*math.sin(t))
    
    
    
    print(center_x, center_y)
    x = center_x - radius
    y = center_y - radius
    w = h = 2 * radius
    if center_x < radius:
      x = 0
      w =radius+center_x
    if center_y < radius:
      y = 0
      h = radius+center_y  
    if center_x+radius > img.shape[1]:
      w = img.shape[1] - x  
    if center_y+radius> img.shape[0]:
      h = img.shape[0] - y  
    # cv2.circle(img, (center_x,center_y), radius, (255, 255, 255), 1)
    # cv2_imshow(img)
    cv2_imshow(img)
    img = img[y:y+h , x:x+w]
    print('image cropping')

    # img = img[y:y + h, x:x + w]
    # cv2_imshow(img)    
    return img
