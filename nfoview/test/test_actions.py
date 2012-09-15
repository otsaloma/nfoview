# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009 Osmo Salomaa
#
# This file is part of NFO Viewer.
#
# NFO Viewer is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# NFO Viewer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NFO Viewer. If not, see <http://www.gnu.org/licenses/>.

import nfoview


class _TestAction(nfoview.TestCase):

    def test_update_sensitivity__insensitive_view(self):
        window = nfoview.Window()
        for name in nfoview.actions.__all__:
            action = getattr(nfoview.actions, name)()
            action.update_sensitivity(window)

    def test_update_sensitivity__sensitive_view(self):
        window = nfoview.Window(self.new_nfo_file())
        for name in nfoview.actions.__all__:
            action = getattr(nfoview.actions, name)()
            action.update_sensitivity(window)


class TestCloseDocumentAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.CloseDocumentAction()


class TestCopyTextAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.CopyTextAction()


class TestEditPreferencesAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.EditPreferencesAction()


class TestOpenFileAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.OpenFileAction()


class TestQuitAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.QuitAction()


class TestSelectAllTextAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.SelectAllTextAction()


class TestShowAboutDialogAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.ShowAboutDialogAction()


class TestShowEditMenuAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.ShowEditMenuAction()


class TestShowFileMenuAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.ShowFileMenuAction()


class TestShowHelpMenuAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.ShowHelpMenuAction()


class TestWrapLinesAction(_TestAction):

    def setup_method(self, method):
        self.action = nfoview.actions.WrapLinesAction()
