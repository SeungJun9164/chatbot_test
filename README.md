# chatbot_test

# 영어 챗봇 구현해보기
### pytorch_chatbot_tutorial.ipynb
- https://tutorials.pytorch.kr/beginner/chatbot_tutorial.html

### bert_en_pytorch_chatbot_tutorial.ipynb
- bert_ko_pytorch_chatbot_tutorial 와 동시에 진행 중
- 동일한 증상때문에 실행불가능
- 수정중...


# 한국어 챗봇 구현해보기
### ko_pytorch_chatbot_tutorial 
- https://github.com/songys/Chatbot_data 의 데이터를 이용하여 구현
- 제대로 된 채팅이 이루어 지지 않음

### ko_pytorch_chatbot_tutorial_2
- https://aihub.or.kr/ 의 대화형 한글 에이전트 데이터셋을 이용하여 구현
- 좀 더 많은 데이터와 1번 이상의 대화가 이루어지는 데이터로 구현해보았지만 마찬가지로 제대로 된 대화가 이루어지지 않음

### ko_pytorch_chatbot_tutorial_3
- 2를 개선 시켜 데이터 정제 수정
- 제대로 대화가 이루어지는 질문 발견(ex. Q : 어디야?, A : 사무실 / Q : 왜 그렇게 놀래?, A : 그냥. 등)
- 여전히 제대로 된 대화 불가능

### bert_ko_pytorch_chatbot_tutorial
- 3를 개선 시켜 bert(bert-base-multilingual-cased)를 이용하여 데이터 분리함
- bert의 vocab을 이용하여 대화를 인코딩까지 완료함
- 하지만 인코딩한 길이가 길어지는 문제가 있음. - 수정완료
- 인코딩, 디코딩 부분까지 수정완료. 메모리 부족으로 훈련이 안되는데 어딘가 잘못된듯 - 수정완료(배치사이즈 64 -> 32로 수정)
- 훈련까지 마치고 대화를 수행하면 동일한 말만 반복하는 문제발생, 대답을 할때 ##과 같이 대답을 하는 문제
- 모든 부분 기존 tutorial과 차이점이 없어 훈련 수 12000으로 증가시켜 
