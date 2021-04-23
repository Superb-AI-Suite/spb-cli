# MIT License
#
# Copyright (c) 2020 Superb AI Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .commands import (
    CreateCommand,
    DescribeCommand,
    DeleteCommand,
    UpdateCommand
)
from spb.exceptions import CommandInitiationFailedException


class CommandBuilder:
    """

    """
    __command_map_ = {
        'describe': DescribeCommand,
        'create': CreateCommand,
        'delete': DeleteCommand,
        'update': UpdateCommand
    }

    def __init__(self, op_name, res_name):
        self.op_name = op_name
        self.res_name = res_name

    def build(self):
        if not self.op_name:
            raise CommandInitiationFailedException('Command operation name is not correct')

        if not self.res_name:
            raise CommandInitiationFailedException('Command resource name is not correct')

        return self.__command_map_[self.op_name](self.res_name)


class CmdMeta(type):
    """
    Command Metaclass 
    """

    def __call__(self, *args, **kwargs):
        str_cmd = kwargs.get('type', None)
        if not str_cmd:
            raise CommandInitiationFailedException('Command need to init with type param')

        op_name, res_name = str_cmd.split('_')
        if not op_name or not res_name:
            raise CommandInitiationFailedException('Command need to take the form of "[op_name]_[resource_name]"')

        return CommandBuilder(op_name, res_name).build()


class Command(metaclass=CmdMeta):
    def __init__(self, type):
        print(self.__dict__)
