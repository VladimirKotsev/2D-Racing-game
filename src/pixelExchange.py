from PIL import Image
import os

COLOR_MAP = {
    (162, 38, 51): (19, 83, 181), # red -> blue
    (228, 59, 68): (94, 181, 212), # orange -> cyan
    (62, 39, 49): (41, 54, 59)
}

def replace_colors(image_path, output_filename):
    """Replaces colors in an image based on the COLOR_MAP dictionary."""
    image = Image.open(image_path).convert("RGBA")
    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            #print('old')
            #print('(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')')
            if (r, g, b) in COLOR_MAP:  # Replace if color is in the map
                pixels[x, y] = (*COLOR_MAP[(r, g, b)], a)
            #else:
                #print('(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')')


    # Save the image
    out_path = os.path.join(os.path.abspath("../assets/images/car/blue_car"), output_filename)
    image.save(out_path, format="PNG")
    print(f"Image saved to: {out_path}")

for i in range(7):  # Loops from 0 to 6 inclusive
    input_path = f"../assets/images/car/red_car/img_{i}.png"
    output_filename = f"img_{i}.png"
    replace_colors(input_path, output_filename)

