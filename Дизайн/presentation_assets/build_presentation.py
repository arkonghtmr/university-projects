# -*- coding: utf-8 -*-
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "presentation_assets"
TEMPLATE = ROOT / "netflix-ui-evolution.pptx"
OUT = ROOT / "Презентация_pr7_PixelArt.pptx"


BG = RGBColor(7, 7, 7)
BG2 = RGBColor(13, 13, 16)
SURFACE = RGBColor(22, 21, 30)
SURFACE_2 = RGBColor(31, 27, 45)
CREAM = RGBColor(244, 239, 232)
MUTED = RGBColor(183, 177, 169)
MUTED_2 = RGBColor(213, 215, 228)
BORDER = RGBColor(72, 68, 82)
PURPLE = RGBColor(139, 92, 246)
PINK = RGBColor(236, 72, 153)
TEAL = RGBColor(38, 182, 164)
BLUE = RGBColor(75, 120, 255)
GOLD = RGBColor(214, 161, 58)
RED = RGBColor(229, 9, 20)


def rgb(hex_color: str) -> RGBColor:
    hex_color = hex_color.strip("#")
    return RGBColor(int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))


def remove_all_slides(prs: Presentation) -> None:
    slide_id_list = prs.slides._sldIdLst
    for slide_id in list(slide_id_list):
        rel_id = slide_id.rId
        slide_id_list.remove(slide_id)
        prs.part.drop_rel(rel_id)


def no_line(shape) -> None:
    shape.line.color.rgb = shape.fill.fore_color.rgb
    shape.line.transparency = 100


def set_fill(shape, color: RGBColor, transparency: int = 0) -> None:
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.fill.transparency = transparency


def background(slide) -> None:
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    set_fill(rect, BG)
    no_line(rect)
    # Thin top accent, visually close to the source template but using PixelArt colors.
    colors = [PURPLE, PINK, TEAL, BLUE, GOLD, RED]
    seg_w = 13.333 / len(colors)
    for i, color in enumerate(colors):
        seg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(i * seg_w), 0, Inches(seg_w + 0.01), Inches(0.09)
        )
        set_fill(seg, color)
        no_line(seg)


def add_text(
    slide,
    text: str,
    x: float,
    y: float,
    w: float,
    h: float,
    size: int = 24,
    color: RGBColor = CREAM,
    bold: bool = False,
    align=PP_ALIGN.LEFT,
    font: str = "Aptos Display",
    line_spacing: float | None = None,
) -> None:
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    for idx, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        if line_spacing is not None:
            p.line_spacing = line_spacing
        for run in p.runs:
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = color


def add_kicker(slide, text: str, x: float, y: float, w: float = 2.2, color: RGBColor = PINK) -> None:
    add_text(slide, text.upper(), x, y, w, 0.22, 10, color, True, font="Aptos")


def add_title(slide, kicker: str, title: str, subtitle: str | None = None) -> None:
    add_kicker(slide, kicker, 0.65, 0.62, 2.4)
    add_text(slide, title, 0.65, 0.98, 11.6, 0.9, 33, CREAM, True, font="Aptos Display")
    if subtitle:
        add_text(slide, subtitle, 0.65, 1.58, 11.6, 0.48, 14, MUTED_2, False, font="Aptos")


def add_card(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: RGBColor = SURFACE,
    border: RGBColor = BORDER,
    transparency: int = 8,
):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    set_fill(card, fill, transparency)
    card.line.color.rgb = border
    card.line.width = Pt(1)
    return card


def add_feature(slide, label: str, body: str, x: float, y: float, w: float, h: float, color: RGBColor) -> None:
    add_card(slide, x, y, w, h, SURFACE, BORDER, 8)
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.07), Inches(h))
    set_fill(strip, color)
    no_line(strip)
    add_text(slide, label.upper(), x + 0.22, y + 0.17, w - 0.35, 0.18, 8, color, True, font="Aptos")
    add_text(slide, body, x + 0.22, y + 0.43, w - 0.35, h - 0.50, 11, CREAM, False, font="Aptos")


def add_pill(slide, text: str, x: float, y: float, w: float, color: RGBColor = PURPLE) -> None:
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.36))
    set_fill(pill, color, 12)
    pill.line.color.rgb = color
    pill.line.width = Pt(1)
    add_text(slide, text, x + 0.12, y + 0.09, w - 0.24, 0.16, 9, CREAM, True, PP_ALIGN.CENTER, font="Aptos")


def add_cover_image(slide, image_path: Path, x: float, y: float, w: float, h: float, border: bool = True):
    image_path = Path(image_path)
    with Image.open(image_path) as im:
        iw, ih = im.size
    pic = slide.shapes.add_picture(str(image_path), Inches(x), Inches(y), Inches(w), Inches(h))
    img_ratio = iw / ih
    box_ratio = w / h
    if img_ratio > box_ratio:
        crop = (1 - box_ratio / img_ratio) / 2
        pic.crop_left = crop
        pic.crop_right = crop
    else:
        crop = (1 - img_ratio / box_ratio) / 2
        pic.crop_top = crop
        pic.crop_bottom = crop
    if border:
        frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        frame.fill.background()
        frame.line.color.rgb = BORDER
        frame.line.width = Pt(1)
        # Keep the image above the frame by moving the frame behind it.
        slide.shapes._spTree.remove(frame._element)
        slide.shapes._spTree.insert(2, frame._element)
    return pic


def add_contain_image(slide, image_path: Path, x: float, y: float, w: float, h: float, border: bool = True):
    image_path = Path(image_path)
    with Image.open(image_path) as im:
        iw, ih = im.size
    img_ratio = iw / ih
    box_ratio = w / h
    if img_ratio > box_ratio:
        pw = w
        ph = w / img_ratio
        px = x
        py = y + (h - ph) / 2
    else:
        ph = h
        pw = h * img_ratio
        px = x + (w - pw) / 2
        py = y
    if border:
        frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        set_fill(frame, RGBColor(10, 10, 12), 0)
        frame.line.color.rgb = BORDER
        frame.line.width = Pt(1)
    return slide.shapes.add_picture(str(image_path), Inches(px), Inches(py), Inches(pw), Inches(ph))


def add_footer(slide, n: int, text: str = "pr7 / PixelArt") -> None:
    add_text(slide, f"{n:02d}", 0.65, 7.05, 0.45, 0.18, 8, MUTED, True, font="Aptos")
    add_text(slide, text, 1.08, 7.05, 3.5, 0.18, 8, MUTED, False, font="Aptos")


def slide_title(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_cover_image(slide, ASSETS / "site-hero.png", 4.95, 0.86, 7.75, 5.05, border=True)
    overlay = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(4.75), Inches(7.5))
    set_fill(overlay, RGBColor(5, 5, 8), 0)
    no_line(overlay)
    add_kicker(slide, "готовый сайт pr7", 0.65, 0.78, 2.6, TEAL)
    add_text(slide, "Лендинг\nPixelArt", 0.65, 1.18, 3.65, 1.15, 37, CREAM, True)
    add_text(
        slide,
        "Моушн-дизайн с нуля\nHTML + CSS + JS реализация",
        0.65,
        2.58,
        3.55,
        0.72,
        16,
        MUTED_2,
        False,
        font="Aptos",
    )
    add_feature(slide, "основа", "практики.docx, ПЗ2, ПЗ3, сайт pr7", 0.65, 4.15, 3.35, 0.75, PURPLE)
    add_feature(slide, "автор", "Фёдоров А.С., БСБО-09-23\nДисциплина: дизайн интерфейсов", 0.65, 5.12, 3.35, 0.82, PINK)
    add_pill(slide, "исследование → архитектура → реализация", 0.65, 6.22, 3.35, TEAL)
    return slide


def slide_route(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "маршрут",
        "Как проект дошёл до готового сайта",
        "Шесть этапов связывают исследование, информационную архитектуру и итоговую HTML/CSS/JS-реализацию.",
    )
    steps = [
        ("ПЗ2", "Исследование\nпроекта"),
        ("ЦА", "Потребности\nи страхи"),
        ("ПЗ3", "Информационная\nархитектура"),
        ("UI", "Темная визуальная\nсистема"),
        ("pr7", "Верстка\nлендинга"),
        ("QA", "Адаптивность\nи проверка"),
    ]
    y = 3.35
    x0 = 0.92
    gap = 2.17
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x0 + 0.45), Inches(y + 0.18), Inches(10.9), Inches(0.025))
    set_fill(line, BORDER, 0)
    no_line(line)
    colors = [PURPLE, PINK, TEAL, BLUE, GOLD, RED]
    for idx, (code, label) in enumerate(steps):
        x = x0 + idx * gap
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(0.46), Inches(0.46))
        set_fill(dot, colors[idx], 0)
        dot.line.color.rgb = colors[idx]
        add_text(slide, code, x + 0.055, y + 0.13, 0.35, 0.12, 8, CREAM, True, PP_ALIGN.CENTER, font="Aptos")
        add_text(slide, label, x - 0.34, y + 0.78, 1.15, 0.52, 12, CREAM, True, PP_ALIGN.CENTER, font="Aptos")
    add_card(slide, 1.15, 5.48, 11.0, 0.82, SURFACE_2, BORDER, 5)
    add_text(
        slide,
        "Итоговая страница сохраняет проектную логику: сначала оффер, затем доказательства ценности, программа, доверие, тарифы и снятие возражений.",
        1.55,
        5.76,
        10.25,
        0.22,
        15,
        CREAM,
        False,
        PP_ALIGN.CENTER,
        font="Aptos",
    )
    add_footer(slide, 2, "структура презентации")
    return slide


def slide_research(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "пз2",
        "Исследование: что должен решать лендинг",
        "Отчет ПЗ2 задает тему, целевое действие, аудиторию, УТП и конкурентный контекст.",
    )
    add_feature(slide, "фокус", "Товарный лендинг для продажи курса или заявки на бесплатную консультацию.", 0.65, 2.45, 4.0, 0.86, PURPLE)
    add_feature(slide, "цель", "Конвертировать посетителей в учеников: показать ценность обучения и снизить страхи.", 0.65, 3.52, 4.0, 0.86, PINK)
    add_feature(slide, "утп", "2 месяца, 2D/3D-анимация, After Effects и Cinema 4D, портфолио из 5 работ.", 0.65, 4.59, 4.0, 0.86, TEAL)
    add_feature(slide, "контекст", "Темная тема и шоурил выбраны как уместные паттерны для сферы motion-дизайна.", 0.65, 5.66, 4.0, 0.86, BLUE)
    add_contain_image(slide, ASSETS / "pz2-page-1.png", 5.55, 2.05, 6.65, 4.67, border=True)
    add_footer(slide, 3, "источник: ПЗ2 «Исследование для проекта»")
    return slide


def slide_audience(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "аудитория",
        "Кому продает сайт",
        "Смысловые блоки повторяют исследованные сегменты и отвечают на их основные сомнения.",
    )
    cards = [
        ("Новички", "Нужна понятная пошаговая программа и ощущение, что можно начать без опыта.", PURPLE),
        ("Смена профессии", "Важны доход, удаленный формат, карьерная поддержка и первые заказы.", PINK),
        ("Дизайнеры", "Нужен новый навык для портфолио: 2D/3D-анимация и showreel.", TEAL),
    ]
    for i, (title, body, color) in enumerate(cards):
        y = 2.35 + i * 1.05
        add_feature(slide, title, body, 0.65, y, 4.0, 0.82, color)
    add_card(slide, 0.65, 5.7, 4.0, 0.78, SURFACE_2, BORDER, 5)
    add_text(slide, "Главная UX-задача: закрыть страхи «нет таланта», «курс окажется водой», «после курса не будет клиентов».", 0.95, 5.97, 3.45, 0.22, 12, CREAM, False, PP_ALIGN.CENTER, font="Aptos")
    add_cover_image(slide, ASSETS / "site-audience.png", 5.12, 2.12, 7.3, 4.35, border=True)
    add_footer(slide, 4, "ПЗ2 + блок «Для кого этот курс»")
    return slide


def slide_architecture(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "пз3",
        "Информационная архитектура",
        "Одностраничный сайт построен как последовательность аргументов: от внимания к доверию и покупке.",
    )
    add_feature(slide, "первый экран", "Заголовок, динамичный визуал и CTA сразу объясняют предложение.", 0.65, 2.38, 3.95, 0.82, PURPLE)
    add_feature(slide, "ценность", "Аудитория, результаты, программа, работы выпускников и преподаватели раскрывают пользу.", 0.65, 3.38, 3.95, 0.82, PINK)
    add_feature(slide, "конверсия", "Тарифы, FAQ и футер снимают последние возражения перед заявкой.", 0.65, 4.38, 3.95, 0.82, TEAL)
    add_feature(slide, "паттерн", "Аккордеоны и карточки уменьшают когнитивную нагрузку на длинной странице.", 0.65, 5.38, 3.95, 0.82, BLUE)
    add_contain_image(slide, ASSETS / "pz3-page-2.png", 5.25, 2.02, 7.05, 4.75, border=True)
    add_footer(slide, 5, "источник: ПЗ3 «Информационная архитектура»")
    return slide


def slide_hero(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "экран 1",
        "Первый экран работает как оффер",
        "Главный экран сочетает УТП, дату старта, два CTA, метрики курса и motion-визуал на canvas.",
    )
    add_feature(slide, "фокус", "«Моушн-дизайн с нуля» — пользователь сразу понимает продукт.", 0.65, 2.28, 3.95, 0.82, PURPLE)
    add_feature(slide, "паттерн", "Две кнопки разделяют горячее действие и мягкую консультацию.", 0.65, 3.28, 3.95, 0.82, PINK)
    add_feature(slide, "эффект", "Шоурил-экран и статистика обещают практический результат: 2 месяца, 5 проектов, 100% практики.", 0.65, 4.28, 3.95, 1.02, TEAL)
    add_pill(slide, "hero / CTA / canvas animation", 0.65, 5.72, 3.95, BLUE)
    add_cover_image(slide, ASSETS / "site-hero.png", 5.0, 2.02, 7.7, 4.85, border=True)
    add_footer(slide, 6, "готовый сайт pr7")
    return slide


def slide_program(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "контент",
        "Программа и материалы не перегружают страницу",
        "Длинный учебный контент спрятан в управляемые блоки и встроенные PDF-фреймы.",
    )
    add_cover_image(slide, ASSETS / "site-program.png", 0.65, 2.28, 5.82, 3.85, border=True)
    add_cover_image(slide, ASSETS / "site-frames.png", 6.85, 2.28, 5.82, 3.85, border=True)
    stats = [("8", "недель"), ("4", "модуля"), ("2", "PDF-фрейма")]
    for i, (num, label) in enumerate(stats):
        x = 1.1 + i * 1.7
        add_text(slide, num, x, 6.35, 0.6, 0.28, 24, [PURPLE, PINK, TEAL][i], True)
        add_text(slide, label, x + 0.45, 6.45, 1.0, 0.18, 10, MUTED_2, False, font="Aptos")
    add_feature(slide, "ux-прием", "Аккордеон раскрывает расписание постепенно.", 7.1, 6.2, 4.7, 0.7, GOLD)
    add_footer(slide, 7, "блоки «Программа» и «Фреймы»")
    return slide


def slide_works(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "портфолио",
        "Работы выпускников продают результат",
        "Галерея заменяет абстрактные обещания визуальным доказательством уровня курса.",
    )
    add_cover_image(slide, ASSETS / "site-works.png", 0.78, 1.78, 11.78, 4.25, border=True)
    add_feature(slide, "9 работ", "9 примеров: заставки, 3D, типографика.", 0.78, 6.17, 3.55, 0.78, PURPLE)
    add_feature(slide, "motion-паттерн", "Play-иконка задает ожидание видео.", 4.88, 6.17, 3.55, 0.78, PINK)
    add_feature(slide, "доверие", "Портфолио показывает итог обучения.", 8.98, 6.17, 3.55, 0.78, TEAL)
    add_footer(slide, 8, "блок «Работы выпускников»")
    return slide


def slide_pricing(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "конверсия",
        "Тарифы и доверие закрывают путь к заявке",
        "После доказательств ценности сайт показывает варианты оплаты и усиливает доверие через преподавателей.",
    )
    add_feature(slide, "преподаватели", "Три карточки специалистов: арт-директор, lead motion designer и freelance motion designer.", 0.65, 2.38, 3.95, 0.95, PURPLE)
    add_feature(slide, "тарифы", "Два сценария покупки: «Стандарт» и «С наставником» с выделением популярного варианта.", 0.65, 3.55, 3.95, 0.95, PINK)
    add_feature(slide, "снятие барьера", "Указана рассрочка на 4 месяца и повторный CTA на консультацию.", 0.65, 4.72, 3.95, 0.95, TEAL)
    add_pill(slide, "29 900 ₽ / 49 900 ₽", 0.65, 6.1, 3.95, GOLD)
    add_cover_image(slide, ASSETS / "site-pricing.png", 5.0, 1.86, 7.7, 4.95, border=True)
    add_footer(slide, 9, "блоки «Преподаватели» и «Тарифы»")
    return slide


def slide_uxui(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "принципы",
        "UX/UI-решения в готовом сайте",
        "Теоретические материалы применены через структуру, визуальную иерархию и группировку элементов.",
    )
    cards = [
        ("UX: целевое действие", "Навигация, CTA и блок тарифов ведут к покупке курса или консультации.", PURPLE),
        ("UI: графическая часть", "Темная тема, градиентные CTA, карточки и крупная типографика задают стиль digital-курса.", PINK),
        ("Гештальт", "Связанные элементы сгруппированы в карточки, сетки и общие области.", TEAL),
    ]
    for i, (title, body, color) in enumerate(cards):
        x = 0.75 + i * 4.15
        add_card(slide, x, 2.35, 3.55, 2.45, SURFACE, BORDER, 8)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 0.35), Inches(2.65), Inches(0.78), Inches(0.08))
        set_fill(bar, color)
        no_line(bar)
        add_text(slide, title, x + 0.35, 3.05, 2.85, 0.42, 18, CREAM, True)
        add_text(slide, body, x + 0.35, 3.78, 2.8, 0.72, 12, MUTED_2, False, font="Aptos")
    add_card(slide, 1.05, 5.55, 11.22, 0.78, SURFACE_2, BORDER, 5)
    palette = [("#8B5CF6", PURPLE), ("#EC4899", PINK), ("#38BDF8", rgb("#38BDF8")), ("#2DD4BF", rgb("#2DD4BF")), ("#F59E0B", rgb("#F59E0B"))]
    add_text(slide, "Палитра сайта", 1.35, 5.82, 1.4, 0.18, 11, CREAM, True, font="Aptos")
    for i, (hex_code, color) in enumerate(palette):
        x = 3.0 + i * 1.45
        sw = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(5.72), Inches(0.42), Inches(0.42))
        set_fill(sw, color, 0)
        sw.line.color.rgb = color
        add_text(slide, hex_code, x + 0.52, 5.83, 0.8, 0.14, 7, MUTED_2, False, font="Aptos")
    add_footer(slide, 10, "теория UX/UI + гештальт-принципы")
    return slide


def slide_tech(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "реализация",
        "Статический сайт без сборщика",
        "Версия pr7 работает как отдельная HTML/CSS/JS-реализация и открывается через index.html.",
    )
    add_card(slide, 0.75, 2.18, 4.25, 3.78, RGBColor(11, 11, 16), BORDER, 0)
    tree = "pr7/\n├─ index.html   структура страницы\n├─ styles.css   темная UI-система\n├─ script.js    интерактив\n└─ assets/      PDF и изображения работ"
    add_text(slide, tree, 1.05, 2.55, 3.7, 2.2, 13, CREAM, False, font="Cascadia Mono")
    add_feature(slide, "script.js", "Мобильное меню, плавная навигация, аккордеоны, рендер карточек и canvas-анимация.", 1.05, 5.13, 3.65, 0.62, TEAL)
    add_cover_image(slide, ASSETS / "site-mobile-menu.png", 5.52, 1.7, 2.55, 5.35, border=True)
    add_feature(slide, "styles.css", "CSS-переменные, responsive grid, фиксированный header, темные карточки и состояния hover.", 8.55, 2.18, 3.95, 0.92, PURPLE)
    add_feature(slide, "index.html", "Семантические секции: hero, audience, benefits, program, frames, works, teachers, pricing, FAQ, footer.", 8.55, 3.34, 3.95, 0.92, PINK)
    add_feature(slide, "assets", "PDF-материалы встроены через iframe, а изображения используются в галерее работ.", 8.55, 4.5, 3.95, 0.92, GOLD)
    add_footer(slide, 11, "папка pr7")
    return slide


def slide_adaptive(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_title(
        slide,
        "адаптив",
        "Сайт сохраняет сценарий на мобильном экране",
        "Мобильная версия перестраивает сетки, скрывает десктопную навигацию и оставляет крупные CTA.",
    )
    add_cover_image(slide, ASSETS / "site-hero.png", 0.72, 2.18, 6.15, 3.55, border=True)
    add_cover_image(slide, ASSETS / "site-mobile-hero.png", 7.32, 2.02, 2.45, 4.92, border=True)
    add_feature(slide, "меню", "Desktop-навигация заменяется burger-меню.", 10.18, 2.05, 2.55, 0.72, PURPLE)
    add_feature(slide, "сетки", "Карточки и галереи переходят в одну колонку.", 10.18, 3.02, 2.55, 0.72, PINK)
    add_feature(slide, "кнопки", "CTA остаются крупными и удобными для нажатия.", 10.18, 3.99, 2.55, 0.72, TEAL)
    add_feature(slide, "визуал", "Canvas и изображения масштабируются под ширину экрана.", 10.18, 4.96, 2.55, 0.72, BLUE)
    add_footer(slide, 12, "desktop + mobile screenshots")
    return slide


def slide_conclusion(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    background(slide)
    add_cover_image(slide, ASSETS / "site-hero.png", 6.15, 0.72, 6.65, 5.4, border=True)
    veil = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(6.05), Inches(7.5))
    set_fill(veil, RGBColor(0, 0, 0), 0)
    no_line(veil)
    add_kicker(slide, "вывод", 0.65, 0.8, 1.5, TEAL)
    add_text(
        slide,
        "Готовый сайт превращает\nисследование в рабочий лендинг.",
        0.65,
        1.22,
        5.85,
        1.25,
        32,
        CREAM,
        True,
    )
    add_text(
        slide,
        "В pr7 есть ясный оффер, логичная информационная архитектура, визуальные доказательства результата, тарифы, FAQ и адаптивная HTML/CSS/JS-реализация.",
        0.65,
        3.05,
        5.55,
        0.78,
        15,
        MUTED_2,
        False,
        font="Aptos",
    )
    add_feature(slide, "главная мысль", "Страница ведет пользователя от интереса к доверию и целевому действию.", 0.65, 4.45, 5.25, 0.86, PINK)
    add_text(slide, "Спасибо за внимание!", 0.65, 6.28, 5.3, 0.38, 25, CREAM, True)
    add_footer(slide, 13, "готовый файл презентации")
    return slide


def build() -> None:
    prs = Presentation(str(TEMPLATE))
    remove_all_slides(prs)
    prs.core_properties.title = "Лендинг PixelArt: Моушн-дизайн с нуля"
    prs.core_properties.subject = "Презентация по готовому сайту pr7"
    prs.core_properties.author = "Фёдоров А.С."

    slide_title(prs)
    slide_route(prs)
    slide_research(prs)
    slide_audience(prs)
    slide_architecture(prs)
    slide_hero(prs)
    slide_program(prs)
    slide_works(prs)
    slide_pricing(prs)
    slide_uxui(prs)
    slide_tech(prs)
    slide_adaptive(prs)
    slide_conclusion(prs)
    prs.save(str(OUT))


if __name__ == "__main__":
    build()
    print(OUT)
