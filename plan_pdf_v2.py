import io
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader


# ---------- ASSETS ----------

def find_arabic_font():
    candidates = [
        Path.home() / "Library/Fonts/NotoKufiArabic[wght].ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/noto/NotoKufiArabic-Regular.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoKufiArabic-Regular.ttf"),
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    for base in [
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
    ]:
        if base.exists():
            matches = list(base.glob("**/NotoKufiArabic*.ttf"))
            if matches:
                return matches[0]

    raise FileNotFoundError(
        "Noto Kufi Arabic font was not found on this system."
    )


FONT_PATH = find_arabic_font()
LAMA_IMAGE_PATH = Path("lama_hero.jpg")

FONT_NAME = "RootsArabic"


# ---------- BRAND COLORS ----------

CREAM = HexColor("#FFF9F5")
SOFT_CREAM = HexColor("#FCF5F2")

BLUSH = HexColor("#F5DDE3")
ROSE = HexColor("#CB8CA2")

LILAC = HexColor("#E9DDF2")
PURPLE = HexColor("#A78BBC")

PLUM = HexColor("#523C47")
BODY = HexColor("#6C5962")
MUTED = HexColor("#9B858E")

WHITE = HexColor("#FFFFFF")
BORDER = HexColor("#EBD9DF")


# ---------- ARABIC ----------

def prepare_arabic(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


def wrap_arabic_text(text, font_name, font_size, max_width):
    words = str(text).split()

    lines = []
    current = ""

    for word in words:

        candidate = f"{current} {word}".strip()

        width = pdfmetrics.stringWidth(
            prepare_arabic(candidate),
            font_name,
            font_size
        )

        if width <= max_width:
            current = candidate

        else:
            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


def draw_rtl_lines(
    pdf,
    text,
    x_right,
    y,
    max_width,
    font_size=11,
    leading=22,
    color=BODY
):
    pdf.setFillColor(color)
    pdf.setFont(FONT_NAME, font_size)

    lines = wrap_arabic_text(
        text,
        FONT_NAME,
        font_size,
        max_width
    )

    for line in lines:

        pdf.drawRightString(
            x_right,
            y,
            prepare_arabic(line)
        )

        y -= leading

    return y


# ---------- DESIGN HELPERS ----------

def draw_page_background(pdf):
    width, height = A4

    pdf.setFillColor(CREAM)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # soft decorative circles
    pdf.setFillColor(BLUSH)
    pdf.circle(
        width + 20,
        height - 40,
        115,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(LILAC)
    pdf.circle(
        -25,
        70,
        90,
        fill=1,
        stroke=0
    )


def draw_brand(pdf):
    width, height = A4

    pdf.setFillColor(PLUM)
    pdf.setFont(FONT_NAME, 9)

    pdf.drawRightString(
        width - 42,
        height - 38,
        prepare_arabic("جذور مع لمى")
    )

    pdf.setFillColor(ROSE)
    pdf.roundRect(
        width - 154,
        height - 52,
        112,
        3,
        2,
        fill=1,
        stroke=0
    )


def draw_footer(pdf, page_number):
    width, _ = A4

    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.5)

    pdf.line(
        42,
        38,
        width - 42,
        38
    )

    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_NAME, 7.5)

    pdf.drawRightString(
        width - 42,
        20,
        prepare_arabic("ROOTS WITH LAMA")
    )

    pdf.drawString(
        42,
        20,
        str(page_number)
    )


def draw_card(
    pdf,
    x,
    y,
    width,
    height,
    fill_color=WHITE,
    radius=20
):
    pdf.setFillColor(fill_color)
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.8)

    pdf.roundRect(
        x,
        y,
        width,
        height,
        radius,
        fill=1,
        stroke=1
    )


def draw_labeled_card(
    pdf,
    title,
    text,
    x,
    y,
    width,
    height,
    fill_color
):
    draw_card(
        pdf,
        x,
        y,
        width,
        height,
        fill_color=fill_color,
        radius=22
    )

    right = x + width - 20

    pdf.setFillColor(ROSE)
    pdf.roundRect(
        right - 34,
        y + height - 23,
        34,
        3,
        2,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(PLUM)
    pdf.setFont(FONT_NAME, 11)

    pdf.drawRightString(
        right,
        y + height - 44,
        prepare_arabic(title)
    )

    draw_rtl_lines(
        pdf,
        text,
        right,
        y + height - 76,
        width - 40,
        font_size=10.5,
        leading=21,
        color=BODY
    )


def draw_image_cover(pdf, image_path, x, y, width, height):
    if not image_path.exists():
        return

    image = ImageReader(str(image_path))

    img_width, img_height = image.getSize()

    scale = max(
        width / img_width,
        height / img_height
    )

    draw_width = img_width * scale
    draw_height = img_height * scale

    draw_x = x + (width - draw_width) / 2
    draw_y = y + (height - draw_height) / 2

    pdf.saveState()

    clip_path = pdf.beginPath()

    clip_path.roundRect(
        x,
        y,
        width,
        height,
        26
    )

    pdf.clipPath(
        clip_path,
        stroke=0,
        fill=0
    )

    pdf.drawImage(
        image,
        draw_x,
        draw_y,
        draw_width,
        draw_height,
        mask="auto"
    )

    pdf.restoreState()

    pdf.setStrokeColor(WHITE)
    pdf.setLineWidth(4)

    pdf.roundRect(
        x,
        y,
        width,
        height,
        26,
        fill=0,
        stroke=1
    )


# ---------- PDF ----------

def create_plan_pdf(plan, child_name="طفلك"):

    if not FONT_PATH.exists():
        raise FileNotFoundError(
            f"Arabic font not found: {FONT_PATH}"
        )

    pdfmetrics.registerFont(
        TTFont(
            FONT_NAME,
            str(FONT_PATH)
        )
    )

    buffer = io.BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4
    )

    width, height = A4

    page_number = 1


    # ========================================
    # COVER
    # ========================================

    draw_page_background(pdf)

    # main blush panel
    pdf.setFillColor(SOFT_CREAM)
    pdf.setStrokeColor(BORDER)

    pdf.roundRect(
        32,
        52,
        width - 64,
        height - 94,
        32,
        fill=1,
        stroke=1
    )

    # photo
    draw_image_cover(
        pdf,
        LAMA_IMAGE_PATH,
        50,
        215,
        205,
        500
    )

    # brand
    pdf.setFillColor(ROSE)
    pdf.setFont(FONT_NAME, 9)

    pdf.drawRightString(
        width - 48,
        height - 88,
        prepare_arabic("ROOTS WITH LAMA · جذور مع لمى")
    )

    # title
    y = height - 155

    y = draw_rtl_lines(
        pdf,
        plan["plan_title"],
        width - 48,
        y,
        270,
        font_size=24,
        leading=35,
        color=PLUM
    )

    y -= 26

    # goal
    y = draw_rtl_lines(
        pdf,
        plan["plan_goal"],
        width - 48,
        y,
        270,
        font_size=11,
        leading=23,
        color=BODY
    )

    # personalized badge
    badge_y = 128

    pdf.setFillColor(LILAC)

    pdf.roundRect(
        width - 305,
        badge_y,
        255,
        62,
        18,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(PLUM)
    pdf.setFont(FONT_NAME, 10)

    pdf.drawRightString(
        width - 68,
        badge_y + 36,
        prepare_arabic(
            f"خطة شخصية أُعدّت خصيصاً لـ {child_name}"
        )
    )

    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_NAME, 7.5)

    pdf.drawRightString(
        width - 68,
        badge_y + 18,
        prepare_arabic(
            "خطوات صغيرة، واقعية، ومصممة لروتينكم"
        )
    )

    pdf.showPage()
    page_number += 1


    # ========================================
    # BEFORE YOU START
    # ========================================

    draw_page_background(pdf)
    draw_brand(pdf)

    pdf.setFillColor(PLUM)
    pdf.setFont(FONT_NAME, 22)

    pdf.drawRightString(
        width - 46,
        height - 105,
        prepare_arabic("قبل ما تبلشي")
    )

    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_NAME, 9)

    pdf.drawRightString(
        width - 46,
        height - 135,
        prepare_arabic(
            "كم شغلة صغيرة بتخلي الأسبوع أوضح وأسهل"
        )
    )

    card_width = width - 92
    card_x = 46

    items = plan["before_you_start"]

    card_height = 112 if len(items) <= 3 else 96

    current_y = height - 190

    colors = [
        HexColor("#FBECEF"),
        HexColor("#F2EAF8"),
        HexColor("#FFF3EC"),
        HexColor("#F6EEF3")
    ]

    for index, item in enumerate(items):

        bottom = current_y - card_height

        draw_card(
            pdf,
            card_x,
            bottom,
            card_width,
            card_height,
            fill_color=colors[index % len(colors)],
            radius=22
        )

        # number
        pdf.setFillColor(ROSE)
        pdf.setFont(FONT_NAME, 18)

        pdf.drawRightString(
            width - 66,
            current_y - 34,
            str(index + 1)
        )

        draw_rtl_lines(
            pdf,
            item,
            width - 104,
            current_y - 32,
            card_width - 95,
            font_size=10.5,
            leading=21,
            color=BODY
        )

        current_y = bottom - 16

    draw_footer(
        pdf,
        page_number
    )

    pdf.showPage()
    page_number += 1


    # ========================================
    # DAYS 1-7
    # ========================================

    day_colors = [
        HexColor("#FBECEF"),
        HexColor("#F3EBF8"),
        HexColor("#FFF0EB"),
        HexColor("#F9EAF1"),
        HexColor("#EFE9F7"),
        HexColor("#FFF2ED"),
        HexColor("#F6EAF1")
    ]

    for day in plan["days"]:

        draw_page_background(pdf)
        draw_brand(pdf)

        # day badge
        pdf.setFillColor(day_colors[(day["day"] - 1) % len(day_colors)])

        pdf.roundRect(
            width - 138,
            height - 128,
            92,
            54,
            17,
            fill=1,
            stroke=0
        )

        pdf.setFillColor(ROSE)
        pdf.setFont(FONT_NAME, 9)

        pdf.drawRightString(
            width - 66,
            height - 96,
            prepare_arabic(
                f"اليوم {day['day']}"
            )
        )

        # focus title
        y = height - 165

        y = draw_rtl_lines(
            pdf,
            day["focus"],
            width - 46,
            y,
            width - 92,
            font_size=20,
            leading=31,
            color=PLUM
        )

        # progress dots
        dot_y = y - 12
        dot_start = width - 47

        for i in range(7):

            if i < day["day"]:
                pdf.setFillColor(ROSE)
            else:
                pdf.setFillColor(BORDER)

            pdf.circle(
                dot_start - (i * 16),
                dot_y,
                3.2,
                fill=1,
                stroke=0
            )

        # cards
        draw_labeled_card(
            pdf,
            "الخطوة الرئيسية",
            day["main_step"],
            46,
            430,
            width - 92,
            190,
            HexColor("#FFF9F7")
        )

        draw_labeled_card(
            pdf,
            "ممكن تقولي",
            day["say_this"],
            46,
            270,
            width - 92,
            130,
            HexColor("#F5EDF8")
        )

        draw_labeled_card(
            pdf,
            "راقبي",
            day["watch_for"],
            46,
            108,
            width - 92,
            132,
            HexColor("#FCECEF")
        )

        # tiny check circle
        pdf.setStrokeColor(ROSE)
        pdf.setLineWidth(1.2)

        pdf.circle(
            66,
            78,
            8,
            fill=0,
            stroke=1
        )

        pdf.setFillColor(MUTED)
        pdf.setFont(FONT_NAME, 7.5)

        pdf.drawString(
            82,
            75,
            "DONE"
        )

        draw_footer(
            pdf,
            page_number
        )

        pdf.showPage()
        page_number += 1


    # ========================================
    # FINAL PAGE
    # ========================================

    draw_page_background(pdf)
    draw_brand(pdf)

    pdf.setFillColor(PLUM)
    pdf.setFont(FONT_NAME, 22)

    pdf.drawRightString(
        width - 46,
        height - 110,
        prepare_arabic("بنهاية الأسبوع")
    )

    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_NAME, 9)

    pdf.drawRightString(
        width - 46,
        height - 140,
        prepare_arabic(
            "ما بدنا الكمال — بدنا نشوف أي حركة صغيرة للأحسن"
        )
    )

    draw_labeled_card(
        pdf,
        "شو منعتبره تقدّم؟",
        plan["end_of_week"],
        46,
        450,
        width - 92,
        230,
        HexColor("#FCECEF")
    )

    draw_labeled_card(
        pdf,
        "إذا بدنا نعدّل الخطة",
        plan["adjustment_note"],
        46,
        175,
        width - 92,
        235,
        HexColor("#F2EBF7")
    )

    pdf.setFillColor(PLUM)
    pdf.setFont(FONT_NAME, 10)

    pdf.drawRightString(
        width - 46,
        105,
        prepare_arabic(
            "خدي اللي ناسبكم، وعدّلي الباقي على مهلك."
        )
    )

    pdf.setFillColor(ROSE)
    pdf.setFont(FONT_NAME, 8)

    pdf.drawRightString(
        width - 46,
        78,
        prepare_arabic("معك لمى")
    )

    draw_footer(
        pdf,
        page_number
    )

    pdf.showPage()


    # ---------- SAVE ----------

    pdf.save()

    buffer.seek(0)

    return buffer
