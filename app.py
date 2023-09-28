import streamlit as st
from PIL import Image

from streamlit_float import float_init

def init():
    st.session_state.results = []
    st.session_state.result = ''
    st.session_state.before = None

def page_config():
    # page config
    icon = Image.open('./static/app_icon.ico')
    st.set_page_config(
        page_title="제1회 코육대 : 계산기",
        page_icon=icon,
        layout="centered",
    )

def footer():
    # footer : copyright & banner image
    float_init()
    banner = st.container()

    markdown_code = """
                    <style>
                        .markdown-style {
                            border-top: 1px solid black;
                            padding: 10px 0;
                            display: flex;  /* Flexbox 레이아웃을 사용 */
                            align-items: center;  /* Flexbox의 수직 중앙 정렬 */
                        }
                        .centered-image {
                            display: block;
                            margin: auto; /* 이미지를 오른쪽 정렬 */
                            width: 40%;
                            height: 40%;
                        }
                        .centered-text {
                            flex: 1;  /* 텍스트를 가운데 정렬 */
                            text-align: center;  /* 텍스트 내용 가운데 정렬 */
                            font-size: 1.0em;  /* 기본 폰트 크기 */
                            font-weight: bold;  /* 볼드체 */
                        }
                    </style>

                    <div class="markdown-style">
                        <a href="https://github.com/leadbreak/coyukdae" class="centered-text">Copyright &copy; 2023 QscarKIM - All Rights Reserved.</a>
                        <a href="https://hanghaeplus-coyukdae.oopy.io/">
                        <img src="app/static/coyukdae_banner.png" class="centered-image">
                    </a>
                    </div>
                        """
    banner.float("bottom: 1rem;background-color: white;")

    banner.markdown(markdown_code,
        unsafe_allow_html=True,
    )

def title():
    con1, con2 = st.columns(2)
    with con1:
        st.title(':red[제 1회 코육대]')
        st.header(':grey[세뱃돈 계산기]')
    title_markdown = """
                    <style>
                        .markdown-style2 {
                            padding: 10px 0;
                            display: flex;  /* Flexbox 레이아웃을 사용 */
                            align-items: center;  /* Flexbox의 수직 중앙 정렬 */
                        }
                        .centered-image2 {
                            display: block;
                            margin: auto; /* 이미지를 오른쪽 정렬 */
                            width: 80%;
                            height: 80%;
                        }

                    </style>

                    <div class="markdown-style2">
                        <a href="https://hanghaeplus-coyukdae.oopy.io/">
                        <img src="app/static/coyukdae_title.png" class="centered-image2">
                    </a>
                    </div>
                    """
    con2.markdown(title_markdown,
    unsafe_allow_html=True,
    )   



def update_result(category:str, result):
    '''
    1. 10자리를 넘어가는 숫자는 infinity로 표기
    2. 연산자 다음 숫자를 입력하지 않을 경우, alert로 표기
    3. 0 나누기 0은 숫자 아님으로 표기
    '''


    if category=='cal':
        st.session_state.results.append(str(st.session_state.result))
        if st.session_state.before == 'num':            
            results = ''.join(st.session_state.results)
            try :
                result = str(int(eval(results)))
            except ZeroDivisionError:
                result = '숫자 아님'

            if len(str(result)) > 10:
                result = 'Infinity'
            elif str(result) == '99':
                st.balloons()
        else : # = 전에 숫자가 아니었을 경우
            result = 'alert'

        st.session_state.results.append('=')
        st.session_state.result = result
    
    elif category=='oper':
        if category == st.session_state.before:
            if not st.session_state.results[-1].isnumeric() :
                st.session_state.results.pop()
        elif st.session_state.before == None:
            st.session_state.results.pop()
            st.session_state.results.append(str(0))
            st.session_state.results.append(str(st.session_state.result))
        else :
            st.session_state.results.append(str(st.session_state.result))
        st.session_state.result = str(result)

    elif category=='num' :
        if category == st.session_state.before:
            if (len(st.session_state.result) > 0) & (st.session_state.result[0] == '0'):
                st.session_state.result = ''
            st.session_state.result = str(st.session_state.result)+str(result)
        else :
            st.session_state.results.append(str(st.session_state.result))
            st.session_state.result = str(result)

    st.session_state.before = category

def eraser(func:str):
    if func == '0':
        st.session_state.result = st.session_state.result[:-1]
    elif func == '1':
        st.session_state.result = st.session_state.results.pop()
    elif func == '2':
        init()


def calculator():
    con = st.empty()
    col1_0, col1_1, col1_2, col1_3, col1_4 = st.columns(5)
    col2_0, col2_1, col2_2, col2_3, col2_4 = st.columns(5)
    col3_0, col3_1, col3_2, col3_3, col3_4 = st.columns(5)
    col4_1, col4_2, col4_3, col4_4 = st.columns([2,1,1,1])
    con2 = st.container()

    express_rule = {'' : 0,
                    '*': '×',
                    '/': '÷',
                    '+': '＋',
                    '-': '－'}
    
    if st.session_state.result in express_rule.keys():
        expression = express_rule[st.session_state.result]
    else :
        expression = st.session_state.result

    con.text_input('', value=expression, disabled=True)
    col1_0.button(label='◀', type='primary', help='clear last input', use_container_width=True, on_click=eraser, args=('0'))
    col1_1.button(label='7', use_container_width=True, on_click=update_result, args=('num', '7'))
    col1_2.button(label='8', use_container_width=True, on_click=update_result, args=('num', '8'))
    col1_3.button(label='9', use_container_width=True, on_click=update_result, args=('num', '9'))
    col1_4.button(label='÷', use_container_width=True, on_click=update_result, args=('oper', '/'))

    col2_0.button(label='C', type='primary', help='clear current input', use_container_width=True, on_click=eraser, args=('1'))
    col2_1.button(label='4', use_container_width=True, on_click=update_result, args=('num', '4'))
    col2_2.button(label='5', use_container_width=True, on_click=update_result, args=('num', '5'))
    col2_3.button(label='6', use_container_width=True, on_click=update_result, args=('num', '6'))
    col2_4.button(label='×', use_container_width=True, on_click=update_result, args=('oper', '*'))

    col3_0.button(label='AC', type='primary', help='clear all inputs', use_container_width=True, on_click=eraser, args=('2'))
    col3_1.button(label='1', use_container_width=True, on_click=update_result, args=('num', '1'))
    col3_2.button(label='2', use_container_width=True, on_click=update_result, args=('num', '2'))
    col3_3.button(label='3', use_container_width=True, on_click=update_result, args=('num', '3'))
    col3_4.button(label='－', use_container_width=True, on_click=update_result, args=('oper', '-'))

    col4_1.button(label='0', use_container_width=True, on_click=update_result, args=('num', '0'))
    col4_2.button(label='00', use_container_width=True, on_click=update_result, args=('num', '00'))
    col4_3.button(label='＝', use_container_width=True, on_click=update_result, args=('cal', '='))
    col4_4.button(label='＋', use_container_width=True, on_click=update_result, args=('oper', '+'))

    history = st.session_state.results+[st.session_state.result]
    if '=' in history:
        if history[-2] == '=':
            st.session_state.results = []
            st.session_state.result = ''
    history_log = '\n'.join(history).strip()
    st.text_area(label='input history', value=history_log, height=500, disabled=True)

if __name__ == '__main__':
    page_config()

    if 'result' not in st.session_state.keys():
        init()

    # Title
    title()    

    # Main
    calculator()

    # footer
    footer()