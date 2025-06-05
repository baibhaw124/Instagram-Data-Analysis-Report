import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from collections import Counter

# Load data
df = pd.read_csv("comments.csv")

# Clean column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Clean comment text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[@#]\w+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    return text.strip()

df['cleaned_comment'] = df['comment'].apply(clean_text)

# Word frequency
all_words = ' '.join(df['cleaned_comment']).split()
word_freq = Counter(all_words)
common_words = word_freq.most_common(20)

# Top 20 common words - Bar Plot
plt.figure(figsize=(12, 6))
words, freqs = zip(*common_words)
sns.barplot(x=list(freqs), y=list(words), palette="viridis")
plt.title("Top 20 Most Common Words in Comments")
plt.xlabel("Frequency")
plt.ylabel("Words")
plt.tight_layout()
plt.show()

# Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(all_words))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud of Comments")
plt.show()

# Comments over time
df['created_timestamp'] = pd.to_datetime(df['created_timestamp'], errors='coerce')
df['date'] = df['created_timestamp'].dt.date
comments_per_day = df.groupby('date').size()

plt.figure(figsize=(12, 5))
comments_per_day.plot()
plt.title("Number of Comments Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Comments")
plt.tight_layout()
plt.show()

# Emoji usage distribution
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='emoji_used', palette="Set2")
plt.title("Emoji Usage in Comments")
plt.xlabel("Emoji Used")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

#  Hashtag usage distribution
plt.figure(figsize=(8, 5))
sns.histplot(df['hashtags_used_count'].dropna(), bins=10, kde=True, color="skyblue")
plt.title("Distribution of Hashtags Used per Comment")
plt.xlabel("Hashtags Used Count")
plt.ylabel("Number of Comments")
plt.tight_layout()
plt.show()

# Top active users (by user__id)
top_users = df['user__id'].value_counts().head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_users.values, y=top_users.index.astype(str), palette="magma")
plt.title("Top 10 Most Active Users")
plt.xlabel("Number of Comments")
plt.ylabel("User ID")
plt.tight_layout()
plt.show()


