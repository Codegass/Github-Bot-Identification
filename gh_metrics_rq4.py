from github import Github
import datetime
import time
import pytz
import pandas as pd
import re

# we have a list of all the bots that are in the PRs
confirmed_bots = [
    "VSCodeTriageBot",
    "dependabot",
    "github-actions[bot]",
    "check-spelling-bot",
    "azure-pipelines[bot]",
    "microsoft-github-policy-service[bot]",
    "typescript-bot",
    "github-pages[bot]",
    "kodiakhq[bot]",
    "renovate[bot]",
    "bors[bot]",
    "microsoft-cla-retired[bot]",
    "msftbot[bot]",
    "facebook-github-bot",
    "review-notebook-app[bot]",
    "codecov-commenter",
    "codesandbox-ci[bot]",
    "msft-fluent-ui-bot",
    "fabricteam",
    "size-auditor[bot]",
    "github-code-scanning[bot]",
    "github-merge-queue[bot]",
    "pull[bot]",
    "PylanceBot",
    "coveralls",
    "llvmbot",
    "wingetbot",
    "apecloud-bot",
    "dotnet-winget-bot",
    "Rust-Winget-Bot",
    "dotnet-maestro[bot]",
    "msfluid-bot",
    "CBL-Mariner-Bot",
    "reunion-maestro[bot]",
    "pull-bot",
    "analysis-bot",
    "AppVeyorBot",
    "sonarcloud[bot]",
    "codecov[bot]",
    "BrewTestBot",
    "acrolinxatmsft1",
    "changeset-bot[bot]",
    "msftclas",
    "playwrightmachine",
    "PrismAutomata",
    "Megalinter",
    "FluentService",
    "MetalMonkey-GSD",
    "csigs"
]

""" K-V pairs of repo_name - GH Repostory Object """
memo = {  }

if __name__ == '__main__':
    # get all the raw data into a DataFrame
    df = pd.read_csv('/Users/rehmanh/Desktop/Research/Chenhao Bot Study/collected_data_one_year_microsoft_May1st-3_fixed.csv', index_col=False)

    # sort by Repo Name and PR number; should be 35,070 unique Pulls
    prs = df.groupby(['repo_name', 'pull_number'], as_index=False).first()
    prs = pd.DataFrame(prs)

    # initialize result Dataframe
    result = pd.DataFrame(columns=['Repo Name', 'Pull Number', 'Bot Present?', 'Created At', 'Initial Activity At', 
                                   'Merged At', 'Turnaround Time', 'Merge Time', 'Idle Time', 'Churn', 
                                   'Comment Count', 'Developer Quantity'])

    # init Github with Token
    gh = Github('')

    # define UTC timezone
    timezone = pytz.timezone("Etc/Greenwich")

    for index, row in prs.iterrows():
        if index == 50:
            break

        if gh.rate_limiting[0] < 5:
            print("SLEEPING TO AVOID RATE LIMIT")
            time.sleep(3600)

        repo_name = row['repo_name']
        pull_number = row['pull_number']
        bot_present = False

        print('{}: {}/{}'.format(index, repo_name, pull_number))

        # get subset of results from original dataset that match given repo and pull number
        sample = df.query("repo_name == @repo_name & pull_number == @pull_number", inplace=False)
        sample = pd.DataFrame(sample)
        
        # get initial activity time
        sample = sample.sort_values(by=['event_time'])
        initial_activity_at = sample.iloc[0]['event_time']
        initial_activity_at = datetime.datetime.strptime(initial_activity_at, "%Y-%m-%d %H:%M:%S")
        initial_activity_at = timezone.localize(initial_activity_at)

        """ calculate idle time (average of time difference) """
        # first get all time stamps in PR activities
        times = [datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S") for t in sample['event_time'].tolist()]
        idle_time = 0
        if len(times) > 1:
            # then get the time differences between activities
            time_differences = [times[i + 1] - times[i] for i in range(len(times) - 1)]
            # then calculate the average idle time
            idle_time = sum(time_differences, datetime.timedelta(0)) / len(time_differences)
            idle_time = str(idle_time)

        # want to check if the users of the PR contains a bot from the list
        users = sample['user'].tolist()
        developer_quantity = len(users)

        for u in users:
            if u.startswith("NamedUser"):
                user = re.findall('"([^"]*)"', u)
                u = user[0]

            if u in confirmed_bots:
                bot_present = True
                developer_quantity -= 1

        try:
            # interface with Github and collect the relevant metrics
            if repo_name not in memo:
                repo = gh.get_repo(repo_name)
                memo[repo_name] = repo
            else:
                repo = memo[repo_name]

            pr = repo.get_pull(pull_number)
            created_at = timezone.localize(pr.created_at)
            turnaround_time = initial_activity_at - created_at
            merged_at = 0
            merge_time = 0

            # if the pull request was merged, calculate the merge time
            if pr.merged:
                merged_at = timezone.localize(pr.merged_at)
                merge_time = merged_at - created_at

            churn = pr.raw_data.get('additions') - pr.raw_data.get('deletions')
            comment_count = pr.raw_data.get('comments')
                
            new_row = {'Repo Name': repo_name, 'Pull Number': pull_number, 'Bot Present?': bot_present, 
                    'Created At': created_at, 'Initial Activity At': initial_activity_at, 'Merged At': merged_at, 
                    'Turnaround Time': turnaround_time, 'Merge Time': merge_time, 'Idle Time': idle_time, 
                    'Churn': churn, 'Comment Count': comment_count, 'Developer Quantity': developer_quantity}
            result.loc[len(result)] = new_row
        except Exception as ex:
            print('There was an error at index {} for repo {} and pull number'.format(index, repo_name, pull_number))
            print(ex)

    result.to_csv('/Users/rehmanh/Desktop/Research/Chenhao Bot Study/TEST_RQ4.csv', index=False)   