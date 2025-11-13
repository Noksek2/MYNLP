
import re
def preprocess_text(text):
  arr=[]
  s=text.lower()
  for s2 in re.split(r'[.,:)!? ]+',s):
    if s2!='':arr.append(s2)
  return arr

def make_word_map(sentences):
  word_map=[]
  sentence_pre=[]
  for s in sentences:
    m=dict()
    text=preprocess_text(s)
    sentence_pre.append(text)
    for word in text:
      m[word]=1 if word not in m else m[word]+1
    word_map.append(m)
  print('word_map:',word_map)
  print('전처리 후 토큰',sentence_pre)
  return (word_map,sentence_pre)

def make_answer_map(word_map,sentence_ans,sentence_pre):
  ans_max=0
  N=len(sentence_ans)

  for ans in sentence_ans:
    if ans_max<ans: ans_max=ans
  word_answer_map=[dict() for _ in range(ans_max+1)]
  word_answer_cnt=[0]*(ans_max+1)
  for i in range(N):
    loc=sentence_ans[i]
    for word,word_cnt in word_map[i].items():
      if not (word in word_answer_map[loc]):
        word_answer_map[loc][word]=word_cnt
      else: word_answer_map[loc][word]+=word_cnt
      #word_answer_map[loc]
    word_answer_cnt[loc]+=len(sentence_pre[i])

  return (word_answer_map,word_answer_cnt)

def naive_eval_sentence(word_answer,text):
  ans_map,ans_cnt=word_answer
  text_list=preprocess_text(text)
  print(text_list)
  A=len(ans_cnt)
  p=[0] * A
  for i in range(A):
    cnt=1
    for word in text_list:
      if word in ans_map[i]:
        _p=ans_map[i][word]
      else: _p=0.00000001
      cnt*=(_p/ans_cnt[i])
      print(_p,end=', ')
    p[i]=cnt
    print('=',p[i])
  return p

def eval_p(p,label):
  max_i=0
  for i in range(len(p)):
    if p[max_i]<p[i]:
      max_i=i
  return label[max_i],max_i


class NaiveEval:
  def __init__(self,sentences,answer):
    self.sentences=sentences
    self.label=[]
    self.answer=[]
    for a in answer:
      if not (a in self.label):
        self.label.append(a)
        self.answer.append(len(self.label)-1)
      else:
        self.answer.append(self.label.index(a))
    print(self.answer,self.label)
  def expect(self):
    self.word_map,self.sentence_pre=make_word_map(self.sentences)
    self.word_answer=make_answer_map(self.word_map,self.answer,self.sentence_pre)

  def eval(self,text):
    p=naive_eval_sentence(self.word_answer,text)
    res=eval_p(p,self.label)
    print(res[0])
train_data = [
    "I love this product, it's amazing!",
    "I'm so happy with the service.",
    "I'm disappointed in the quality.",
    "I'm not satisfied with the outcome.",
]
ans_data=[
    'good',
    'good',
    'bad',
    'bad'
]

n=NaiveEval(train_data,ans_data)
n.expect()
n.eval('happy')