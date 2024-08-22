import praw
import pandas as pd

def fetch_comments(subreddit, keywords):
    data = []
    extractedIDs = []

    for keyword in keywords:
        for submission in subreddit.search(query=keyword, sort='new', syntax='lucene', limit=10):
            submissionID = submission.id
            if submissionID in extractedIDs:
                print(f"Skipping submission (ID: {submissionID})")
                continue
            
            extractedIDs.append(submissionID)
            submissionCreatedTime = submission.created_utc
            title = submission.title

            print(f"Found submission: {title} (ID: {submissionID})")

            submission.comments.replace_more(limit=10)  # Flatten comments (handle "more comments")
            for comment in submission.comments.list():
                data.append({
                    'SubmissionID': submissionID,
                    'SubmissionCreatedTime': submission.created_utc,
                    'Title': submission.title,
                    'Selftext': submission.selftext,
                    'Score': submission.score,
                    'URL': submission.url,
                    'CommentID': comment.id,
                    'CommentBody': comment.body,
                    'CommentScore': comment.score,
                    'CommentCreatedTime': comment.created_utc
                })
        
    df = pd.DataFrame(data)
    print(df.head())
    return df


def runScript():
    reddit = praw.Reddit(client_id="E79_ZBpaukgd_hG7ITs-Og",
                         client_secret="ubdZhNM6qctblRepzY_fXbRK4hX4dw",
                         user_agent='SentimentAnanlysis')
    
    keywords = ['CT', 'cybertruck', 'cyber', 'cyberbeast']

    subreddit = reddit.subreddit("cybertruck")

    df = fetch_comments(subreddit, keywords)

    df.to_csv('reddit_comments.csv', index = False)

runScript()