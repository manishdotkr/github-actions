# GitHub Actions - Repo and PR Monitoring

This repository contains a collection of GitHub Actions workflows designed to monitor the repository and pull requests, performing various operations based on predefined conditions.

## Workflows

### 1. **DO_NOT_MERGE**

- **Functionality**: Closes the pull request if it has a "DO NOT MERGE" label.
- **Triggers**: Triggered when a pull request is opened, edited, reopened, or labeled.
- **Environment**:
  - `JOB`: DO_NOT_MERGE
  - `GITHUB_TOKEN`: ${{ secrets.GITHUB_TOKEN }}
  - `REPO_NAME`: ${{ github.repository }}
  - `PR_NUMBER`: ${{ github.event.pull_request.number }}
  - `WEBHOOK`: ${{ secrets.GOOGLE_CHAT_WEBHOOK }}

### 2. **TAG_CHECKER**

- **Functionality**: Checks if the version from the version file already exists as a tag.
- **Triggers**: Triggered when a pull request is opened, edited, or reopened.
- **Environment**:
  - `GITHUB_TOKEN`: ${{ secrets.GITHUB_TOKEN }}
  - `REPO_NAME`: ${{ github.repository }}
  - `PR_NUMBER`: ${{ github.event.pull_request.number }}
  - `WEBHOOK`: ${{ secrets.GOOGLE_CHAT_WEBHOOK }}

### 3. **PR_MONITOR**

- **Functionality**: Monitors stale pull requests and takes action.
- **Triggers**: Scheduled to run every day at 9:00 AM UTC.
- **Environment**:
  - `JOB`: PR_MONITOR
  - `GITHUB_TOKEN`: ${{ secrets.GITHUB_TOKEN }}
  - `REPO_NAME`: ${{ github.repository }}
  - `WEBHOOK`: ${{ secrets.GOOGLE_CHAT_WEBHOOK }}

### 4. **PR_CHECKER**

- **Functionality**: Checks the pull request description and target.
- **Triggers**: Triggered when a pull request is opened, edited, or reopened.
- **Environment**:
  - `JOB`: PR_CHECKER
  - `GITHUB_TOKEN`: ${{ secrets.GITHUB_TOKEN }}
  - `REPO_NAME`: ${{ github.repository }}
  - `PR_NUMBER`: ${{ github.event.pull_request.number }}
  - `WEBHOOK`: ${{ secrets.GOOGLE_CHAT_WEBHOOK }}

### 5. **MERGE_CLOSE**

- **Functionality**: Merges and closes the pull request using slash commands.
- **Triggers**: Triggered when an issue comment is made.
- **Environment**:
  - `JOB`: MERGE_CLOSE
  - `GITHUB_TOKEN`: ${{ secrets.GITHUB_TOKEN }}
  - `PR_NUMBER`: ${{ github.event.issue.number }}
  - `REPO_NAME`: ${{ github.repository }}
  - `MERGE_PR`: ${{ github.event.comment.body == '/Approved' }}
  - `CLOSE_PR`: ${{ github.event.comment.body == '/Close' }}
  - `WEBHOOK`: ${{ secrets.GOOGLE_CHAT_WEBHOOK }}

### 6. **GCHAT**

- **Functionality**: Checks if notifications are sent to Google Chat.
- **Triggers**: Triggered when a pull request is opened, edited, reopened, or closed, or when an issue comment is made.
- **Environment**:
  - `JOB`: GCHAT
  - `GITHUB_TOKEN`: ${{ secrets.GITHUB_TOKEN }}
  - `REPO_NAME`: ${{ github.repository }}
  - `PR_NUMBER`: ${{ github.event.pull_request.number }}
  - `EVENT`: ${{ github.event.action }}
  - `WEBHOOK`: ${{ secrets.GOOGLE_CHAT_WEBHOOK }}

## Usage

To use these workflows in your repository, simply copy the respective workflow files and modify them as needed. Ensure that you have appropriate permissions and secrets configured in your GitHub repository settings.

Feel free to contribute, report issues, or suggest improvements!

**Note:** Ensure that you have configured the necessary permissions and secrets in your GitHub repository settings for the workflows to function correctly.
