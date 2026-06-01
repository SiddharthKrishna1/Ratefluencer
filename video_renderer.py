import hashlib
import math
import tempfile
from pathlib import Path

try:
    import imageio.v2 as imageio
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    imageio = None
    np = None
    Image = None
    ImageDraw = None
    ImageFont = None


WIDTH = 720
HEIGHT = 1280
FPS = 12


def _ensure_video_dependencies():
    global imageio, np, Image, ImageDraw, ImageFont
    if imageio is not None and np is not None and Image is not None:
        return

    try:
        import imageio.v2 as imageio_import
        import numpy as np_import
        from PIL import Image as PILImage, ImageDraw as PILImageDraw, ImageFont as PILImageFont
    except ImportError as exc:
        raise RuntimeError("MP4 rendering dependencies are missing. Run pip install -r requirements.txt and restart Streamlit.") from exc

    imageio = imageio_import
    np = np_import
    Image = PILImage
    ImageDraw = PILImageDraw
    ImageFont = PILImageFont


def _font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def _wrap_text(draw, text, font, max_width):
    words = str(text).split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _draw_wrapped(draw, text, xy, font, fill, max_width, line_gap=8, align="left"):
    x, y = xy
    lines = _wrap_text(draw, text, font, max_width)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_x = x
        if align == "center":
            line_x = x + (max_width - line_width) / 2
        draw.text((line_x, y), line, font=font, fill=fill)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def _scene_duration_seconds(scene, fallback=8):
    time_text = str(scene.get("time", ""))
    parts = time_text.lower().replace("s", "").split("-")
    if len(parts) == 2:
        try:
            return max(3, min(15, float(parts[1]) - float(parts[0])))
        except ValueError:
            return fallback
    return fallback


def _palette(seed_text):
    digest = hashlib.sha256(seed_text.encode("utf-8")).hexdigest()
    hue = int(digest[:2], 16)
    return (
        (7, 17 + hue % 20, 31 + hue % 34),
        (20 + hue % 50, 184, 166),
        (56, 189, 248),
        (245, 158, 11),
    )


def _draw_gradient(draw, frame_index, total_frames, topic):
    base, teal, blue, amber = _palette(topic)
    progress = frame_index / max(total_frames - 1, 1)
    for y in range(HEIGHT):
        mix = y / HEIGHT
        pulse = int(16 * math.sin((progress * math.pi * 2) + mix * 3))
        r = int(base[0] * (1 - mix) + 14 * mix) + pulse
        g = int(base[1] * (1 - mix) + 24 * mix) + pulse
        b = int(base[2] * (1 - mix) + 45 * mix) + pulse
        draw.line([(0, y), (WIDTH, y)], fill=(max(0, r), max(0, g), max(0, b)))

    orb_x = int(WIDTH * (0.2 + 0.6 * progress))
    draw.ellipse((orb_x - 260, 70, orb_x + 260, 590), fill=(*teal, 38))
    draw.ellipse((WIDTH - orb_x - 220, 700, WIDTH - orb_x + 220, 1160), fill=(*amber, 32))
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=(60, 80, 100), width=3)


def _render_scene_frame(package, scene, scene_index, frame_index, total_frames):
    topic = package.get("title", "Ratefluencer Reel")
    image = Image.new("RGB", (WIDTH, HEIGHT), (7, 7, 15))
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    _draw_gradient(draw, frame_index, total_frames, topic)

    title_font = _font(58, bold=True)
    label_font = _font(24, bold=True)
    body_font = _font(30)
    small_font = _font(22)
    subtitle_font = _font(32, bold=True)

    draw.rounded_rectangle((42, 42, WIDTH - 42, 100), radius=22, fill=(15, 23, 42, 190), outline=(103, 232, 249, 105), width=2)
    draw.text((64, 57), "RATEFLUENCER AI REEL", font=label_font, fill=(167, 243, 208))
    draw.text((WIDTH - 160, 57), str(scene.get("time", "")), font=label_font, fill=(248, 250, 252))

    scene_badge = f"SCENE {scene_index + 1}"
    draw.rounded_rectangle((52, 150, 190, 194), radius=20, fill=(103, 232, 249, 230))
    draw.text((74, 161), scene_badge, font=small_font, fill=(7, 17, 31))

    y = 235
    y = _draw_wrapped(
        draw,
        scene.get("on_screen_text", ""),
        (52, y),
        title_font,
        (248, 250, 252),
        WIDTH - 104,
        line_gap=12,
    )

    draw.rounded_rectangle((52, 610, WIDTH - 52, 840), radius=28, fill=(15, 23, 42, 180), outline=(148, 163, 184, 70), width=2)
    _draw_wrapped(
        draw,
        scene.get("visual", ""),
        (82, 640),
        body_font,
        (203, 213, 225),
        WIDTH - 164,
        line_gap=10,
    )

    draw.rounded_rectangle((42, HEIGHT - 238, WIDTH - 42, HEIGHT - 66), radius=28, fill=(0, 0, 0, 160), outline=(255, 255, 255, 45), width=2)
    _draw_wrapped(
        draw,
        scene.get("voiceover", ""),
        (66, HEIGHT - 210),
        subtitle_font,
        (248, 250, 252),
        WIDTH - 132,
        line_gap=8,
        align="center",
    )

    progress_width = int((WIDTH - 84) * ((frame_index + 1) / max(total_frames, 1)))
    draw.rounded_rectangle((42, HEIGHT - 34, WIDTH - 42, HEIGHT - 22), radius=6, fill=(30, 41, 59, 230))
    draw.rounded_rectangle((42, HEIGHT - 34, 42 + progress_width, HEIGHT - 22), radius=6, fill=(103, 232, 249, 255))

    return Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")


def generate_reel_mp4(package):
    _ensure_video_dependencies()

    scenes = package.get("scenes") or []
    if not scenes:
        raise ValueError("No scenes available to render.")

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        output_path = Path(tmp.name)

    try:
        with imageio.get_writer(output_path, fps=FPS, codec="libx264", quality=8, macro_block_size=16) as writer:
            for scene_index, scene in enumerate(scenes[:6]):
                duration = _scene_duration_seconds(scene)
                total_frames = max(1, int(duration * FPS))
                for frame_index in range(total_frames):
                    frame = _render_scene_frame(package, scene, scene_index, frame_index, total_frames)
                    writer.append_data(np.asarray(frame))

        data = output_path.read_bytes()
    finally:
        try:
            output_path.unlink(missing_ok=True)
        except OSError:
            pass

    return data
