import cv2
import numpy as np
import pandas as pd
import datetime
from sqlalchemy import create_engine
import time

conn = create_engine("postgresql+psycopg2://root:12345678@localhost:5432/plnstats").connect()

cap = cv2.VideoCapture(0)
(ret, frame) = cap.read()

capture_status = True



while capture_status:
    (ret, frame) = cap.read()

    result = frame.copy()
    size = result.size
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([168, 25, 0])
    upper = np.array([179, 255, 255])
    mask = cv2.inRange(image, lower, upper)
    result = cv2.bitwise_and(result, result, mask=mask)

    no_red = cv2.countNonZero(mask)
    frac_red = np.divide(float(no_red), size)
    percent_red = np.multiply((float(frac_red)), 100)

    if (percent_red >= 10.0):
        data_capture = {
            'color_percentage': percent_red,
            'created_on': datetime.datetime.now()
        }

        df = pd.DataFrame(columns=['color_percentage','created_on'],data=data_capture,index=[0])
        df.to_sql('home_pln_kwh_sensor', schema='public', con=conn, if_exists='append',index=False)



cap.release()
cv2.destroyAllWindows()