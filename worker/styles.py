import re


rotation = ["0.00","5.00","-5.00","0.00","0.00","0.00","0.00"]
scales = ["100","110","90","100","100","100","100"]
font_size_pt = 18

def gen_styles():
    styles = []
    count = 0
    for j in rotation:
        style = "Style: s" + str(count) + ", Roboto, 18, &H00FFFFFF , &H00FF0000, &H00FFFFFF , &H00000000 , -1, 0, 0, 0,100,100, 0, " + j + ", 1, 3 , 4, 3, 0, 0, 50, 0, 2\n" #30, 30, 30
        styles.append(style)
        count += 1
    return styles


##Alignment values are based on the numeric keypad layout. {\an1} - bottom left, {\an2} - bottom center, {\an3} - bottom right, {\an4} - center left, {\an5} - center center, {\an6} - center right, {\an7} - top left, {\an8} - top center, {\an9} - top right.


def calculate_text_height():
    """
    Calcule la hauteur en pixels d'un texte en fonction de la taille de la police en points.
    
    :param font_size_pt: Taille de la police en points.
    :param dpi: Résolution en DPI (par défaut 72 DPI, standard).
    :return: Hauteur en pixels.
    """
    dpi=72
    # Convertir la taille de la police de points à pouces
    height_in_inches = font_size_pt / 72.0
    
    # Convertir la hauteur de pouces à pixels
    height_in_pixels = height_in_inches * dpi
    
    return height_in_pixels


def remove_punctuation_and_whitespace(text):
    # Use regex to remove all non-alphabetic characters
    cleaned_text = re.sub(r'[^a-zA-Z]', '', text)
    return cleaned_text