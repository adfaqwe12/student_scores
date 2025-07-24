# student_scores
import streamlit as st
import re
import pandas as pd
from io import StringIO

stu_name = {
    "중1-1": ["사무엘", "이예빈", "심규현", "이하준", "김태현", "김수현", "김단아", "유지훈", "이수빈", "서재원"],
    "중1-2": ["최서우", "권태현", "김나은", "전시영", "양여원", "엄준상", "장윤승", "유한준"],
    "중1-3": ["최서연", "이시완", "우상민", "서유준", "양서준"],
    "중1-4": ["손민준", "윤가람"],
    "중1-5": ["안예승", "안예담", "정수연"],
    "중1-6": ["이다경", "최문수", "권서율", "박수혁", "김민지", "고주원", "윤동건", "최지원"],
    "중1-7": ["최여울", "추윤지", "김민주2", "오나현", "강채윤", "김채윤", "이미르", "정의찬", "윤세인", "홍서우", "장윤재", "전유진", "한재현", "김민준4"],
    "중1-8": ["전지후", "박서연2", "조연우3", "김세빈", "김민솔", "윤도하", "김연욱", "손연주", "장세준", "김유섭", "최혜원", "장규리"],
    "중1-9": ["정하율", "김나헌", "박기정", "박채윤", "하주안", "정범준"],
    "중1-10": ["우아립", "김호연", "황창현", "유지희", "김시은2"],
    "중1-11": ["조원준", "김민석", "한유진2", "정현준", "김동하", "이하은3", "김시은", "김민재3", "김민서6", "문지우", "김승훈", "최혜원"],
    "중1-12": ["김서진4", "진재우", "김나현", "민시윤", "이민하", "신지우2", "안아현", "이동연"],
    "중1-13": ["김하연", "원예송", "이재준2", "이소율", "이도영", "이정민3", "강유주", "이지현", "박현서", "김도연", "강연우"],
    "중2-1": ["권민용", "정지현", "장민준", "임승건", "전우주", "박정연", "함기태", "주요한", "강현민", "고소원", "김단효", "김지오2"],
    "중2-2": ["임지혜", "오준엽", "김유빈", "김도훈"],
    "중2-3": ["송은모", "전서현", "곽민석"],
    "중2-4": ["김남혁", "손범식", "유준민", "안효주2", "설재호"],
    "중2-5": ["임동길", "김세윤", "민윤홍", "이승석", "김도담", "함태경"],
    "중3-1": ["김강비", "윤서진", "김건민", "양주혁", "송유나", "전지훈2", "함시연", "유서희", "서효은", "류하연", "정나윤"],
    "중3-2": ["장세윤", "김온유", "심재현", "권민재", "이서준4", "최윤희", "김다연"],
    "중3-3": ["윤정욱", "이시후", "김준호", "장준", "곽대성", "김범진", "고슬아"],
    "대성상지1": ["권민결", "방건우", "최형우", "김민준", "김하림", "김효인", "이다경"],
    "원고육민1": ["이성준", "이민재", "채예성", "최형욱", "박윤우", "김도윤", "최찬영", "김재민"],
    "진광치악1": ["한승민", "박지성", "김태준", "박주호", "민현정", "금경민", "김루아"],
    "원여북원섬강1": ["김소리", "한소현", "조인서", "손혜림", "차민지", "김서경", "정윤지"],
    "상지2": ["최윤아", "유민정"],
    "원고2": ["채승우", "김재현", "이한솔", "손민영", "이지안"],
    "치악2": ["이민준", "박소정", "김용석"],
    "북원2": ["오서윤", "임희수", "한효주"],
    "원여대성진광2": ["이다현", "김민준", "이유성", "지혜찬", "표하민"],
    "고3": ["류예서", "박선경", "김신형", "송정호", "김세현", "김윤기"]
}

pattern = r"^([가-힣0-9]+)\s*(\d+/(20|30|40))?\s*(\((.*?)\)|\w+)?\s*(결시|결석)?$"

st.title("학생 점수 자동 정리 웹앱")
st.write("텍스트 파일을 업로드하거나, 아래에 점수표를 붙여넣으세요.")

mode = st.radio("입력 방식 선택", ("파일 업로드", "텍스트 직접 입력"))

if mode == "파일 업로드":
    uploaded_file = st.file_uploader("파일을 선택하세요 (.txt)", type=["txt"])
    if uploaded_file:
        text = StringIO(uploaded_file.read().decode("utf-8")).read()
    else:
        text = ""
else:
    text = st.text_area("여기에 학생 점수표를 붙여넣으세요.", height=300)

if text:
    score_dict = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.findall(pattern, line)
        if match:
            row = match[0]
            name = row[0]
            score = row[1] or ""
            absent = row[5] or ""
            score_dict[name] = score if not absent else absent

    name_list = list(score_dict.keys())

    stu_list = list(stu_name.values())
    stu_class_list = list(stu_name.keys())
    max_intersection = 0
    max_index = 0
    for i, class_name in enumerate(stu_list):
        inter = set(class_name) & set(name_list)
        if len(inter) > max_intersection:
            max_intersection = len(inter)
            max_index = i

    target_class = stu_class_list[max_index]
    st.subheader(f"자동 인식된 반: **{target_class}**")

    ordered_students = stu_name[target_class]
    data = {
        "이름": ordered_students,
        "점수/결석": [score_dict.get(name, "") for name in ordered_students]
    }
    df = pd.DataFrame(data)

    st.dataframe(df, hide_index=True, use_container_width=True)

    # 텍스트(복사용) 생성 - csv(쉼표 구분)
    text_lines = ["이름,점수/결석"]
    for name, score in zip(ordered_students, [score_dict.get(name, "") for name in ordered_students]):
        text_lines.append(f"{name},{score}")

    st.text_area(
        "아래 내용을 복사해서 사용하세요 (엑셀/스프레드시트에 바로 붙여넣기 가능):",
        value="\n".join(text_lines),
        height=250
    )

else:
    st.info("좌측에서 파일을 업로드하거나 점수표를 붙여넣으면 결과가 나타납니다.")