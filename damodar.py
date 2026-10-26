import os
import cv2
import numpy as np
import random
import math

# 1. Load Main Damodar Painting
img_path = 'damodar.jpg'
if not os.path.exists(img_path):
    print(f"Error: '{img_path}' nahi mili!")
    exit()

original_img = cv2.imread(img_path)
img = cv2.resize(original_img, (800, 800))
h, w, _ = img.shape

# 2. Load Black Background Morpankh Image
feather_path = 'morpankh.png'
if not os.path.exists(feather_path):
    print(f"Error: 'morpankh.png' nahi mili!")
    exit()

raw_feather = cv2.imread(feather_path, cv2.IMREAD_UNCHANGED)

# Black background ko transparent ya black blend karne ke liye clean setup
if raw_feather.shape[2] == 4:
    feather_img = raw_feather
else:
    # Convert RGB to RGBA by removing/making dark pixels transparent or handling black bg
    gray = cv2.cvtColor(raw_feather, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY) # Removes pure black background
    b, g, r = cv2.split(raw_feather)
    feather_img = cv2.merge((b, g, r, alpha))

# 3. Window Setup - Fullscreen Clean Setup
window_name = "Kartik Maas - Perfect Viral Reel | Gracy Builds"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 4. Phase 1: 11+ Morpankh flying slowly from bottom to top on glowing background
feather_steps = 200  # Slow and smooth timing
feathers_data = []
num_feathers = 12    # Exactly 12 feathers flying up

for _ in range(num_feathers):
    feathers_data.append({
        'x_start': random.randint(80, w - 80),
        'y_start': h + random.randint(20, 350),
        'size': random.randint(110, 160),
        'angle_speed': random.uniform(0.2, 0.6),
        'offset': random.uniform(0, 360)
    })

# Glowing background sparkles
sparkles = []
for _ in range(70):
    sparkles.append({
        'x': random.randint(0, w),
        'y': random.randint(0, h),
        'radius': random.randint(1, 3),
        'color': random.choice([(255, 255, 255), (0, 255, 255), (255, 0, 255), (0, 165, 255)])
    })

for step in range(feather_steps + 1):
    frame = np.full((h, w, 3), (20, 10, 35), dtype=np.uint8) # Rich dark glowing background
    
    # Twinkling sparkles
    for s in sparkles:
        cv2.circle(frame, (s['x'], s['y']), s['radius'], s['color'], -1)

    progress = step / feather_steps
    
    try:
        f_h, f_w = feather_img.shape[:2]
        for f in feathers_data:
            fy = int(f['y_start'] - (progress * (h + 400)))
            fx = int(f['x_start'] + 45 * math.sin(progress * 8 + f['offset']))
            f_size = f['size']
            
            if fy > -f_size:
                aspect_ratio = f_w / f_h
                curr_w, curr_h = int(f_size), int(f_size / aspect_ratio)
                resized_f = cv2.resize(feather_img, (curr_w, curr_h))
                
                angle = (step * f['angle_speed']) % 360
                M = cv2.getRotationMatrix2D((curr_w//2, curr_h//2), -angle, 1.0)
                rotated_f = cv2.warpAffine(resized_f, M, (curr_w, curr_h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
                
                y1, y2 = max(0, fy - curr_h//2), min(h, fy + curr_h//2)
                x1, x2 = max(0, fx - curr_w//2), min(w, fx + curr_w//2)
                
                if y2 - y1 > 0 and x2 - x1 > 0:
                    rf_y1 = max(0, -(fy - curr_h//2))
                    rf_x1 = max(0, -(fx - curr_w//2))
                    rf_y2 = rf_y1 + (y2 - y1)
                    rf_x2 = rf_x1 + (x2 - x1)
                    
                    if rotated_f.shape[2] == 4:
                        alpha_ch = rotated_f[:, :, 3] / 255.0
                        for c in range(3):
                            alpha = alpha_ch[rf_y1:rf_y2, rf_x1:rf_x2]
                            frame[y1:y2, x1:x2, c] = (alpha * rotated_f[rf_y1:rf_y2, rf_x1:rf_x2, c] + 
                                                       (1 - alpha) * frame[y1:y2, x1:x2, c])
                    else:
                        frame[y1:y2, x1:x2] = rotated_f[rf_y1:rf_y2, rf_x1:rf_x2]
    except Exception as e:
        pass

    cv2.imshow(window_name, frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# 5. Phase 2: Very Smooth and Slow Top-to-Bottom Image Reveal with Neon Line
reveal_steps = 150  # Super smooth & slow reveal for reel length
for step in range(reveal_steps + 1):
    frame = np.full((h, w, 3), (20, 10, 35), dtype=np.uint8)
    progress = step / reveal_steps
    
    current_height = int(progress * h)
    if current_height > 0:
        frame[0:current_height, :] = img[0:current_height, :]
        
    # Bright Neon Cyan & Magenta glowing line moving down as the image reveals
    if current_height < h:
        cv2.line(frame, (0, current_height), (w, current_height), (0, 255, 255), 4) # Neon Cyan
        cv2.circle(frame, (w // 2, current_height), 8, (255, 0, 255), -1)          # Magenta glowing core

    cv2.imshow(window_name, frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# 6. Final Clear Image Hold for Recording (Clean view, perfect for reels)
final_frame = img.copy()

for _ in range(200):  # Hold clear view for ~6-7 seconds so you can record easily
    cv2.imshow(window_name, final_frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()