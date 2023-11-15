import os
from github import Github
from datetime import datetime, timedelta
import yaml
import requests

def load_config(config_file):
    try:
        with open(config_file, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"msg file '{config_file}' not found.") 
#loading msgs
msg = load_config('msg.yaml')

# env variables
job = os.getenv("JOB") if(os.getenv("JOB")) else None
# if not job:
#     raise ValueError(f"JOB name must be provided")
githubToken = os.getenv("GITHUB_TOKEN") if(os.getenv("GITHUB_TOKEN")) else None
repoName = os.getenv('REPO_NAME') if(os.getenv('REPO_NAME')) else None
prNumber = int(os.getenv('PR_NUMBER')) if ( os.getenv('PR_NUMBER') ) else None

#making checks for essential variables
# assert githubToken or repoName or job, "Must Provide All Three github_token ,repo_name and job_name for this workflow"
assert githubToken , "Must Provide github_token for this workflow"
assert repoName    , "Must Provide repo_name for this workflow"
assert job,          "Must Provide job_name for this workflow"
#initiating github
g = Github(githubToken)
repo = g.get_repo(repoName)
pr = repo.get_pull(prNumber) if(prNumber) else None 

def main():
    # running jobs
    if not pr and job in ['PR_CHECKER' , 'FILE_CHECKER' , 'TAG_MATCHER' , 'MERGE_CLOSE' , 'DO_NOT_MERGE' ]:
        raise ValueError("Please provide a Valid PR Number")
    
    if job == "PR_MONITOR":
        pr_monitor()
    elif job == "PR_CHECKER":
        pr_checker()
    elif job == "FILE_CHECKER": # TAG_CHECKER
        file_checker()
    elif job == "TAG_MATCHER":  # TAG_CHECKER
        tag_matcher()
    elif job == "MERGE_CLOSE":
        merge_close_pr()
    elif job == "DO_NOT_MERGE":
        do_not_merge()
    elif job == "GCHAT":
        gChat_notification(os.getenv('EVENT'))
    else:
        raise ValueError("Please provide Valid JOB Name")
    

def pr_monitor():
    # Makring all the PRs on the repo as stale if they are not active for the last 15 days.
    print("---------------running pr_monitor---------------")
    #local variables
    now = datetime.now()
    stale_days = 15;
    stale_close_days = 2;
    allPullRequests = repo.get_pulls(state='open')

    for pr in allPullRequests:
        time_diff = now - pr.updated_at
        # 1. Check if the time difference is greater than the stale_days
        if time_diff > timedelta(days=stale_days):
            print(f"Marking Pull request: {pr.number} as stale!")
            pr.create_issue_comment( msg.get("stale_label") )
            pr.add_to_labels('Stale')

        # 2. Close staled PR if 2 days of no activity and if it has the label 'Stale'
        if "Stale" in [label.name for label in pr.labels] and time_diff > timedelta(days=stale_close_days):
            # check if the time difference is greater than the stale_close_days
            print(f"Pull request: {pr.number} is stale and closed!")
            print(msg.get("staled_PR_closing"))
            pr.edit(state="closed")
            pr.create_issue_comment(msg.get("staled_PR_closing") )  
            gChat_notification("closed")
   
def file_checker():
    # Check All the files and see if there is a file named "VERSION"
    print("---------------running file_checker---------------")
    fileName = os.getenv("VERSION_FILE")
    assert fileName , "Must Provide a File Name for running the file_checker job"
    files = pr.get_files()
    version_file_exist = False
    for file in files:
        if file.filename == 'VERSION':
            print(f"file : {file}")
            version_file_exist = True
            break
    if version_file_exist:
        print(msg.get("check_version_file") )
    else:
        print(msg.get("version_file_inexistence"))
        pr.edit(state='closed')
        pr.create_issue_comment(msg.get("version_file_inexistence") )
        gChat_notification("closed")

def tag_matcher():
    # Check if version name from "VERSION" already exists as tag  
    print("---------------running version_checker---------------")

    versionFile = os.getenv("VERSION_FILE")
    assert versionFile , "Must Provide a tag from version file for running the version_checker job"
    
    print(f"version from VERSION_FILE : {versionFile}")
    tags = repo.get_tags()
    tag_exist = False
    if versionFile in [tag.name for tag in tags]:
        tag_exist = True

    if not tag_exist:
        print(msg.get("tagcheck_success") )
    else:
        print(msg.get("tagcheck_reject") )
        pr.edit(state='closed')
        pr.create_issue_comment(msg.get("tagcheck_reject") )
        gChat_notification("closed")

def pr_checker():
    # Check if the pull request targets the master branch directly and not comming from release branch
    if pr.base.ref == 'master' and not pr.head.ref.startswith('release/'):
        print(f"Pull request: {pr.number} was targeted to master")
        print(msg.get("check_PR_target"))
        pr.edit(state='closed')
        pr.create_issue_comment(msg.get("check_PR_target") )
        gChat_notification("closed")
    # Check if the pull request has a description
    if not pr.body:
        print(f"Pull request: {pr.number} has no description" )
        print(msg.get("check_description"))
        pr.edit(state='closed')
        pr.create_issue_comment(msg.get("check_description"))
        gChat_notification("closed")
        
def merge_close_pr():
    merge = os.getenv("MERGE_PR")
    close = os.getenv("CLOSE_PR")
    assert merge in ['true' , 'false'] , f"Please provide correct value for merge, given value is: {merge}"
    assert close in ['true' , 'false'] , f"Please provide correct value for close, given value is: {close}"

    # Check if the comment "/Approved" in the pull request comments
    if merge.__eq__('true'):
        pr.merge(merge_method = 'merge', commit_message = msg.get("approve_merge"))
        pr.create_issue_comment(msg.get("approve_comment"))
        print(msg.get("approve_comment"))

    # Check if the comment "/Close" in the pull request comments
    if close.__eq__('true'):    
        print(msg.get("closing_comment"))
        pr.edit(state="closed")
        pr.create_issue_comment(msg.get("closing_comment"))
        gChat_notification("closed")

def do_not_merge():
    labels = pr.get_labels()
    if "DO NOT MERGE" in [label.name for label in labels]:
        print(msg.get("label"))    
        pr.edit(state='closed')
        pr.create_issue_comment(msg.get("label"))
        gChat_notification("closed")

def gChat_notification(event):
    # Google chat integration with github
    event = event if event else 
    gChatWebhookUrl = os.getenv('WEBHOOK')
    assert event , "Please provide a valid event"
    assert gChatWebhookUrl , "Please provide a valid google chat webhook URL"
    
    message = f"An Event is created on PR:\nTitle: {pr.title}\nURL: {pr.html_url}"
    msgDictionery = {
        "opened"   : f"New Pull Request Created by {pr.user.login}:\nTitle: {pr.title}\nURL: {pr.html_url}",
        "edited"   : f"Pull Request Edited by {pr.user.login}:\nTitle: {pr.title}\nURL: {pr.html_url}",
        "closed"   : f"Pull Request Closed by {pr.user.login}:\nTitle: {pr.title}\nURL: {pr.html_url}",
        "reopened" : f"Pull Request Reopened by {pr.user.login}:\nTitle: {pr.title}\nURL: {pr.html_url}"
    }
    message = msgDictionery.get(event , message)
    payload = {
        "text" : message
    }
    response = requests.post(gChatWebhookUrl, json=payload)
    print(response)
    print(event)

