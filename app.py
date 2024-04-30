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

    seasonal_makeup_tips = {
        "Spring": "Use bright eye shadows like pink and purple, apply pink blush, and choose from eye-catching lipstick shades in the 'Show Stopper' collection.",
        "Summer": "Opt for lightweight, oil-free foundation and waterproof mascara, use bronze blush, and embrace vibrant and shiny eye shadow colors for day and evening looks.",
        "Winter": "Focus on nourishing skin care products like 'Shea Butter Collection' from The Body Shop, use bold earthy eye shadows, black eyeliner, and apply highlighter generously to brighten the dull winter complexion.",
        "Autumn": "Feature bold lip colors in red and purple, add a golden shimmer to eye shadows, and use dewy makeup to give the skin a radiant and vibrant appearance."
    }


    face_shape_tips = {
        "Round Face": "Use arched eyebrows, contouring at the cheeks, and luminous blush for makeup; opt for short wavy hair or an asymmetrical medium-length cut for hairstyles.",
        "Oval Face": "Keep lips simple with heavy eye makeup, follow natural eyebrow arch, and highlight nose bridge and forehead for makeup; choose a side-swept pixie or a curly neck-length bob for hairstyles.",
        "Square Face": "Contour to soften jawline angles, use lighter concealer on forehead and under cheeks, and bright or coral lips for makeup; medium-length hair tucked to the side or an asymmetrical bob for hairstyles.",
        "Rectangular Face": "Soften the jawline and forehead with contour, use cat-eye eyeliner, and apply blush high on cheeks for makeup; opt for a long layered pixie or shoulder-length layered hair with bangs for hairstyles.",
        "Diamond Face": "Highlight forehead, upper lip, chin, and nose bridge, and contour to reduce cheekbone width for makeup; long layered waves or a chin-length bob for hairstyles.",
        "Heart-Shaped Face": "Minimize sharp angles with soft smokey eyes and bronzer for contouring, and thick mascara for makeup; choose a bob shorter than shoulders or long, layered cuts for hairstyles."
    }


    nail_polish_tips = {
        "Very Light Skin": "Preferred Colors: Soft, light colors like nude, white, light pink, beige, and cream to complement very light skin.\nAvoid: Neon colors which can darken the skin appearance, and dark colors during the day as they may make the skin look too pale.",
        "Medium Skin (Wheatish - Yellow)": "Preferred Colors: Strong, vibrant colors such as bold white, red, blue, green, and pink to help make the skin appear brighter.\nAvoid: Light, muted shades and yellow tones like yellow, orange, and brick, which can dull the skin. Neon colors are also not recommended.",
        "Dark Skin (All Shades)": "Preferred Colors: Most colors including soft, vivid, strong, neon, and dark shades which suit dark skin well.\nAvoid: Brown shades as they don’t show up well; instead opt for dark burgundy or other dark shiny colors.",
    }


    makeup_routines = {
        "Weekend/Errands/Lounging Makeup": "Previously applied post-workout, even indoors, but now often goes without, focusing on skincare like face washing and applying sunscreen. Weekends in the 20s often involved no makeup or party makeup.",
        "Daily Makeup (Office Makeup)": "Routine includes concealer, eyebrow pencil/gel, eyeliner, a single eyeshadow color, mascara, blush, lip liner, and lipstick. Maintains two or three standard looks with set combinations of eyeliner, eyeshadow, and lipstick colors.",
        "Work-From-Home Makeup": "Initially no makeup but shifted to a simplified routine due to dressing-up advice, now includes sheer lipstick, blush, under-eye concealer, waterproof eyeliner, and occasionally liquid shadow, keeping to minimalistic approaches with different eyeliner and lipstick colors.",
        "Big Presentation and Job Interview Makeup": "Opts for a confident yet professional look, distinct from both the daily and party makeup styles.",
        "Date Night or Party Makeup": "Prefers a smoky eye look with foundation, concealer, contour/highlight/blush, eyeshadow primer, 2-4 eyeshadows in the same color family, dark and light eyeliners, neutral lip color, and multiple mascara layers or magnetic lashes. Enjoys experimenting and sometimes involves family in choosing colors."
    }


    eye_makeup_styles = {
        "Classic Smokey Eye Makeup": "Apply a neutral base color, blend a darker shade into the crease and outer corners, smudge dark eyeshadow along the lash lines, and finish with mascara for drama. Suitable for evening events.",
        "Bridal Eye Makeup": "Use elegant, soft, long-lasting neutral shades like champagne or soft pinks, subtle winged eyeliner, inner corner shimmer, and waterproof mascara for weddings.",
        "Natural and Fresh Eye Makeup": "Enhance features subtly with light neutral eyeshadow, brown eyeliner, and mascara. Ideal for everyday wear or a 'no-makeup' makeup look.",
        "Step-by-Step Eye Makeup Tutorial": "A tutorial ideal for beginners, breaking down each step from eyelid prep to blending shades, with images or videos for guidance.",
        "Nude Eye Makeup": "Create a soft, natural look with beige and light brown shades, blending darker shades into the crease and finishing with mascara and nude eyeliner.",
        "Bold and Colorful Eye Makeup": "Use vibrant shades like blue, green, or purple, with monochromatic or contrasting colors in matte or metallic textures, balanced with a neutral lip color for a statement look.",
        "Everyday Eye Makeup for Work": "Keep it simple and professional with neutral eyeshadows, minimal eyeliner, mascara, and groomed eyebrows for a polished work appearance.",
        "Dramatic Winged Eyeliner": "Draw a thickening line along the upper lash line, extending upwards for the wing, adjusting boldness to match style preference. Adds sophistication to any look.",
        "Glittery Eye Makeup for Parties": "Add sparkle with glittery eyeshadow or loose glitter on the lids or lower lash line, using a primer to keep glitter in place and simple makeup elsewhere to highlight eyes.",
        "Soft and Romantic Eye Makeup": "Use pastel shades like pink or lavender, blending darker shades into the crease, highlighting inner corners with shimmer, and finishing with thin eyeliner and mascara. Ideal for date nights or special occasions."
    }


    hijab_styles = {
    "Heart-Shaped Face": '''
        Opt for: Loose hijab styles to soften a broad forehead.
        Avoid: Tightly secured hijabs that highlight the forehead.
        Tips: Wrap the scarf around the jaw to adjust proportions and cover the forehead to balance the facial structure.''',
    "Oval Face": '''
        Suitable Styles: Most styles, including Gulf and Turkish. Princess hijab is also appropriate.
        Options: Cover both forehead and cheeks if desired. Be cautious with the Spanish hijab if fuller figured.''',
    "Square Face": '''
        Avoid: Tight hijabs under the chin and covering forehead and cheekbones.
        Wrap: Head cover around the chin to conceal face width and arrange the hijab to round the face.
        Not Recommended: Turkish hijab style around the neck.''',
    "Round Face": '''
        Advice: Start the hijab at the hairline, place near cheekbones to shape the face more like an oval, avoid showing chin.
        Avoid Style: Spanish hijab style, suited for long, slender necks.''',
    "Rectangular Face": '''
        Opt for: Styles that round off the angular edges of the face, like loose drapes.
        Avoid: Styles that tighten around the jaw and forehead, accentuating length.
        Tips: Opt for voluminous styles that add width around the cheeks.''',
    "Diamond Face": '''
        Suitable Styles: Wide under-scarves to broaden the forehead and chin area.
        Avoid: Narrow headbands or styles that expose the forehead or chin.
        Tips: Emphasize the cheekbones with a slightly looser wrap around them.'''
}


# Checkboxes for each category
    if st.checkbox("Need makeup tips based on season?"):
        selected_seasonal_makeup = st.selectbox("Choose your seasonal makeup tips:", list(seasonal_makeup_tips.keys()))
    else:
        selected_seasonal_makeup = "No need"

    if st.checkbox("Need makeup tips based on face shape?"):
        selected_face_shape = st.selectbox("Choose tips based on your face shape:", list(face_shape_tips.keys()))
    else:
        selected_face_shape = "No need"

    if st.checkbox("Need nail polish tips based on skin tone?"):
        selected_nail_polish = st.selectbox("Select nail polish tips for your skin tone:", list(nail_polish_tips.keys()))
    else:
        selected_nail_polish = "No need"

    if st.checkbox("Need tips on typical makeup routines?"):
        selected_makeup_routine = st.selectbox("Select your typical makeup routines:", list(makeup_routines.keys()))
    else:
        selected_makeup_routine = "No need"

    if st.checkbox("Need tips on eye makeup styles?"):
        selected_eye_makeup = st.selectbox("Choose your preferred eye makeup styles:", list(eye_makeup_styles.keys()))
    else:
        selected_eye_makeup = "No need"
    if st.checkbox("Need tips on hijab styles based on face shape?"):
        selected_hijab_styles = st.selectbox("Select hijab styles based on your face shape:", list(hijab_styles.keys()))
    else:
        selected_hijab_styles = "No need"

    inp = ""
    if seasonal_makeup_tips.get(selected_seasonal_makeup):
        inp += "selected_seasonal_makeup information: " + seasonal_makeup_tips[selected_seasonal_makeup] + " "
    if face_shape_tips.get(selected_face_shape):
        inp += "selected_face_shape information: " + face_shape_tips[selected_face_shape] + " "
    if nail_polish_tips.get(selected_nail_polish):
        inp += "selected_nail_polish information: " + nail_polish_tips[selected_nail_polish] + " "
    if makeup_routines.get(selected_makeup_routine):
        inp += "selected_makeup_routine information: " + makeup_routines[selected_makeup_routine] + " "
    if eye_makeup_styles.get(selected_eye_makeup):
        inp += "selected_eye_makeup information: " + eye_makeup_styles[selected_eye_makeup] + " "
    if hijab_styles.get(selected_hijab_styles):
        inp += "selected_hijab_styles information: " + hijab_styles[selected_hijab_styles]

    inp = inp.strip()  # To remove any trailing space


    def generate_content(inp):
        load_dotenv()
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=gemini_api_key)
        try:

            # Assuming the model requires a PIL Image; if it requires another format you might need to adjust this
            prompt = f'''You are an expert in providing the best facial makeup tips based on the following information: 
            
            Sort all information clearly and avoid repeating any parts. Please personalize the answer.
            Response must be as clear points asn ONLY in Arabic Langauge'''
            model = genai.GenerativeModel('gemini-1.0-pro-latest')
            response = model.generate_content([prompt])
            return response.text
        except Exception as e:
            st.error("Failed to generate content: {}".format(e))
            return str(str(None))



    if st.button("Generate Recommandation"):

            processed_text = generate_content(inp)

            if processed_text:
                # Display the result from generate_content
                st.markdown(f"<div style='direction: rtl; text-align: right;'>{processed_text}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
