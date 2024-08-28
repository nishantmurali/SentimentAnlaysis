import praw
import pandas as pd
import datetime

def fetch_comments(reddit, subreddit, keywords):
    data = []
    extractedIDs = []
    subreddit = reddit.subreddit(subreddit)


    for keyword in keywords:
        for submission in subreddit.search(query=keyword, sort='new', syntax='lucene', limit=None):
            submissionID = submission.id
            if submissionID in extractedIDs:
                print(f"Skipping submission (ID: {submissionID})")
                continue
            
            extractedIDs.append(submissionID)
            title = submission.title

            print(f"Found submission: {title} (ID: {submissionID})")

            submission.comments.replace_more(limit=None)  # Flatten comments (handle "more comments")
            for comment in submission.comments.list():
                data.append({
                    'Subreddit': 'r/cybertruck',
                    'SubmissionID': submissionID,
                    'Submission Created Time': datetime.datetime.fromtimestamp(submission.created_utc),
                    'Submission Title': submission.title,
                    'Submission Body': submission.selftext,
                    'Score': submission.score,
                    'URL': submission.url,
                    'Comment ID': comment.id,
                    'Comment Body': comment.body,
                    'Comment Score': comment.score,
                    'Comment Created Time': datetime.datetime.fromtimestamp(comment.created_utc)
                })
        
    df = pd.DataFrame(data)
    print(df.head())
    return df


def runScript():
    reddit = praw.Reddit(client_id="E79_ZBpaukgd_hG7ITs-Og",
                         client_secret="ubdZhNM6qctblRepzY_fXbRK4hX4dw",
                         user_agent='SentimentAnanlysis')
    
    keywords = ['CT', 'cybertruck', 'cyber', 'cyberbeast']

    start_date = datetime.timedelta(days=30)
    end_date = datetime.date.today()

    df = fetch_comments(reddit, 'cybertruck', keywords, start_date, end_date)
    df = fetch_comments(reddit, 'realtesla', keywords, start_date, end_date)
    df = fetch_comments(reddit, 'teslamotors', keywords, start_date, end_date)



    df.to_csv('reddit_comments.csv', index = False)

runScript()