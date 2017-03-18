import requests
import json
import operator

def get_max_forks_count_repos():
    try:
        url_org_repos_format = "https://api.github.com/orgs/{}/repos"

        url_org_repos = url_org_repos_format.format(raw_input("Give the organization name: "))
        no_repos = int(raw_input("Enter max no of repos: "))

        org_repos_src_json = requests.get(url_org_repos)
        org_repos_list =  org_repos_src_json.json()

        max_forks_count_repos = sorted(org_repos_list, key = lambda k: k['forks_count'], reverse=True)[:no_repos]
        # print max_forks_count_repos

        with open('data.txt', 'w') as outfile:
            print 'Writing to file'
            json.dump(max_forks_count_repos, outfile)

        return max_forks_count_repos
    except Exception, e:
        print e
        return None

def get_max_repo_committer(url, no_commiters):
    try:
        repo_commits_src = requests.get(url) 
        repo_commmits = repo_commits_src.json()
        name_commit_map = {}
        # print repo_commmits
        for commit in repo_commmits:
            committer_name = commit['commit']['author']['name']
            # print committer_name
            if committer_name not in name_commit_map:
                name_commit_map[committer_name] = 1
            else:
                name_commit_map[committer_name] += 1
        name_commit_map = sorted(name_commit_map.items(), key=operator.itemgetter(1), reverse=True)[:no_commiters]
        return name_commit_map
    except Exception, e:
        print e
        return None

def main():
    try:
        max_forks_count_repos = get_max_forks_count_repos()
        if max_forks_count_repos is None:
            return
        no_commiters = int(raw_input("Enter no of commiters"))
        for repo in max_forks_count_repos:
            commits_url_format = repo['commits_url']
            commits_url = commits_url_format.replace('{/sha}', '')
            print repo["full_name"]
            print get_max_repo_committer(commits_url, no_commiters)
    except Exception, e:
        print e

if __name__ == '__main__':
    main()

