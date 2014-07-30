import os
import datetime
import subprocess
import logging

import ckan
from ckan import plugins as p

log = logging.getLogger(__name__)


class RepoInfo(p.SingletonPlugin):

    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IActions)

    # IConfigurer

    def update_config(self, config):
        # add template directory
        p.toolkit.add_template_directory(config, 'templates')

        self.repos_info = []

        repo_refs = config.get('ckanext.repo.repos', 'ckan')
        repo_refs = repo_refs.split(' ')

        for repo_ref in repo_refs:
            repo_info = _get_repo_info(repo_ref)
            if repo_info:
                self.repos_info.append(repo_info)

    # p.ITemplateHelpers

    def get_helpers(self):
        return {
            'get_repos_info': self._get_repos_info,
            'render_repos_info': self._render_repos_info,
        }

    # IActions

    def get_actions(self):
        @p.toolkit.side_effect_free
        @p.toolkit.auth_allow_anonymous_access
        def repos_info_show(context, data_dict):
            return self.repos_info

        return {
            'repos_info_show': repos_info_show,
        }

    def _get_repos_info(self):
        return self.repos_info


    def _render_repos_info(self):
        return p.toolkit.render_snippet('repo_snippet.html',
                                        {'repos_info': self.repos_info})


def _import_ckanext_module(name):
    try:
        return getattr(__import__('ckanext', fromlist=[name]), name)
    except ImportError:
        return None


def _import_module(name):
    try:
        return __import__(name)
    except ImportError:
        return None


def _get_repo_info(repo_ref):

    if '/' in repo_ref:
        parts = repo_ref.split('/')
        github_org = parts[0]
        repo_name = parts[1]
    else:
        github_org = 'ckan'
        repo_name = repo_ref

    if repo_name.startswith('ckanext-'):
        parts = repo_name.split('-')
        module = _import_ckanext_module(parts[1])
        cwd_dir = '../..'
    else:
        module = _import_module(repo_name)
        cwd_dir = '..'

    if not module:
        log.error('Could not load module for repo {0}'.format(repo_ref))
        return None

    cwd = os.path.join(os.path.dirname(module.__file__), cwd_dir)

    repo_info = {
        'name': repo_name,
        'hash': '',
        'title': '',
        'url': '',
        'branch': '',
    }

    # Current commit
    try:
        git_show = subprocess.check_output(
            ['git', 'show', '--oneline'], cwd=cwd)
        commit = git_show.split('\n')[0].split(' ')
        repo_info['hash'] = commit.pop(0)
        repo_info['title'] = ' '.join(commit)
        repo_info['url'] = 'https://github.com/{0}/{1}/commit/{2}'.format(
            github_org,
            repo_name,
            repo_info['hash'])
    except subprocess.CalledProcessError:
        pass

    # Current branch (requires Git 1.6.3 or higher)
    try:
        repo_info['branch'] = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=cwd).strip()
    except subprocess.CalledProcessError:
        pass

    # Last pulled
    try:
        date = subprocess.check_output(
            ['stat', '-c', '%Y', '.git/FETCH_HEAD'], cwd=cwd)

        repo_info['last_updated'] = datetime.datetime.fromtimestamp(
            int(date)).strftime('%Y-%m-%d %H:%M:%S')
    except subprocess.CalledProcessError:
        pass

    return repo_info
