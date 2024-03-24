from PIL import Image, ImageDraw, ImageFont
import io
import textwrap


class ImageService:
    def __init__(self):
        pass

    def createImageSmeme(self, data):
        validate = self.validateInputImage(data)
        if validate:
            return validate

        img = self.load_image_from_base64(data['image']['data'])
        img = img.resize((460, 460), Image.ANTIALIAS)
        draw = ImageDraw.Draw(img)
        img_width, img_height = img.size
        header_font_size, footer_font_size = self.hitung_font_size(img_width, img_height)

        header_font_size = int(header_font_size)
        footer_font_size = int(footer_font_size)
        watermark_font_size = 15

        header_text = data['header'].upper()
        footer_text = data['footer'].upper()
        watermark_text = data['watermark']

        self.add_header_text(draw, header_text, img_width, img_height, header_font_size)
        self.add_footer_text(draw, footer_text, img_width, img_height, footer_font_size)
        self.add_watermark_text(draw, watermark_text, img_width, img_height, watermark_font_size)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")

        return {'img': buffer.getvalue(), 'status': 200, 'type': 'image/png'}

    @staticmethod
    def load_image_from_base64(base64_data):
        return Image.open(io.BytesIO(base64_data))

    @staticmethod
    def hitung_font_size(img_width, img_height):
        if img_width < 500 and img_height < 500:
            header_font_size = 45
            footer_font_size = 45
        elif img_width < 1000 and img_height < 1000:
            header_font_size = 55
            footer_font_size = 55
        else:
            header_font_size = 50
            footer_font_size = 50

        return header_font_size, footer_font_size

    @staticmethod
    def add_header_text(draw, header_text, img_width, img_height, font_size):
        font = ImageFont.truetype("public/assets/arial_bold.ttf", font_size)
        max_text_width = 12
        wrapped_lines = textwrap.wrap(header_text, width=max_text_width)

        position_y = 25
        for line in wrapped_lines:
            text_width, text_height = draw.textsize(line, font=font)
            position_x = (img_width - text_width) // 2

            if position_y + text_height > img_height:
                position_y = 25
                position_y += text_height
                if position_y + text_height > img_height:
                    break

            stroke_color = "black"
            draw.text((position_x - 1, position_y), line, font=font, fill=stroke_color)
            draw.text((position_x + 1, position_y), line, font=font, fill=stroke_color)
            draw.text((position_x, position_y - 1), line, font=font, fill=stroke_color)
            draw.text((position_x, position_y + 1), line, font=font, fill=stroke_color)
            draw.text((position_x, position_y), line, font=font, fill="white")

            position_y += text_height + 5

    @staticmethod
    def add_footer_text(draw, footer_text, img_width, img_height, font_size):
        font = ImageFont.truetype("public/assets/arial_bold.ttf", font_size)
        max_text_width = 12
        wrapped_lines = textwrap.wrap(footer_text, width=max_text_width)

        position_y = img_height - 45
        for line in wrapped_lines[::-1]:
            text_width, text_height = draw.textsize(line, font=font)
            position_x = (img_width - text_width) // 2

            if position_y - text_height < 0:
                break

            stroke_color = "black"
            draw.text((position_x - 1, position_y - text_height), line, font=font, fill=stroke_color)
            draw.text((position_x + 1, position_y - text_height), line, font=font, fill=stroke_color)
            draw.text((position_x, position_y - text_height - 1), line, font=font, fill=stroke_color)
            draw.text((position_x, position_y - text_height + 1), line, font=font, fill=stroke_color)
            draw.text((position_x, position_y - text_height), line, font=font, fill="white")

            position_y -= (text_height + 5)

    @staticmethod
    def add_watermark_text(draw, watermark_text, img_width, img_height, font_size):
        font = ImageFont.truetype("public/assets/arial.ttf", font_size)
        text_width, text_height = draw.textsize(watermark_text, font=font)
        position = (10, img_height - text_height - 10)
        draw.text(position, watermark_text, font=font, fill="white")

    @staticmethod
    def validateInputImage(data):
        if data is None:
            return {'message': 'Data not found', 'status': 400}
        if data['header'] == '':
            return {'message': 'Header is required', 'status': 400}
        if data['image'] == '':
            return {'message': 'Image is required', 'status': 400}
        if data['image'] != '':
            if data['image']['ext'] not in ['jpg', 'jpeg', 'png', 'webp']:
                return {'message': 'Format gambar tidak didukung', 'status': 400}
            elif data['image']['size'] > 3000000:
                return {'message': 'Ukuran gambar terlalu besar', 'status': 400}
        return None
