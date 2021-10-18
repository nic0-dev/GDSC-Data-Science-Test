# This is the file you will need to edit in order to complete assignment 1
# You may create additional functions, but all code must be contained within this file


# Some starting imports are provided, these will be accessible by all functions.
# You may need to import additional items
import os
import nltk
import numpy as np
import json
import pandas as pd
import re
from matplotlib import pyplot as plt
# nltk.download()
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# You should use these two variable to refer the location of the JSON data file and the folder containing the news articles.
# Under no circumstances should you hardcode a path to the folder on your computer (e.g. C:\Chris\Assignment\data\data.json) as this path will not exist on any machine but yours.
datafilepath = 'data/data.json'
articlespath = 'data/football'

def task1():
    #Complete task 1 here
    with open(datafilepath, encoding="utf8") as f:
        data = json.load(f)
    return sorted(data['teams_codes'])
    
def task2():
    #Complete task 2 here
    with open(datafilepath, encoding="utf8") as f:
        data = json.load(f)

    a = [i['club_code'] for i in data['clubs']]
    b = [i['goals_scored'] for i in data['clubs']]
    c = [i['goals_conceded'] for i in data['clubs']]

    df = pd.DataFrame({'team code': sorted(a), 'goals scored by team': [i for _, i in sorted(zip(a, b))], 'goals scored against team': [i for _, i in sorted(zip(a, c))]})
    return df.to_csv('task2.csv', index=False, encoding="utf8")
      
def task3():
    #Complete task 3 here
    name = []
    score = []
    for filename in os.listdir(articlespath):
        with open(os.path.join(articlespath, filename), encoding="utf8") as f:
            text = f.read()
            x = re.findall(' \d{1,2}-\d{1,2}', text)
            ans = 0
            if x:
                for s in x:
                    ans = max(sum([int(i) for i in s.split('-')]), ans)
        name.append(os.path.basename(os.path.join(articlespath, filename)))
        score.append(ans)

    df = pd.DataFrame({'filename': name, 'total_goals': score})
    return df.to_csv('task3.csv', index=False, encoding="utf8")

def task4():
    #Complete task 4 here
    name = []
    score = []
    for filename in os.listdir(articlespath):
        with open(os.path.join(articlespath, filename), encoding="utf8") as f:
            text = f.read()
            x = re.findall(' \d{1,2}-\d{1,2}', text)
            ans = 0
            if x:
                for s in x:
                    ans = max(sum([int(i) for i in s.split('-')]), ans)
        name.append(os.path.basename(os.path.join(articlespath, filename)))
        score.append(ans)

    df = pd.DataFrame({'filename': name, 'total_goals': score})


    quartile_1 = np.round(df['total_goals'].quantile(0.25), 2)
    quartile_3 = np.round(df['total_goals'].quantile(0.75), 2)
    iqr = np.round(quartile_3 - quartile_1, 2)

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_ticks_position('none')
    ax.grid(color='grey', axis='y', linestyle='-', linewidth=0.25, alpha=0.5)
    ax.boxplot(df['total_goals'])
    return plt.savefig('task4.png')
    
def task5():
    #Complete task 5 here
    with open(datafilepath, encoding="utf8") as f:
        data = json.load(f)

    club = dict()

    for filename in os.listdir(articlespath):
        with open(os.path.join(articlespath, filename), encoding="utf8") as f:
            text = f.read()
            for s in data['clubs']:
                if s['name'] not in club:
                    club[s['name']] = 0
                if len(re.findall(s['name'], text)) > 0:
                    club[s['name']] += 1

    x = [i['name'] for i in data['clubs']]
    y = list(club.values())
    df = pd.DataFrame({'club name': x, 'number of mentions': y})
    plt.bar(x, y)
    plt.title('Number of Club Names Mentioned')
    plt.xlabel('Club Name')
    plt.xticks(rotation=45)
    plt.ylabel('Number of Mentions')
    plt.savefig('task5.png')
    # plt.show()
    return df.to_csv('task5.csv', index=False, encoding="utf8")

def task6():
    #Complete task 6 here
    with open(datafilepath, encoding="utf8") as f:
        data = json.load(f)
    name = [i['name'] for i in data['clubs']]
    res = [[a, b] for a in name for b in name]

    club = dict()
    club2 = dict()
    for filename in os.listdir(articlespath):
        with open(os.path.join(articlespath, filename), encoding="utf8") as f:
            text = f.read()
            for s in res:
                idx = '-'.join(s)
                if idx not in club:
                    club[idx] = 0
                if len(re.findall(s[0], text)) > 0 and len(re.findall(s[1], text)) > 0:
                    club[idx] += 1
            for s in data['clubs']:
                if s['name'] not in club2:
                    club2[s['name']] = 0
                if len(re.findall(s['name'], text)) > 0:
                    club2[s['name']] += 1

    sim_score = []
    cnt = 0
    ans = []
    for s in res:
        idx = '-'.join(s)
        if club2[s[0]] + club2[s[1]] == 0:
            ans.append(0.0)
        else:
            ans.append((2 * club[idx])/(club2[s[0]] + club2[s[1]]))
        cnt += 1
        if cnt == 20:
            sim_score.append(ans)
            ans = []
            cnt = 0
    plt.imshow(sim_score, cmap='hot', interpolation='nearest')
    plt.xticks([i for i in range(0, 20)], labels=name, rotation=45)
    plt.yticks([i for i in range(0, 20)], labels=name)
    for i in range(20):
        for j in range(20):
            c = 'black' if round(sim_score[i][j], 1) >= 0.7 else 'w'
            plt.text(j, i, round(sim_score[i][j], 1), ha='center', va='center', color=c)
    plt.tight_layout
    # plt.show()
    return plt.savefig('task6.png')
    
def task7():
    #Complete task 7 here
    with open(datafilepath, encoding="utf8") as f:
        data = json.load(f)

    club = dict()
    name = [i['name'] for i in data['clubs']]
    for filename in os.listdir(articlespath):
        with open(os.path.join(articlespath, filename), encoding="utf8") as f:
            text = f.read()
            for s in data['clubs']:
                if s['name'] not in club:
                    club[s['name']] = 0
                if len(re.findall(s['name'], text)) > 0:
                    club[s['name']] += 1

    x = club.values()
    y = [i['goals_scored'] for i in data['clubs']]
    plt.scatter(x, y, c='maroon', s=100, alpha=0.5)
    plt.xlabel('Number of Mentions')
    plt.ylabel('Number of Goals Scored')
    plt.title('Comparing Information')
    # plt.show()
    return plt.savefig('task7.png')

    
def task8(filename):
    #Complete task 8 here
    with open(filename, encoding="utf8") as f:
        text = f.read()
        x = ' '.join(re.findall('[a-zA-Z]+', text)).lower()
        x_token = word_tokenize(x)
        ans = [word for word in x_token if not word in stopwords.words('english')]
        ans = [x for x in ans if len(x) > 1]
    return ans
