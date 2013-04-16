import os
import datetime
import subprocess

import ckan
from ckan import plugins as p


class RepoInfo(p.SingletonPlugin):

    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    repo_info = {}

    def update_config(self, config):
        # add template directory
        p.toolkit.add_template_directory(config, 'templates')


        cwd = os.path.join(os.path.dirname(ckan.__file__), '..')
        self.repo_info = {
            'hash': '',
            'title': '',
            'url': '',
            'branch':'',
        }

        # Current commit
        try:
            git_show = subprocess.check_output(['git', 'show', '--oneline'], cwd=cwd)
            commit = git_show.split('\n')[0].split(' ')
            self.repo_info['hash'] = commit.pop(0)
            self.repo_info['title'] = ' '.join(commit)
            self.repo_info['url'] = config.get('ckanext.repo.base_commit_url',
                                     'https://github.com/okfn/ckan/commit/{0}').format(self.repo_info['hash'])
        except subprocess.CalledProcessError:
            pass

        # Current branch (requires Git 1.6.3 or higher)
        try:
            self.repo_info['branch'] = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=cwd).strip()
        except subprocess.CalledProcessError:
            pass

        # Last pulled
        try:
            date = subprocess.check_output(['stat', '-c', '%Y', '.git/FETCH_HEAD'], cwd=cwd)
            self.repo_info['last_updated'] = datetime.datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')
        except subprocess.CalledProcessError:
            pass

    def get_helpers(self):
        return {'get_repo_info': self.get_repo_info}

    def get_repo_info(self):
        return p.toolkit.render_snippet('repo_snippet.html', {'repo_info': self.repo_info})


