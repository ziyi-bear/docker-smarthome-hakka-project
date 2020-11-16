#!/usr/bin/env python
# coding: utf-8

# ## 客家語音(文字轉語音服務)
# 
# * [CSIAP客家語文化特徵詞](http://gohakka.org/CSIAP/App/)
# * [服務.意傳.台灣](https://xn--lhrz38b.xn--v0qr21b.xn--kpry57d/)
# * [標漢字音標](https://服務.意傳.台灣/標漢字音標)
# * [語音合成](https://服務.意傳.台灣/語音合成)

# In[ ]:


import requests
import json


# In[2]:


from flask import Flask, request
app = Flask(__name__)


# In[3]:


hakkadic_url = 'http://gohakka.org/hakkadic/api.py'
hakka4Chinese_url = 'https://服務.意傳.台灣/標漢字音標'
hakka4Audio_url = 'https://服務.意傳.台灣/語音合成'


# ### 客家語文化特徵詞服務
# 範例: `妳好`->`汝好`

# In[4]:


def gethakkadic(targetText):
    global hakkadic_url
    response = requests.get(hakkadic_url, params={'text': targetText})
    response_obj = json.loads(response.content)
    print(response_obj)
    return response_obj['hakka_text']


# ### 標漢字音標特徵服務
# 範例: `汝好`->`汝 好｜hau`

# In[5]:


def gethakka4Chinese(targetText):
    global hakka4Chinese_url
    response = requests.get(hakka4Chinese_url, params={'查詢腔口': '四縣腔', '查詢語句': targetText})
    response_obj = json.loads(response.content)
    print(response_obj)
    return response_obj['分詞']


# ### 語音合成
# 範例: `汝 好｜hau`->``wav音訊檔案`

# In[6]:


def gethakka4Audio(targetText, targetFileName):
    global hakka4Audio_url
    response = requests.get(hakka4Audio_url, params={'查詢腔口': '四縣腔', '查詢語句': targetText})
    filename = '{}.wav'.format(targetFileName)
    # 儲存檔案下來一份到伺服器
    with open(filename, 'wb') as f:
        f.write(response.content)
    return response.content


# ### 完整國字轉客語語音

# In[7]:


def text2hakkaSpeech(targetText):
    hakka_text = gethakkadic(targetText)
    hakka_text = gethakka4Chinese(hakka_text)
    return gethakka4Audio(hakka_text, targetText)


# ### 伺服器微服務
# 
# * `/`: 將國字`妳好`轉換成`客家語音檔案`  
# GET: `text`
# * `/hakkadic`: 將國字`妳好`轉換成  
# GET: `text`
# * `/hakka4chinese`  
# GET: `text`

# In[8]:


### 請求URL
@app.route('/')
def text2hakkaSpeech_main():
    text = request.args.get('text')
    return text2hakkaSpeech(text)


# In[9]:


@app.route('/hakkadic')
def gethakkadic_main():
    text = request.args.get('text')
    return gethakkadic(text)


# In[10]:


@app.route('/hakka4chinese')
def gethakka4Chinese_main():
    text = request.args.get('text')
    return gethakka4Chinese(text)


# ### 執行範例

# In[12]:


audioFileContent = text2hakkaSpeech('熊熊')


# In[ ]:


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)

