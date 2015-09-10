# A script to scrape /r/India

import time
import praw
from collections import deque
import traceback
import datetime
import pickle

DEBUG = False
DAY_IN_SECONDS = 60 * 60 * 24

class subStats(object):

        def __init__(self, user, passwd, subreddit, file):

                USER_AGENT = 'Script by /u/kashre001'
                self.reddit = praw.Reddit(user_agent=USER_AGENT)
                self.reddit.login(user, passwd, disable_warning=True)
                self.subreddit = self.reddit.get_subreddit(subreddit)
                self.file = file
                self.submissions = []
                self.authors = []
                self.comments = []
                self.offset = -(5.5 * 60 * 60)
                self.min_date = self.subreddit.created_utc - self.offset
                self.max_date = time.time() - self.offset          
                print ("Current time :" + str(self.max_date) + ' ' + self.easyTime(time.time() - self.offset))
                print ("Creation time :" + str(self.min_date)+ ' ' + self.easyTime(self.min_date))
                print ('Total existence time: ' + str(int((self.max_date - self.min_date)/DAY_IN_SECONDS/365)) + \
                ' years & ' + str((int(self.max_date - self.min_date)/DAY_IN_SECONDS)%365) + ' days\n')

        def easyTime(self,timestamp):
                time = datetime.datetime.utcfromtimestamp(timestamp)
                time = datetime.datetime.strftime(time, "%b %d %Y %H:%M:%S")
                return time
                

        def fetch_submissions(self, max_duration=5):

                if max_duration:
                    self.min_date = self.max_date - (DAY_IN_SECONDS * max_duration)

                Done = False

                upperTime = self.max_date 
                lowerTime = self.min_date 
                
                while not Done:
                        
                        try:
                                if DEBUG:
                                        print ('------------------------------------------------------\n')
                                        print (str(lowerTime) + '  ' + self.easyTime(lowerTime) + '\n')
                                        print (str(upperTime) + '  ' + self.easyTime(upperTime) + '\n')
                                        print ('\nreached')

                                query = 'timestamp:%d..%d' % (lowerTime, (upperTime + 8 * 60 * 60))
                                submissions = list(self.reddit.search(query, subreddit=self.subreddit, sort='new', limit=100, syntax='cloudsearch'))
                                						
                                for submission in submissions:                                                                               
                                        self.submissions.append(submission)
                                        if DEBUG:
                                                print(submission.author)
                                                print (str(submission.created_utc) + '  ' + self.easyTime(submission.created_utc) + '\n')
                                        if submission.created_utc > self.max_date:
                                                continue
                                        if submission.created_utc <= self.min_date:
                                                Done = True                                        
                                                break                                
                        
                                self.submissions.sort(key=lambda x: x.created_utc)
                                upperTime = self.submissions[0].created_utc - 0.001
                                
                                if DEBUG:
                                        print (self.easyTime(upperTime) + '\n')            

                                time.sleep(2);

                        except KeyboardInterrupt:
                                print ("\nExiting loop...\n")
                                break
                        except Exception as e:
                                print ('Going to sleep for 30 seconds...\n')
                                time.sleep(30)
                                self.submissions.sort(key=lambda x: x.created_utc)
                                upperTime = self.submissions[0].created_utc - 0.001
                                continue                        

                self.submissions.sort(key=lambda x: x.created_utc)
                print(len(self.submissions))
                pickle.dump(self.submissions, self.file, protocol=-1)
                return True
                
def main():

        outFile = open('submissions.p', 'wb')
        stats = subStats('kashre001','xxxx','india',outFile)
        
        if (stats.fetch_submissions(365)):
                print ('Success')
        else:
                print ('Faaaaaail')
        
        outFile.close()
        del outFile
                
#call main function
main()