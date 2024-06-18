#!/usr/bin/env python
# coding: utf-8

# In[2]:


#importing packages i'd need
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


#importing dataset into a dataframe
df = pd.read_csv("audible.csv")
df.head(10)


# In[3]:


#checking for null values
df.isna().sum()


# In[4]:


#checking for duplicates
df.duplicated().sum()


# In[4]:


#removing unnecessary text in the author and narrator columns
df['author'] = df['author'].str.replace('Writtenby:', "")
df['narrator'] = df['narrator'].str.replace('Narratedby:', "")
df


# In[5]:


#creating a function to split names in the author and narrators column
def split_names(data, column_name):
    pattern = re.compile(r'(?<=[a-z])(?=[A-Z])')
    data[column_name] = data[column_name].apply(lambda x: ' '.join(pattern.split(x, 1)))
    return data
df = split_names(df, 'author')
df


# In[6]:


df = split_names(df, 'narrator')
df


# In[7]:


#workiing on time column to convert to minutes
df['time'] = df['time'].astype(str)
hours = df['time'].str.extract(r'(\d+)\s*hrs').astype(float)
minutes = df['time'].str.extract(r'(\d+)\s*mins').astype(float)
hours_in_min = hours * 60
total_min = hours_in_min.fillna(0) + minutes.fillna(0)
df['time'] = total_min
df


# In[8]:


#copying stars column to create ratings column inorder to separate stars and ratings 
df['ratings'] = df['stars']
df


# In[9]:


#cleaning the stars column
df['stars'] = df['stars'].str.extract(r'(\d+\.\d+|\d+)')
df['stars']


# In[10]:


df['stars'].fillna(value=0.0, inplace=True)
df


# In[11]:


#working on the ratings column
df['ratings'] = df['ratings'].str.extract(r'(\d+) ratings')
df['ratings']


# In[12]:


df['ratings'].fillna(value=0.0, inplace=True)
df


# In[13]:


#Visualization to know which movies are longest
movies_time = df.groupby('name')['time'].mean().sort_values(ascending=False)

#selecting the five longest movies
top_movies = movies_time.head(5).index

#plot
plt.figure(figsize=(10, 6))
plt.pie(movies_time[top_movies], labels=top_movies, autopct='%1.1f%%')
plt.title('Longest Movies, Top 5')
plt.axis('equal') #to obtain perfect circle
plt.show()


# In[20]:


df['stars'] = pd.to_numeric(df['stars'], errors='coerce')

movies_ratings = df.groupby('name')['stars'].mean().sort_values(ascending=False)
top_rated_movies = movies_ratings.head(15)

plt.figure(figsize=(10, 6))
plt.scatter(top_rated_movies.index, top_rated_movies.values)
plt.title('Top 10 Rated')
plt.xlabel('Movie Name')
plt.ylabel('Ratings')
plt.xticks(rotation=90)
plt.show()


# In[15]:


#We convert price column into numeric values to enable visualizing the most expensive movies
df['price'] = pd.to_numeric(df['price'], errors='coerce')

movies_price = df.groupby('name')['price'].mean().sort_values(ascending=False)
top_movies = movies_price.head(10)

plt.figure(figsize=(10, 6))
plt.scatter(top_movies.index, top_movies.values)
plt.title('Top 10 Movies by Average Revenue')
plt.xlabel('Movie Name')
plt.ylabel('Average Revenue')
plt.xticks(rotation=90)
plt.show()


# In[14]:


#histogram plot to understand language distribution of the movies
plt.figure(figsize=(8,6))
sns.countplot(x=df['language'])
plt.title('Distribution of language Values')
plt.xticks(rotation=90)
plt.show()


# In[ ]:




