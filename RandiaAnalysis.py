# Analysis of scraped file

import time
import praw
import datetime
import pickle
import requests
import json
import pprint
from wordcloud import WordCloud, STOPWORDS

WIDTH = 1280
HEIGHT = 720
NUM_OF_WORDS = 250

def sentiAnalysis(isUrl, dataToAnalyse):

    """
    Function which does sentimental analysis of URL or Text
    """

    print ('Entering...\n')
    header={"X-Mashape-Key": "euAnPjoRGMmshFM35j8LaStTkTLwp1cvGc9jsnfgvjFO2KRD7h", "Accept": "application/json"}

    if(isUrl):        
        postURL = 'https://loudelement-free-natural-language-processing-service.p.mashape.com/nlp-url/?url='        
        url_params = postURL + dataToAnalyse
        #print (url_params)        

    if not(isUrl):
        postURL = 'https://loudelement-free-natural-language-processing-service.p.mashape.com/nlp-text/?text='
        url_params = postURL + dataToAnalyse
        #print (url_params)

    try :
    
        response = requests.get(url_params, headers=header)
        tempDict = response.json()
        #print (str(tempDict['sentiment-text']) + ' ' + str(tempDict['sentiment-score']) + '\n' + str(tempDict['extracted-content']) + '\n')
        print ('Leaving...' + '\n')
        return (str(tempDict['sentiment-text']) + ',' + str(tempDict['sentiment-score']))

    except Exception as e:
        print ('Error in sentimental analysis...\n')
        print ('Exception: ' + str(e) + '\n' + 'Leaving..' + '\n')
        return ''
    
def easyTime(timestamp):
    time = datetime.datetime.utcfromtimestamp(timestamp)
    time = datetime.datetime.strftime(time, "%b %d %Y %H:%M:%S")
    return time

def processSubmissions(content, outFile):
    """

    Function to process submissions and write necessary stuff onto a .csv file
    
    """
    submissions = reversed(content)        

    for submission in submissions:

        try:

            # Pre-processing of text
            sub_url = str(submission.url)
            sub_url = sub_url.replace("\n", "")
            sub_url = sub_url.replace(",", "")

            sub_title = str(submission.title)
            sub_title = sub_title.replace("\n", "")
            sub_title = sub_title.replace(",", ";")

            #sub_sentiAnalysis = sentiAnalysis(False, sub_title)

            # All writes
            """
            outFile.write(str(submission.author) + ',')                
            outFile.write(str(submission.num_comments) + ',')
            outFile.write(str(submission.score) + ',')                
            outFile.write(str(submission.num_reports) + ',')
            outFile.write(str(easyTime(submission.created_utc)) + ',')                
            outFile.write(str(submission.is_self) + ',')
            outFile.write(str(submission.over_18) + ',')
            outFile.write(str(submission.gilded) + ',')                                
            outFile.write(str(submission.link_flair_text) + ',')
            outFile.write(sub_url + ',')
            outFile.write(str(submission.fullname) + ',')
            outFile.write(str(submission.permalink) + ',')
            outFile.write(str(sub_title) + ',')
            outFile.write(str(sub_sentiAnalysis) + '\n')
            """
            outFile.write(str(submission.ups) + ',')
            outFile.write(str(submission.downs) + '\n')
            

        except Exception as e:
            print ('Something wrong with Reddit\n')
            print ('Sleeping for 30 seconds . . .\n')
            time.sleep(30)

    return True;

def getSubmissionTextAsSingleString(content):
    """    
    Get all submission titles as a single string    
    """

    items = reversed(content)
    text = ''

    for item in items:
        #print (item.link_flair_text)
        if item.is_self is not True:
            #print (str(item.author) + ' ' + item.permalink)
            text += item.title
            text += ' '

    return text

def makeCloud(text, imgFile, words):
    """
    Makes a word cloud and stores it in a jpeg file
    """
    excludewords = STOPWORDS.copy()
    
    for word in words:
        excludewords.add(word)
    
    wordcloud = WordCloud(max_words=NUM_OF_WORDS, width=WIDTH, height=HEIGHT, stopwords=excludewords).generate(text)
    image = wordcloud.to_image()
    image.show()
    image.save(imgFile + '.jpeg')      

def writeFreq(text, outFile, words):
    """
    Writes frequencies of words into the specified file
    """

    excludewords = STOPWORDS.copy()
    
    for word in words:
        excludewords.add(word)
    
    wordcloud = WordCloud(max_words=NUM_OF_WORDS, stopwords=excludewords)
    freqList  = wordcloud.process_text(text)

    for item in freqList:
        outFile.write(item[0] + ',' + str(item[1]) + '\n')


def fetchAndProcessComments(content, outFile):
    """

    Function to process comments from a submission and write necessary stuff onto a .csv file
    
    """
    submissions = reversed(content)        
    r = praw.Reddit('/r/india scraping by /u/kashre001')
    #sub_sentiAnalysis = sentiAnalysis(False, sub_title)
    
    for submission in submissions:

        if (int(submission.created_utc) > 1418545890):
            continue

        # Pre-processing of text
        sub_url = str(submission.url)
        sub_url = sub_url.replace("\n", "")
        sub_url = sub_url.replace(",", "")
        sub_title = str(submission.title)
        sub_title = sub_title.replace("\n", "")
        sub_title = sub_title.replace(",", ";")

        # Get all comments for this submission
        Done = True
        while Done:

            try: 
                new_submission = r.get_submission(submission_id = submission.id)
                new_submission.replace_more_comments(limit=None, threshold=0)
                all_flat_comments = praw.helpers.flatten_tree(new_submission.comments)
                break

            except Exception as e:
                print ('Something went wrong...\n Sleeping for 60 seconds...\n')
                time.sleep(60)
                

        for comment in all_flat_comments:
            

            # Pre-processing of comment body
            comment_body = str(comment.body)
            comment_body = comment_body.replace("\n", "")
            comment_body = comment_body.replace(",", ";")

            comment_permalink = str(submission.permalink[:-17]) + str(comment.id)

            # All writes
            outFile.write(str(comment.author) + ',')
            outFile.write(str(easyTime(comment.created_utc)) + ',')
            outFile.write(str(comment.score) + ',')
            outFile.write(str(comment.controversiality) + ',')
            outFile.write(str(comment.gilded) + ',')
            outFile.write(str(comment.id) + ',')
            outFile.write(comment_permalink + ',')
            outFile.write(str(comment.parent_id) + ',')
            outFile.write(str(comment.distinguished) + ',')
            outFile.write(str(comment_body) + ',')
            outFile.write(',')
            outFile.write(str(submission.author) + ',')                
            outFile.write(str(submission.num_comments) + ',')
            outFile.write(str(submission.score) + ',')                
            outFile.write(str(submission.num_reports) + ',')
            outFile.write(str(easyTime(submission.created_utc)) + ',')                
            outFile.write(str(submission.is_self) + ',')
            outFile.write(str(submission.over_18) + ',')
            outFile.write(str(submission.gilded) + ',')                                
            outFile.write(str(submission.link_flair_text) + ',')
            outFile.write(str(submission.domain) + ',')
            outFile.write(str(submission.fullname) + ',')
            outFile.write(str(submission.permalink) + ',')
            outFile.write(str(sub_title) + '\n')
            
    return True
    
        

def main():

    inFile   = open('submissions.p','rb')    
    #outFile  = open('RandiaxRand.csv','w',encoding='utf-8')
    #freqFile = open('RandiaFreq.csv','w',encoding='utf-8')
    txtFile  = open('RandiaComments5.csv','w',encoding='utf-8')
    imgFile  = 'randialinkcloud'    
    words_to_be_excluded = ['p','np','r','s','thread','say','will','need','india\'','t','u','modi\'','k','e','go',\
                            'see','x','still','vs','says','may','.']
    content = pickle.load(inFile)
    print (len(content))
    
    #processSubmissions(content, outFile)
    #text = getSubmissionTextAsSingleString(content)
    #makeCloud(text, imgFile, words_to_be_excluded)
    #writeFreq(text, freqFile, words_to_be_excluded)
    if(fetchAndProcessComments(content, txtFile)):
        print ("SUCESS BRO")
    print ('Total no. of submissions: ' + str(len(content)))

    outFile.close()
    inFile.close()

# Call Main
main()
