import pandas as pd
# Extract the Date time
def date_time(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+]), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    result = re.match(pattern, s)
    if result:
        return True
    return False


# Extract contacts
def find_contact(s):
    s = s.split(":")
    if len(s) == 2:
        return True
    else:
        return False


# Extract Message
def getMassage(lines):
    splitline = lines.split('] ')
    datetime = splitline[0];
    date, times = datetime.split(', ')
    date = date.replace("[", "")
    time = times
    message = " ".join(splitline[1:])
        #message += i.split(': ')[1]
    #print(message)
    if find_contact(message):
        splitmessage = message.split(": ")
        author = splitmessage[0]
        message = splitmessage[1]
    else:
        author = None
    return date, time, author, message


# In[3]:


data = []
conversation = '_chat.txt'
with open(conversation, encoding="utf-8") as fp:
    fp.readline()
    messageBuffer = []
    date, time, author = None, None, None
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if line:
            # if date_time(line):
            # if len(messageBuffer) >0:
            messageBuffer.clear()
            date, time, author, message = getMassage(line)
            data.append([date, time, author, ''.join(message), 0, 0, 0])
            # data.append(line)
    # else:
    # messageBuffer.append(line)

# In[63]:


df = pd.DataFrame(data, columns=["Date", "Time", "Author", "Message", "Positive", "Negative", "Neutral"])
df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d', errors='ignore')
# data = df.dropna()
#print(df)
#print(data)
#print(type(data))
#print(df["Message"])
#print(df["Positive"])
#sys.exit(0)
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sentiments = SentimentIntensityAnalyzer()
df["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in df["Message"]]
df["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in df["Message"]]
df["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in df["Message"]]
df.head()
print(df)
sys.exit(0)
# In[39]:


x = sum(data["Positive"])
y = sum(data["Negative"])
z = sum(data["Neutral"])


def score(a, b, c):
    if (a > b) and (a > c):
        print("Positive ")
    if (b > a) and (b > c):
        print("Negative")
    if (c > a) and (c > b):
        print("Neutal")


score(x, y, z)

# In[20]:


df.Author.unique()

# In[21]:


media_messages = df[df['Message'] == 'Oke'].shape[0]
print(media_messages)


# In[38]:


def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list


# In[39]:


import regex

df["emoji"] = df["Message"].apply(split_count)
emojis = sum(df['emoji'].str.len())
df.head(50)

# In[40]:


total_emojis_list = list([a for b in df.emoji for a in b])
emoji_dict = dict(Counter(total_emojis_list))
emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
for i in emoji_dict:
    print(i)

# In[41]:
text = ""

# for review in data.Message:
# print(review)
# print(text)
print("There are {} words in all the messages.".format(len(text)))
stopwords = set(STOPWORDS)
# Generate a word cloud image
wordCloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
# Display the generated image:
# the matplotlib way:
plt.figure(figsize=(10, 5))
plt.imshow(wordCloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# In[ ]:
