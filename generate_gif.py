from PIL import Image, ImageDraw, ImageFont
import os, re

W, H = 900, 550
BG = (15, 15, 25)
FG = (200, 200, 200)

font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 16)
title_font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 18)

def read_clean(path):
    lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            line = re.sub(r'\x1b\[[0-9;]*m', '', line)
            line = re.sub(r'\x1b\]8;;.*?\x1b\\', '', line)
            line = line.replace('\u00b7', '\u25cb')
            lines.append(line)
    return lines

def draw_frame(lines_text, title):
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 45], fill=(25, 25, 40))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([15 + i*22, 12, 31 + i*22, 28], fill=c)
    draw.text((100, 12), title, fill=FG, font=title_font)
    y = 80
    for line in lines_text:
        draw.text((30, y), line, fill=(180, 180, 180), font=font)
        y += 28
    return img

full_lines = read_clean('assets/full.txt')
compact_lines = read_clean('assets/compact.txt')
ascii_lines = read_clean('assets/ascii.txt')
bare_lines = read_clean('assets/bare.txt')

formats = [
    ('Full View (Default)', full_lines),
    ('Compact Mode', compact_lines),
    ('ASCII Mode', ascii_lines),
    ('Bare Mode (Plain Text)', bare_lines),
]

frames = [draw_frame(['  ' + l for l in lines], title) for title, lines in formats]

frames[0].save(
    'assets/statusline-demo.gif',
    save_all=True,
    append_images=frames[1:],
    duration=2000,
    loop=0,
    optimize=True,
)
size = os.path.getsize('assets/statusline-demo.gif')
print(f'GIF saved: assets/statusline-demo.gif ({size/1024:.1f} KB)')
