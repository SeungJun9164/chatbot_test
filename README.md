# chatbot_test

# 영어 챗봇 튜토리얼 모델로 구현해보기
### pytorch_chatbot_tutorial
- [파이토치 튜토리얼](https://tutorials.pytorch.kr/beginner/chatbot_tutorial.html) \
[바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/pytorch_chatbot_tutorial.ipynb)

### bert_en_pytorch_chatbot_tutorial
- [bert 논문](https://arxiv.org/abs/1810.04805)
- 파이토치 튜토리얼과 동일한 모델사용
- [bert(bert-base-multilingual-cased)](https://huggingface.co/transformers/pretrained_models.html)를 이용했을 경우 10만번 이상의 훈련이 필요 \
![image](https://user-images.githubusercontent.com/60804222/108584711-e170a580-7386-11eb-96b4-cafe4b33cd5a.png) 

- [bert(bert-large-uncased)](https://huggingface.co/transformers/pretrained_models.html)를 이용했을 경우 5만번 정도 진행하면 어느정도 대화 가능 \
![image](https://user-images.githubusercontent.com/60804222/108584725-f64d3900-7386-11eb-9bba-800bf043f74f.png) \
[주피터 바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/bert_en_pytorch_chatbot_tutorial.ipynb) 
[파이썬 바로가기](https://github.com/SeungJun9164/chatbot_test/blob/main/bert_en_pytorch_chatbot_tutorial.py)

# 한국어 챗봇 튜토리얼 모델로 구현해보기
***한국어 챗봇 튜토리얼 모델은 정상적으로 작동 되지 않음***
***현재 모델로는 한국어를 처리하기에 맞지 않다고 판단하여 더 이상 이 모델로는 구현하지 않을 것***
### ko_pytorch_chatbot_tutorial 
- [송영숙님의 깃허브](https://github.com/songys/Chatbot_data)의 데이터를 이용하여 구현
### ko_pytorch_chatbot_tutorial_2, ko_pytorch_chatbot_tutorial_3
- [AIhub](https://aihub.or.kr) 의 대화형 한글 에이전트 데이터셋을 이용하여 구현
### bert_ko_pytorch_chatbot_tutorial
- [bert(bert-base-multilingual-cased)](https://arxiv.org/abs/1810.04805)를 이용하여 데이터 분리함

### kobert_ko_pytorch_chatbot_tutorial
- SKTBrain의 [KoBert](https://github.com/SKTBrain/KoBERT)를 사용하여 구현
- 테스트중...
