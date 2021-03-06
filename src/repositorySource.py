#!/usr/bin/env python
# https://github.com/PyGithub/PyGithub
from helper import log,getConfig,giteaCreateUserOrOrg,giteaSetRepoTopics,giteaSession,giteaCreateRepo,ghApi,giteaCreateOrg,giteaGetUser,config

def repositorySource():
    config = getConfig()
    repo_map = config['repomap']
    session = giteaSession()
    gh = ghApi()

    for repo in gh.get_user().get_repos():
        if not repo.fork:
            real_repo = repo.full_name.split('/')[1]
            gitea_dest_user = repo.owner.login
            repo_owner=repo.owner.login

            log('Source Repository : {0}'.format(repo.full_name))

            if real_repo in repo_map:
                gitea_dest_user = repo_map[real_repo]

            gitea_uid = giteaGetUser(gitea_dest_user)

            if gitea_uid == 'failed':
                gitea_uid = giteaCreateUserOrOrg(gitea_dest_user,repo.owner.type)

            repo_name = "{0}".format(real_repo)

            m = {
                "repo_name"         : repo_name,
                "description"       : (repo.description or "not really known")[:255],
                "clone_addr"        : repo.clone_url,
                "mirror"            : True,
                "private"           : repo.private,
                "uid"               : gitea_uid,
            }

        status = giteaCreateRepo(m,repo.private)
        if status != 'failed':
            topics = repo.get_topics()
            giteaSetRepoTopics(repo_owner,repo_name,topics)
        else:
            log(repo)

        log(False)