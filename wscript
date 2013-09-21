# -*- coding: utf-8 -*-

APPNAME = 'clitool'
VERSION = '0.3.2'

top = '.'
out = '_build'

import os
import sys


def configure(ctx):
    ctx.find_program('pip')
    ctx.find_program('pep8')
    if sys.version_info.major == 2:
        ctx.find_program('pyflakes')
    ctx.find_program('sphinx-build')
    ctx.find_program('py.test', var='PYTEST')


def build(bld):
    nodes = bld.path.ant_glob(['clitool/**/*.py'],
                    excl=['**/setup.py', '**/unicodecsv.py'])
    for node in nodes:
        bld(rule='${PEP8} --ignore=E126,E128 --show-source ${SRC}', source=node)
        if sys.version_info.major == 2:
            bld(rule='${PYFLAKES} ${SRC}', source=node)
    nodes = bld.path.ant_glob(['tests/**/*.py'])
    for node in nodes:
        bld(rule='${PEP8} --ignore=E126,E128,E501 --show-source ${SRC}', source=node)
        if sys.version_info.major == 2:
            bld(rule='${PYFLAKES} ${SRC}', source=node)
    tests = bld.path.ant_glob(['tests/*.py'])
    for t in tests:
        bld(rule='${PYTEST} --junitxml=${TGT} ${SRC}',
            source=t, target=t.get_bld().change_ext('.xml'))


def example(ctx):
    ctx.exec_command('python setup.py install')
    ctx.exec_command('python -m clitool.cli -o o.py')
    ctx.exec_command('python -m clitool.accesslog < data/access_log')
    ctx.exec_command("pip uninstall clitool")


def cleanbuild(ctx):
    from waflib import Options
    Options.commands = ['distclean', 'configure', 'build', 'example'] + Options.commands


def release(ctx):
    ctx.exec_command('python setup.py clean sdist upload')


def doc(ctx):
    ctx.exec_command('python setup.py install')
    wd = 'doc'
    cmd = ['make', 'html']
    ctx.exec_command(cmd, cwd=wd)
    ctx.exec_command("pip uninstall clitool")


def docclean(ctx):
    wd = 'doc'
    cmd = ['make', 'clean']
    ctx.exec_command(cmd, cwd=wd)


def dist(ctx):
    ctx.algo = 'zip'
    # to strip base directory, define arch_name.
    ctx.arch_name = '%s-%s.%s' % (APPNAME, VERSION, ctx.algo)
    ctx.base_name = '.'
    ctx.files = ctx.path.ant_glob(['doc/_build/html/**/*'])
    ctx.base_path = ctx.path.find_dir('doc/_build/html')


def apidoc(ctx):
    from waflib import Options
    Options.commands = ['docclean', 'doc', 'dist'] + Options.commands


# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
