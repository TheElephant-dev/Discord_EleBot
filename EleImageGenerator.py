from PIL import Image
from PIL import Image, ImageDraw, ImageFont
import pathlib
import os



def GetFilePathOfImageMessage(AbuserName = 'AbuserName', VictimName = 'VictimName', MessageType = 'Generic'):
    CurrentDir = str(pathlib.Path().absolute())


    # make sure the path exists
    if not os.path.exists(f'{CurrentDir}/Assets/Images/temp'):
        os.makedirs(f'{CurrentDir}/Assets/Images/temp')
        print(f'Created {CurrentDir}/Assets/Images/temp')



    img = returnCreatedImage(CurrentDir, AbuserName, VictimName, MessageType)





    #Save the image into a temp file
    img.save(CurrentDir + '/Assets/Images/temp/LatestAbuseImage.png')
    return CurrentDir + '/Assets/Images/temp/LatestAbuseImage.png'


























######################################## Image Creation


def returnCreatedImage(CurrentDir, AbuserName, VictimName, MessageType):
    # Create The Fonts
    HappyFont_Large = ImageFont.truetype(CurrentDir + '/Assets/Fonts/CheerfulScript.ttf', 70)

    StampFont_Large = ImageFont.truetype(CurrentDir + '/Assets/Fonts/old_stamper.ttf', 45)

    NormalFont_Large = ImageFont.truetype(CurrentDir + '/Assets/Fonts/Uni Sans.ttf', 65)
    NormalFont_Mid = ImageFont.truetype(CurrentDir + '/Assets/Fonts/Uni Sans.ttf', 30)
    NormalFont_Small = ImageFont.truetype(CurrentDir + '/Assets/Fonts/Uni Sans.ttf', 20)
    if MessageType == 'Generic':
        img = Image.new('RGB', (100, 30), color=(73, 109, 137))
        Draw = ImageDraw.Draw(img)
        Draw.text((10, 10), "Hello world", font=NormalFont_Mid, fill=(255, 255, 0))
        return img
    elif MessageType == 'AbuseMessageToAbuser':
        # Grab a backround template
        img = Image.open(CurrentDir + "/Assets/Images/AbuserWarningTemplate.png")

        # Edit the image
        Draw = ImageDraw.Draw(img)

        Draw.text((10, 10), f"Hello {AbuserName}", font=StampFont_Large, fill=(100, 20, 20))
        Draw.text((130, 70), f"Please Stop with the ", font=NormalFont_Mid, fill=(200, 200, 200))
        Draw.text((60, 100), f"fuc*ing abuse", font=HappyFont_Large, fill=(20, 20, 20))
        Draw.text((10, 230), f"Im sure {VictimName} is sick of your sh*t.", font=NormalFont_Mid, fill=(200, 200, 200))
        Draw.text((380, 270), f"K tnx bye  -TheElephant", font=NormalFont_Small, fill=(100, 100, 100))

    elif MessageType == 'AbuseMessageToVictim':
        # Grab a backround template
        img = Image.open(CurrentDir + "/Assets/Images/AbuserWarningTemplate.png")

        # Edit the image
        Draw = ImageDraw.Draw(img)

        Draw.text((10, 10), f"Hello {VictimName}", font=StampFont_Large, fill=(20, 100, 20))
        Draw.text((130, 70), f"{AbuserName} Wont Stop with the ", font=NormalFont_Mid, fill=(200, 200, 200))
        Draw.text((60, 100), f"fuc*ing abuse", font=HappyFont_Large, fill=(20, 20, 20))
        Draw.text((380, 270), f"K tnx bye  -TheElephant", font=NormalFont_Small, fill=(100, 100, 100))
    else:
        print('returnCreatedImage Error with', CurrentDir, AbuserName, VictimName, MessageType)





    return img