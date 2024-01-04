rotation = ["0.00","5.00","-5.00","0.00","0.00","0.00","0.00"]
scales = ["100","110","90","100","100","100","100"]

def gen_styles():
    styles = []
    count = 0
    for j in rotation:
        style = "Style: s" + str(count) + ", Roboto, 18, &H00FFFFFF , &H00FF0000, &H00FFFFFF , &H00000000 , -1, 0, 0, 0,100,100, 0, " + j + ", 1, 3 , 4, 3, 0, 0, 50, 0, 2\n" #30, 30, 30
        styles.append(style)
        count += 1
    return styles


##Alignment values are based on the numeric keypad layout. {\an1} - bottom left, {\an2} - bottom center, {\an3} - bottom right, {\an4} - center left, {\an5} - center center, {\an6} - center right, {\an7} - top left, {\an8} - top center, {\an9} - top right.