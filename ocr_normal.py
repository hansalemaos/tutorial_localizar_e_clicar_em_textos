import random
from time import sleep
import re
from tesseractrapidfuzz import ocr_and_fuzzy_check
from PrettyColorPrinter import add_printer

add_printer(1)
from mousekey import MouseKey

mkey = MouseKey()
mkey.enable_failsafekill('ctrl+e')
from fast_ctypes_screenshots import (
    ScreenshotOfOneMonitor,
)

for acao in range(10):
    with ScreenshotOfOneMonitor(
            monitor=0, ascontiguousarray=False
    ) as screenshots_monitor:
        img = screenshots_monitor.screenshot_one_monitor()

    df = ocr_and_fuzzy_check(
        tesseract_path=r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        allpics=[
            img
        ],
        strings_to_compare=[
            "johnnycash",
        ],
        compare_single_words=True,
        compare_grouped_words=True,
        scorer_single_words="WRatio",
        scorer_grouped_words="WRatio",
        add_after_tesseract_path="",
        add_at_the_end="-l eng --psm 3",
        workers=5,
        processor=lambda x: re.sub(r"\W+", "", str(x).lower()),
    )
    print(df.to_string())
    max_val = df.compared_group_similarity.max()
    min_val = max_val * .8
    df2 = df.loc[(df.compared_group_similarity <= max_val)
                 & (df.compared_group_similarity >= min_val)]
    df3 = df2.loc[(df2.start_x > 500) & (df2.start_y > 200) &
                  (df2.end_y < 750)].sort_values(by='compared_word_similarity', ascending=False)
    x, y = df3.sample(1)[['x_center', 'y_center']].__array__()[0]
    x, y = int(x), int(y)
    mkey.left_click_xy_natural(
        x=x,
        y=y,
        delay=random.uniform(.1, .3),  # duration of the mouse click (down - up)
        min_variation=-3,  # a random value will be added to each pixel  - define the minimum here
        max_variation=3,  # a random value will be added to each pixel  - define the maximum here
        use_every=4,  # use every nth pixel
        sleeptime=(0.005, 0.009),  # delay between each coordinate
        print_coords=True,  # console output
        percent=90,  # the lower, the straighter the mouse movement
    )
    sleep(random.uniform(5, 8))
