# chatbot_test

# 영어 챗봇 구현해보기
### pytorch_chatbot_tutorial.ipynb
- https://tutorials.pytorch.kr/beginner/chatbot_tutorial.html

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
- 3를 개선 시켜 bert를 이용하여 데이터 분리함
- bert의 vocab을 이용하여 대화를 인코딩까지 완료함
- 하지만 인코딩한 길이가 길어지는 문제가 있음.
- 길이가 길어서 그런지 훈련이 되지 않음.
- 수정중...
