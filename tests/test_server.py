# -*- coding: utf-8 -*-
"""Test for tmuxp Server object."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import logging

from tmuxp import Server
from .helpers import TmuxTestCase

logger = logging.getLogger(__name__)


class ServerTest(TmuxTestCase):

    def test_has_session(self):
        assert self.t.has_session(self.TEST_SESSION_NAME)
        assert not self.t.has_session('asdf2314324321')

    def test_socket_name(self):
        """ ``-L`` socket_name.

        ``-L`` socket_name  file name of socket. which will be stored in
               env TMUX_TMPDIR or /tmp if unset.)

        """
        myserver = Server(socket_name='test')

        assert myserver.socket_name == 'test'

    def test_socket_path(self):
        """ ``-S`` socket_path  (alternative path for server socket). """
        myserver = Server(socket_path='test')

        assert myserver.socket_path == 'test'

    def test_config(self):
        """ ``-f`` file for tmux(1) configuration. """
        myserver = Server(config_file='test')
        assert myserver.config_file == 'test'

    def test_256_colors(self):
        myserver = Server(colors=256)
        assert myserver.colors == 256

        proc = myserver.cmd('list-servers')

        assert '-2' in proc.cmd
        assert '-8' not in proc.cmd

    def test_88_colors(self):
        myserver = Server(colors=88)
        assert myserver.colors == 88

        proc = myserver.cmd('list-servers')

        assert '-8' in proc.cmd
        assert '-2' not in proc.cmd


class EnvironmentTest(TmuxTestCase):

    def test_show_environment(self):
        """Server.show_environment() returns dict."""
        vars = self.server.show_environment()
        assert isinstance(vars, dict)

    def test_set_show_environment_single(self):
        """Set environment then Server.show_environment(key)."""
        self.server.set_environment('FOO', 'BAR')
        assert 'BAR' == self.server.show_environment('FOO')

        self.server.set_environment('FOO', 'DAR')
        assert 'DAR' == self.server.show_environment('FOO')

        assert 'DAR' == self.server.show_environment()['FOO']

    def test_show_environment_not_set(self):
        """Unset environment variable returns None."""
        assert self.server.show_environment('BAR') is None
