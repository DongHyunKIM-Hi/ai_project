import os
import streamlit as st
import pandas as pd
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.title('운명의 구슬 🥸')

volume = st.slider('긍정지수를 선택해주세요', min_value=0, max_value=100, step=5, value=50)
input_birth = st.date_input('생년월일은 선택해주세요', value=pd.to_datetime('2023-06-01'))

with st.form("개인 input data를 입력해주세요"):
    input_name = st.text_input("이름을 입력해주세요")
    input_mbti = st.text_area("mbti를 입력해주세요")
    submitted = st.form_submit_button("제출")
    if submitted:
        st.write("이름: " + input_name)
        st.write("mbti: " + input_mbti)
        st.write("생년월일: " + input_birth.strftime('%Y-%m-%d'))
        st.write("선택된 value: " + str(volume))
    else:
        st.write("이름: ")
        st.write("mbti: ")
        st.write("생년월일: ")

if st.button('생성하기'):
    with st.spinner('생성 중입니다.'):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "이름은" + input_name + "이고 mbti는 " + input_mbti + "이고 생년월일은 " + input_birth.strftime('%Y-%m-%d'),
                },
                {
                    "role": "system",
                    "content": "입력 받은 인물에 대한 150자 이내의 10년후 미래를 예측해줘 미래가 긍정적인지 부정적인지는 100% 중에서 " +  str(volume) + "만큼 긍정적이게 작성해줘" ,
                }
            ],
            model="gpt-4",
        )
    
        # 이미지 생성 요청
        response = client.images.generate(
            model="dall-e-3",
            prompt=chat_completion.choices[0].message.content + "에 어울리는 이미지",
            size="1024x1024",
            quality="standard",
            n=1
        )
    
    result = chat_completion.choices[0].message.content
    image_url = response.data[0].url
    st.write(result)

    # 애니메이션을 위한 HTML 및 CSS 삽입
    animation_html = f"""
    <style>
    .rotate-and-fade {{
        animation: spin-and-fade 4s forwards;
    }}
    @keyframes spin-and-fade {{
        0% {{
            transform: rotate(0deg);
            opacity: 1;
        }}
        100% {{
            transform: rotate(360deg);
            opacity: 0;
        }}
    }}
    </style>
    <img src="{image_url}" class="rotate-and-fade" style="width:100%;max-width:600px;" />
    """
    
    st.markdown(animation_html, unsafe_allow_html=True)
