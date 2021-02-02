# chatbot_test

# 영어 챗봇 구현해보기
### pytorch_chatbot_tutorial
- [파이토치 튜토리얼](https://tutorials.pytorch.kr/beginner/chatbot_tutorial.html) \
[바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/pytorch_chatbot_tutorial.ipynb)

### bert_en_pytorch_chatbot_tutorial
- bert_ko_pytorch_chatbot_tutorial 와 동시에 진행 중
- 훈련 횟수 3만번
![image](https://user-images.githubusercontent.com/60804222/106424197-1df66300-64a5-11eb-8db2-046f3b767011.png) \
- 훈련 횟수 6만번
![image](https://user-images.githubusercontent.com/60804222/106560907-27e29980-656b-11eb-9963-2ba0af18f4f8.png)
- 현재 bert_ko와 마찬가지로 제대로 된 대답 불가능 \
[주피터 바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/bert_en_pytorch_chatbot_tutorial.ipynb)
[파이썬 바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/bert_en_pytorch_chatbot_tutorial.py)

# 한국어 챗봇 구현해보기
### ko_pytorch_chatbot_tutorial 
- [송영숙님의 깃허브](https://github.com/songys/Chatbot_data)의 데이터를 이용하여 구현
- 제대로 된 채팅이 이루어 지지 않음 \
[바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/ko_pytorch_chatbot_tutorial.ipynb)

### ko_pytorch_chatbot_tutorial_2
- [AIhub](https://aihub.or.kr) 의 대화형 한글 에이전트 데이터셋을 이용하여 구현
- 좀 더 많은 데이터와 1번 이상의 대화가 이루어지는 데이터로 구현해보았지만 마찬가지로 제대로 된 대화가 이루어지지 않음 \
[바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/ko_pytorch_chatbot_tutorial_2.ipynb)

### ko_pytorch_chatbot_tutorial_3
- 2를 개선 시켜 데이터 정제 수정
- 제대로 대화가 이루어지는 질문 발견(ex. Q : 어디야?, A : 사무실 / Q : 왜 그렇게 놀래?, A : 그냥. 등)
- 여전히 제대로 된 대화 불가능 \
[바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/ko_pytorch_chatbot_tutorial_3.ipynb)

### bert_ko_pytorch_chatbot_tutorial
- 3를 개선 시켜 [bert(bert-base-multilingual-cased)](https://arxiv.org/abs/1810.04805)를 이용하여 데이터 분리함
- bert의 vocab을 이용하여 대화를 인코딩까지 완료함
- 인코딩, 디코딩 부분까지 수정완료. 메모리 부족으로 훈련이 안되는데 어딘가 잘못된듯 - 수정완료(배치사이즈 64 -> 32로 수정)
- 훈련까지 마치고 대화를 수행하면 동일한 말만 반복하는 문제발생 - 수정완료(훈련 횟수 4000 -> 12000)
- 모든 부분 기존 tutorial과 차이점이 없어 훈련 수 12000으로 증가시켜 진행 - 여전히 제대로 된 대화 안됨
- MAX_LENGTH = 30으로 증가 / 훈련 횟 수 6만번으로 증가시켜서 진행 중 - 여전히 제대로 된 대화 불가능 \
![bert_ko_capture](https://user-images.githubusercontent.com/60804222/106237136-7af1df00-6241-11eb-8aa2-7d2a7282e905.PNG) \
[.ipynb 바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/bert_ko_pytorch_chatbot_tutorial.ipynb)
[.py 바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/bert_ko_pytorch_chatbot_tutorial.py)
- SKTBrain의 [KoBert](https://github.com/SKTBrain/KoBERT)를 사용해 볼 계획 \

### kobert_ko_pytorch_chatbot_tutorial
- SKTBrain의 [KoBert](https://github.com/SKTBrain/KoBERT)를 사용해 토큰화 부터 다시 진행 중
- 문장을 토큰화 시키는 데까지 성공, 토큰화 하여 인코딩화를 어떻게 해야할지 검색, 고민 중
- 인코딩화 까지 완료하여 채팅하는 데 까지 완료, 제대로 된 대답 불가능 \
[바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/kobert_ko_pytorch_chatbot_tutorial.ipynb)

