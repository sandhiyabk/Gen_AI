

# ✅ Install necessary libraries
!pip install -q gradio deep-translator

# ✅ Import packages
import gradio as gr
from deep_translator import GoogleTranslator
import random
from PIL import Image
import io

# ✅ Mood-based caption templates
caption_templates = {
    "Romantic": [
        "Lost in the colors of {place}, where every breath whispered love.",
        "{place} wrapped us in a warm embrace, one sunset at a time."
    ],
    "Adventurous": [
        "To the peaks of {place}, where the winds cheer and paths dare.",
        "Wandered wild through {place}, where every turn was a thrill."
    ],
    "Cozy": [
        "Sipped dreams in {place}, wrapped in a blanket of clouds.",
        "{place} felt like a lullaby hummed by the hills."
    ],
    "Magical": [
        "{place} glowed like a dream — stardust in every corner.",
        "In {place}, magic wasn't illusion, it was the moment."
    ]
}

# ✅ Mood-to-music suggestions (use royalty-free preview links)
music_links = {
    "Romantic": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "Adventurous": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "Cozy": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "Magical": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
}

# ✅ Generate caption
def generate_post(image, place, mood, lang_code):
    if not image or not place or not mood:
        return "Please provide all inputs.", None, None

    caption = random.choice(caption_templates[mood]).format(place=place)

    # Poetic Translation
    try:
        translated = GoogleTranslator(source='auto', target=lang_code).translate(caption)
    except Exception:
        translated = "[Translation Failed]"

    # Music URL
    song_url = music_links.get(mood, None)

    final_output = f"📍 **{place}**\n🎭 Mood: *{mood}*\n\n📝 **Original Caption**: {caption}\n\n🌐 **Poetic Translation**: {translated}"

    return final_output, image, song_url

# ✅ Build Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("🌍 **AI Travel InstaPost Generator**")
    gr.Markdown("Upload a travel photo, get a poetic caption and translation, with mood-based music 🎶")

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(label="Upload Travel Photo", type="pil")
            place_input = gr.Textbox(label="Where was this taken?")
            mood_input = gr.Dropdown(label="What mood fits best?", choices=list(caption_templates.keys()))
            lang_input = gr.Dropdown(label="Translate Caption To", choices=[
                "hi", "ta", "fr", "es", "ja", "zh", "ko"
            ], value="hi")
            submit_btn = gr.Button("Generate Post")

        with gr.Column(scale=1):
            output_text = gr.Markdown(label="Generated Post")
            image_output = gr.Image(label="Preview")
            audio_output = gr.Audio(label="Mood-based Music", interactive=False)

    submit_btn.click(fn=generate_post, inputs=[image_input, place_input, mood_input, lang_input],
                     outputs=[output_text, image_output, audio_output])

# ✅ Launch
demo.launch()

# ✅ Install necessary libraries
!pip install -q gradio deep-translator

# ✅ Import packages
import gradio as gr
from deep_translator import GoogleTranslator
import random

# ✅ Mood-based caption templates
caption_templates = {
    "Romantic": [
        "Lost in the colors of {place}, where every breath whispered love.",
        "{place} wrapped us in a warm embrace, one sunset at a time."
    ],
    "Adventurous": [
        "To the peaks of {place}, where the winds cheer and paths dare.",
        "Wandered wild through {place}, where every turn was a thrill."
    ],
    "Cozy": [
        "Sipped dreams in {place}, wrapped in a blanket of clouds.",
        "{place} felt like a lullaby hummed by the hills."
    ],
    "Magical": [
        "{place} glowed like a dream — stardust in every corner.",
        "In {place}, magic wasn't illusion, it was the moment."
    ]
}

# ✅ Mood-to-music suggestions
music_links = {
    "Romantic": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "Adventurous": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "Cozy": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "Magical": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
}

# ✅ Generate caption with English → Tamil translation
def generate_post(image, place, mood, lang_code):
    if not image or not place or not mood:
        return "Please provide all inputs.", None, None

    # 1. Pick template and format
    caption_en = random.choice(caption_templates[mood]).format(place=place)

    # 2. Translate caption into target language (e.g., Tamil 'ta')
    try:
        caption_ta = GoogleTranslator(source='en', target=lang_code).translate(caption_en)
    except Exception:
        caption_ta = "[Translation failed]"

    # 3. Retrieve mood music
    song_url = music_links.get(mood)

    # 4. Assemble final output
    output = (
        f"📍 **{place}**\n"
        f"🎭 Mood: *{mood}*\n\n"
        f"📝 **English Caption**: {caption_en}\n\n"
        f"🌐 **Translated Caption** ({lang_code}): {caption_ta}"
    )
    return output, image, song_url

# ✅ Build Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("🌍 **AI Travel InstaPost Generator**")
    gr.Markdown("Upload a travel photo and get a poetic English caption automatically translated into Tamil (or another language), with mood-based music 🎶")

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(label="Upload Travel Photo", type="pil")
            place_input = gr.Textbox(label="Where was this taken?")
            mood_input = gr.Dropdown(label="What mood fits best?", choices=list(caption_templates.keys()))
            lang_input = gr.Dropdown(
                label="Translate Caption To",
                choices=[("Tamil", "ta"), ("Hindi", "hi"), ("French", "fr"), ("Spanish", "es")],
                value="ta"
            )
            submit_btn = gr.Button("Generate Post")

        with gr.Column(scale=1):
            output_text = gr.Markdown(label="Generated Post")
            image_output = gr.Image(label="Preview")
            audio_output = gr.Audio(label="Mood-based Music", interactive=False)

    submit_btn.click(
        fn=generate_post,
        inputs=[image_input, place_input, mood_input, lang_input],
        outputs=[output_text, image_output, audio_output]
    )

# ✅ Launch app
demo.launch()

