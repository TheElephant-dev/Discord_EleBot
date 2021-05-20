from PIL import Image
from PIL import Image, ImageDraw, ImageFont
import pathlib
import os
import io
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import matplotlib as mpl
import numpy as np








def getimg_OfAuditGraph(StaticYSize = 20, ListOfDates = ['01/02/1991'], DataEntries = [1], RGB = [200, 200, 200]):
    datetimedates = [dt.datetime.strptime(d, '%m/%d/%Y').date() for d in ListOfDates]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.xlim(0, len(ListOfDates))
    plt.ylim(0, StaticYSize)

    PointAmount = list(range(len(DataEntries)))
    plt.plot(PointAmount, DataEntries, color=[RGB[0] / 255, RGB[1] / 255, RGB[2] / 255])
    plt.gcf().autofmt_xdate()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    im = Image.open(buf)
    return im
    buf.close()




def getimgarray_OfAuditGraph(dates, AllAuditData):
    imgarray = []
    for AuditDataEntry in AllAuditData:
        imgarray.append(getimg_OfAuditGraph(StaticYSize=20, ListOfDates=dates, DataEntries=AuditDataEntry, RGB=[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))
    return imgarray






#Create Data

AuditData = []
GraphableFactors = ['Mutes', 'Warns', 'Audits']
ListOfDates = ['01/02/1991','01/03/1991','01/04/1991','01/05/1991','01/06/1991','01/07/1991','01/08/1991']


for DataType in range(len(GraphableFactors)):
    DataOfDay = []
    for GraphableFactor in GraphableFactors:
        DataOfDay.append(random.randint(0, 20))
    AuditData.append(DataOfDay)


print(AuditData)

DataTypesAmount = 8
#ListOfDates = ['01/02/1991','01/03/1991']

imgArray = getimgarray_OfAuditGraph(ListOfDates, AuditData)

# im.show()
for imgNum in range(len(imgArray)):
    if imgNum + 1 == len(imgArray):
        imgArray[imgNum].show()
    #
    # else:
    #     print(f'imgNum({imgNum}) != len(imgArray)({len(imgArray)})')