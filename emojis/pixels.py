from PIL import Image

# Open the image file
image = Image.open("./images/1.png")

# Get the width and height of the image
width, height = image.size

# Print the width and height
print("Width:", width)
print("Height:", height)

###emojis en 72x72 pixels