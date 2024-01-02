#!/bin/bash

id=$(gh pr view $1 --json id -q '.id')

MUTATION='
  mutation($id: ID!) {
    convertPullRequestToDraft(input: { pullRequestId: $id }) {
      pullRequest {
        id
        number
        isDraft
      }
    }
  }
'
gh api graphql -F id="${id}" -f query="${MUTATION}" >/dev/null

printf "\033[32m✓\033[0m Pull request #$1 is marked as \"draft\"\n"