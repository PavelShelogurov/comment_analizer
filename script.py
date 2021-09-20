import matplotlib.pyplot as plt
import subprocess as sub
import json
import requests

'''
    Скрипт ищет комментарии к видео. В итоге подсчитывает их количство 

    https://developers.google.com/youtube/v3/docs/comments дока по ютубу
'''

TEXT_FORMAT = 'html' #или plainText
MAX_RESULTS = 100
API_KEY = '' #Добавить сюда API_KEY для youtube API
VIDEO_ID =  '' #Добавить адрес видео
PAGE_TOKEN = ''
TOTAL_COMMENTS = 0

def checkReplyComment(jsonFile):
    total_comments = 0
    contReplyComment = jsonFile["snippet"]["totalReplyCount"]
    if(contReplyComment > 0):
        commentId = jsonFile["snippet"]["topLevelComment"]["id"]
        pageToken = ''
        isContunue = True
        number = 1
        while (isContunue):
            REQUEST_REPLY_COMMENTS = f'https://www.googleapis.com/youtube/v3/comments?key={API_KEY}&part=snippet&maxResults={MAX_RESULTS}&parentId={commentId}&pageToken={pageToken}'
            resp = requests.get(REQUEST_REPLY_COMMENTS)
            jsonReplyCommentFile = json.loads(resp.text)
            items_json = jsonReplyCommentFile["items"]
            for item in items_json:
                author = item["snippet"]["authorDisplayName"]
                text = item["snippet"]["textOriginal"]
                #вот тут происходит запись комментариев заменить эту строчку на то, что небоходимо делать
                print(f'---{number}| {author} : {text}')
                number+=1
                total_comments += 1
            try:
                pageToken = jsonReplyCommentFile["nextPageToken"]
            except KeyError:
                #следующей страницы с комментариями нет
                isContunue = False
    return total_comments            
        

hasNextPage = True

number = 0
#файл для записи оментариев
file_comments = open('comments.txt', 'w')
while (hasNextPage):
    REQUEST_URL = f'https://www.googleapis.com/youtube/v3/commentThreads?key={API_KEY}&videoId={VIDEO_ID}&textFormat={TEXT_FORMAT}&maxResults={MAX_RESULTS}&part=snippet&pageToken&pageToken={PAGE_TOKEN}'

    resp = requests.get(REQUEST_URL)
    jsonFile = json.loads(resp.text)
    countOfComments = jsonFile["pageInfo"]["totalResults"]
    try:
        #если существуют ещё коментарии присылается токен, используемы для запроса слудующих комментарив
        PAGE_TOKEN = jsonFile["nextPageToken"]
    except KeyError:
        #если их не сущуствует, обулям данные
        PAGE_TOKEN = ''
        hasNextPage = False
        print('Следующая страница с комментариями не найдена')
    for i in range(0, countOfComments):
        author = jsonFile["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        text = jsonFile["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        #file_comments.write(f'{author} : {text}')
        TOTAL_COMMENTS += 1 
        number += 1
        print(f'{number}| {author} : {text}')
        TOTAL_COMMENTS += checkReplyComment(jsonFile["items"][i])
        #если коментарий имеет вложенные комментарии (ответы)
        

file_comments.close()
print('Операция получения комментариев законцена')
print('Total comments:', TOTAL_COMMENTS)




'''
jsonObj = json.load(resp.content)

#вывод коментариев в очередном json файле
for i in range(0 , 20):
    print(jsonObj["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"][i]["commentThreadRenderer"]["comment"]["commentRenderer"]["contentText"]["runs"][0]["text"])
#print(jsonObj["a"])


'''


'''

data = {'banana' : 3, 'apple' : 10, 'juce' : 12}

#вывод полученного результата в вите графика
key = list(data.keys())
value = list(data.values())

fig, ax = plt.subplots()
ax.bar(key, value)
fig.suptitle('Categorical Plotting')
fig.show()
print('Нажмите любую клавишу для завершения')
input()

'''