import os
import io
import streamlit as st
from dotenv import load_dotenv
# Assuming ElevenLabs is a valid library that you have access to.
# from elevenlabs.client import ElevenLabs
import google.generativeai as genai
from PIL import Image
import warnings
from io import BytesIO
import time

def main():
    # Load environment variables
    load_dotenv()

    # Streamlit app setup
    st.title("💄👄👠💅Stylish✨💋💇‍♀️💁‍♀️")



    def generate_content(img_buffer, inp):
        load_dotenv()
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=gemini_api_key)
        try:
            # Load the image from BytesIO to PIL Image
            image = Image.open(img_buffer)

            # Assuming the model requires a PIL Image; if it requires another format you might need to adjust this
            prompt = f'''You are an expert in providing advice and recommendations for events. Based on the facial image provided, please recommend the best makeup colors, hairstyles or hijab style, manicures, and clothing arrangements according to this specific and personalized information {inp}, Answer in Arabic ONLY'''
            model = genai.GenerativeModel('gemini-1.0-pro-vision-latest')
            response = model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            st.error("Failed to generate content: {}".format(e))
            return None


    img_file_buffer = st.file_uploader("Upload an image (jpg, png, jpeg):", type=["jpg", "png", "jpeg"])
    eye_colors = st.text_input("Eye color")
    skin_colors = st.text_input("Skin color")
    hijab =  st.text_input("You wear Hijab or no?")
    season = st.text_input("season 'summer winter autumn spring'")
    description = st.text_input("Tell me about this ocuasion")

    inp = "Eye color : " + eye_colors + ' , ' + "Skin color : " +  skin_colors + ' , ' + "You wear Hijab or no? : " +  hijab + ' , ' +  "season 'summer winter autumn spring': " +  season + ' , ' + "Tell me about this ocuasion" +  description 

    if st.button("Generate Recommandation"):
        if img_file_buffer:
            # Convert the file buffer to an image object
            image_stream = BytesIO(img_file_buffer.getvalue())

            # Generate content based on text and image
            processed_text = generate_content(image_stream,inp)

            if processed_text:
                # Display the result from generate_content
                st.markdown(f"<div style='direction: rtl; text-align: right;'>{processed_text}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
