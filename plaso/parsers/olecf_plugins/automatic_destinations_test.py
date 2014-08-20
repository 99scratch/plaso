#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 The Plaso Project Authors.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the .automaticDestinations-ms OLECF file plugin."""

import unittest

# pylint: disable=unused-import
from plaso.formatters import olecf as olecf_formatter
from plaso.lib import eventdata
from plaso.lib import timelib_test
from plaso.parsers.olecf_plugins import automatic_destinations
from plaso.parsers.olecf_plugins import interface
from plaso.parsers.olecf_plugins import test_lib


class TestAutomaticDestinationsOlecfPlugin(test_lib.OleCfPluginTestCase):
  """Tests for the .automaticDestinations-ms OLECF file plugin."""

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    self._plugin = automatic_destinations.AutomaticDestinationsOlecfPlugin()

  def testProcess(self):
    """Tests the Process function."""
    test_file = self._GetTestFilePath([
       u'1b4dd67f29cb1962.automaticDestinations-ms'])
    event_queue_consumer = self._ParseOleCfFileWithPlugin(
        test_file, self._plugin)
    event_objects = self._GetEventObjectsFromQueue(event_queue_consumer)

    self.assertEquals(len(event_objects), 44) 

    # Check a AutomaticDestinationsDestListEntryEvent.
    event_object = event_objects[3]

    self.assertEquals(event_object.offset, 32)

    self.assertEquals(
        event_object.timestamp_desc, eventdata.EventTimestamp.MODIFICATION_TIME)

    expected_timestamp = timelib_test.CopyStringToTimestamp(
        '2012-04-01 13:52:38.997538')
    self.assertEquals(event_object.timestamp, expected_timestamp)

    expected_msg = (
        u'Entry: 11 '
        u'Pin status: Unpinned '
        u'Hostname: wks-win764bitb '
        u'Path: C:\\Users\\nfury\\Pictures\\The SHIELD '
        u'Droid volume identifier: {cf6619c2-66a8-44a6-8849-1582fcd3a338} '
        u'Droid file identifier: {63eea867-7b85-11e1-8950-005056a50b40} '
        u'Birth droid volume identifier: '
        u'{cf6619c2-66a8-44a6-8849-1582fcd3a338} '
        u'Birth droid file identifier: {63eea867-7b85-11e1-8950-005056a50b40}')

    expected_msg_short = (
        u'Entry: 11 '
        u'Pin status: Unpinned '
        u'Path: C:\\Users\\nfury\\Pictures\\The SHIELD')

    self._TestGetMessageStrings(event_object, expected_msg, expected_msg_short)

    # Check a WinLnkLinkEvent.
    event_object = event_objects[1]

    expected_timestamp = timelib_test.CopyStringToTimestamp(
        '2010-11-10 07:51:16.749125')
    self.assertEquals(event_object.timestamp, expected_timestamp)

    expected_msg = (
        u'File size: 3545 '
        u'File attribute flags: 0x00002020 '
        u'Drive type: 3 '
        u'Drive serial number: 0x24ba718b '
        u'Local path: C:\\Users\\nfury\\AppData\\Roaming\\Microsoft\\Windows\\'
        u'Libraries\\Documents.library-ms '
        u'Link target: [Users Libraries, UNKNOWN: 0x00]')

    expected_msg_short = (
        u'C:\\Users\\nfury\\AppData\\Roaming\\Microsoft\\Windows\\Libraries\\'
        u'Documents.library-ms')

    self._TestGetMessageStrings(event_object, expected_msg, expected_msg_short)


if __name__ == '__main__':
  unittest.main()
