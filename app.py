import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import re

# =========================
# Настройки
# =========================

st.set_page_config(
    page_title="Food Ingredient Scanner",
    layout="centered"
)

st.title("🧪 AI Food Ingredient Scanner")
st.write("Качи снимка или използвай камера за разпознаване на съставки.")

# =========================
# Вредни съставки
# =========================

harmful_ingredients = {
    "E621": "Мононатриев глутамат",
    "PALM OIL": "Палмово масло",
    "ПАЛМОВО МАСЛО": "Палмово масло",
    "ASPARTAME": "Аспартам",
    "АСПАРТАМ": "Аспартам",
    "E951": "Аспартам",
    "E102": "Тартразин",
    "E110": "Жълт оцветител",
    "E124": "Понсо 4R"
}

# =========================
# OCR Reader
# =========================

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])

reader = load_reader()

# =========================
# Качване на снимка
# =========================

uploaded_file = st.file_uploader(
    "📂 Качи снимка",
    type=["jpg", "jpeg", "png"]
)

# =========================
# Камера
# =========================

camera_image = st.camera_input("📸 Направи снимка")

image_source = None

if uploaded_file is not None:
    image_source = uploaded_file

elif camera_image is not None:
    image_source = camera_image

# =========================
# OCR обработка
# =========================

if image_source is not None:

    image = Image.open(image_source)

    st.image(image, caption="Избрана снимка", use_container_width=True)

    image_np = np.array(image)

    with st.spinner("🔍 Разпознаване на текст..."):

        results = reader.readtext(image_np)

        extracted_text = " ".join([res[1] for res in results])

    st.subheader("📄 Разпознат текст")
    st.write(extracted_text)

    # =========================
    # Търсене на вредни съставки
    # =========================

    found = []

    text_upper = extracted_text.upper()

    for ingredient, description in harmful_ingredients.items():

        pattern = re.escape(ingredient.upper())

        if re.search(pattern, text_upper):
            found.append((ingredient, description))

    st.subheader("⚠️ Анализ на съставките")

    if found:

        st.error("Открити са потенциално вредни съставки:")

        for ing, desc in found:
            st.write(f"• {ing} → {desc}")

    else:
        st.success("Не са открити вредни съставки.")

# =========================
# Информация
# =========================

st.markdown("---")
st.write("Поддържани езици: 🇧🇬 Български / 🇬🇧 English")
