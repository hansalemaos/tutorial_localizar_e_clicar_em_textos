import random
import re
import undetected_chromedriver as uc
from time import sleep
from a_selenium_click_on_coords import click_on_coordinates
from tesseractrapidfuzz import ocr_and_fuzzy_check

if __name__ == "__main__":
    driver = uc.Chrome(version_main=116)
    driver.get(r"https://www.youtube.com/watch?v=1WaV2x8GXj0&list=PLwhAEl-ufO2svyEJj8D2ViK_ZQrsOjz1Q&index=1")
    for rxa in range(10):
        img=driver.get_screenshot_as_png()
        df = ocr_and_fuzzy_check(
            tesseract_path=r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            allpics=[
              img
            ],
            strings_to_compare=[
                'johnnycash',
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

        max_val = df.compared_group_similarity.max()
        min_val = max_val*.8
        df2=df.loc[(df.compared_group_similarity <= max_val) & (df.compared_group_similarity >= min_val) ]
        sample = df2[:10].sample(1)[['x_center','y_center']].__array__()[0]
        click_on_coordinates(driver, x=int(sample[0]), y=int(sample[1]), script_timeout=10)
        sleep(random.uniform(5, 10))
