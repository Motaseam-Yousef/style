import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

def main():
    # Load environment variables
    load_dotenv()


    # Streamlit app setup
    st.title("💄👄👠💅 Stylish 💅👠👄💄")
    st.markdown("## مرحبا سأساعد باختيار أفضل مكياج لك")

    # Configure the Generative AI model
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    chat = model.start_chat()

    # Examples for users
    examples = {
        "نصائح مكياج حسب الفصل": "أريد أفضل مكياج لبشرتي الحنطية في فصل الصيف",
        "نصائح حسب شكل الوجه": "أريد أفضل مكياج لوجهي المستدير لدي مقابلة عمل",
        "نصائح طلاء الأظافر": "للبشرة الفاتحة جدًا ما أفضل طلاء أظافر لي",
        "روتين المكياج": "إنها عطلة نهاية الأسبوع وأريد الخروج مع صديقتي ما أفضل مكياج لهذه المناسبة",
        "أساليب مكياج العيون": "أريد مكياج يظهر عيوني العسلية ويظهرني قوية",
        "نصائح لأنماط الحجاب": "ما أفضل لفة شال وأفضل لون لدي مقابلة عمل"
    }

    # Display examples in a sidebar with clickable options
    st.sidebar.header("أمثلة للاستفسارات")
    for category, example in examples.items():
        if st.sidebar.button(example, key=category):
            st.session_state['user_input'] = example

    # Input from user
    user_input = st.text_input("كيف يمكني اليوم مساعدتك لاختيار ستايلك؟", value=st.session_state.get('user_input', ''))

    # Handling button press
    if st.button("إرسال"):
        if user_input:
            try:
                # Additional instructions for the AI model
                user_input += '''
                \nالرد فقط باللغة العربية
                اذا لم يكن السؤال يتعلق بالمكياج أو الشعر او طلاء الاظافر او العناية بالبشرة الرجاء الرد بعذرا أنا هنا لمساعدتك بستايلك
                '''
                response = chat.send_message(user_input)
                # Displaying response
                st.markdown(f"<div style='direction: rtl; text-align: right;'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("فشل في التواصل مع نموذج الذكاء الاصطناعي: {}".format(e))

if __name__ == "__main__":
    main()
