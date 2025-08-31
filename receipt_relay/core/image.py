from PIL import Image
import io


def process_image(data: bytes, max_width: int) -> Image.Image:
    img = Image.open(io.BytesIO(data))
    img = img.convert('L')
    w, h = img.size
    if w > max_width:
        new_height = int(h * (max_width / w))
        img = img.resize((max_width, new_height))
    return img.convert('1')
