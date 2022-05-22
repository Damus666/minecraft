from settings import WIDTH,HEIGHT,MY_WIDTH,MY_HEIGHT

def width_calculator(desired_result,intt=False):
    divider = MY_WIDTH/desired_result
    pixels = WIDTH/divider
    if intt:
        return round(pixels)
    else:
        return pixels

def height_calculator(desired_result,intt=False):
    divider = MY_HEIGHT/desired_result
    pixels = HEIGHT/divider
    if intt:
        return round(pixels)
    else:
        return pixels

def medium_calculator(desired_result,intt=False):
    first = width_calculator(desired_result,intt)
    second = height_calculator(desired_result,intt)
    pixels = (first+second)/2
    if intt:
        return round(pixels)
    else:
        return pixels