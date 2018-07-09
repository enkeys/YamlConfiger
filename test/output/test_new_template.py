# Copyright 2018 Red Hat Inc.
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

import os
import shutil

import mock as mock
import pytest

import amqcfg.output
from amqcfg.output import new_template
from ..files.fakes import fake_templates_path, fake_select_template_dir


@mock.patch('amqcfg.output.select_template_dir',
            side_effect=fake_select_template_dir)
@mock.patch('amqcfg.output.ensure_output_path', mock.Mock())
@mock.patch('shutil.copytree', mock.Mock())
def test_true(*_):
    template_name = 'my_template/1.2.3'
    template_path = fake_templates_path()
    template = os.path.join(template_path, template_name)
    destination_path = '/output/template/dir/'
    destination_name = 'new_template'
    destination = os.path.join(destination_path, destination_name)

    new_template(template_name, destination)
    # noinspection PyUnresolvedReferences
    amqcfg.output.ensure_output_path.assert_called_with(destination)
    # noinspection PyUnresolvedReferences
    shutil.copytree.assert_called_with(template, destination,
                                       symlinks=False)


@mock.patch('amqcfg.output.select_template_dir',
            side_effect=fake_select_template_dir)
@mock.patch('amqcfg.output.ensure_output_path',
            side_effect=OSError('[Errno 13] Permission denied: \'path\''))
@mock.patch('shutil.copytree', mock.Mock())
def test_bad_destination(*_):
    template_name = 'my_template/1.2.3'
    destination = '/bad/destination'

    with pytest.raises(OSError):
        new_template(template_name, destination)
    # noinspection PyUnresolvedReferences
    amqcfg.output.ensure_output_path.assert_called_with(destination)
    # noinspection PyUnresolvedReferences
    shutil.copytree.assert_not_called()


@mock.patch('amqcfg.output.select_template_dir',
            side_effect=fake_select_template_dir)
@mock.patch('amqcfg.output.ensure_output_path', side_effect=mock.Mock())
def test_no_destination(*_):
    template_name = 'my_template/1.2.3'
    destination = ''

    with pytest.raises(OSError):
        new_template(template_name, destination)
    # noinspection PyUnresolvedReferences
    amqcfg.output.ensure_output_path.assert_not_called()
