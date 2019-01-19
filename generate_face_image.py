from __future__ import print_function
import sys
import os
import argparse
import cv2
import dlib

parser = argparse.ArgumentParser(description='Generate Face Photo')
parser.add_argument('--num', '-n', type=int, default=-1,
                    help='number of photo to take')
parser.add_argument('--device', '-d', type=int, default=0,
                    help='device number(default 0)')
parser.add_argument('--outputdir', '-o', default='',
                    help='学習データのディレクトリ')
args = parser.parse_args()

if args.num == -1 or args.outputdir == "":
    parser.print_help()
    sys.exit(1)


try:
    if os.path.isdir(args.outputdir):
        print("{} is exits (ok)".format(args.outputdir))
    else:
        print("{} doesn't exits".format(args.outputdir))
        print('creating {}'.format(args.outputdir))
        os.mkdir(args.outputdir)
except Exception:
    print("can't create {}".format(args.outputdir))
    sys.exit()

cap = cv2.VideoCapture(args.device)

detector = dlib.get_frontal_face_detector()
count = 0

while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray, 1)

    for i, d in enumerate(faces):
        color = (0, 255, 0)
        pen_w = 2
        if d.right() - d.left() < 100 / 2 or d.bottom() - d.top() < 100 / 2:
            print('detected face is too small.')
            continue
        x = d.left()
        y = d.top()
        w = d.right() - x
        h = d.bottom() - y
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness=pen_w)
        count += 1
        cv2.imwrite(args.outputdir + "\\" + "test" + "_" +
                    str(count) + ".jpg", gray[y:y + h, x:x + w])
        sys.stderr.write(args.outputdir + "\\" + "test" + "_" +
                    str(count) + ".jpg\n")
        cv2.imshow("frame", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    elif count > args.num:
        break

cap.release()
cv2.destroyAllWindows()
