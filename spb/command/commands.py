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

import abc

from spb.orm import Loader


class BaseCommand(metaclass=abc.ABCMeta):
    """
    A BaseCommand is base class of command operation classes.
    """

    def __init__(self, res_name):
        """
        type: str
        res_name: resource name 
        """
        self.res_name = res_name
        self._loader = Loader()

    @abc.abstractmethod
    def execute(self, session=None, option=None, optional=None):
        """
        Caution: 
        """
        if type(self) is BaseCommand:
            raise NotImplementedError("Interfaces can't be instantiated")


class DescribeCommand(BaseCommand):
    """
    Describe command is for retrieving
    """

    def execute(self, session=None, option=None, optional=None):
        DescribeModel = self._loader.get_model(self.res_name)
        model = DescribeModel()
        return model.manager().query(option, optional)


class CreateCommand(BaseCommand):
    """
    Creation command
    """

    def execute(self, session=None, option=None, optional=None):
        CreateModel = self._loader.get_model(self.res_name)
        model = CreateModel()
        return model.manager().mutation(option, optional)


class DeleteCommand(BaseCommand):
    """
    Delete command
    """

    def execute(self, session=None, option=None, optional=None):
        print('exeute in DeleteCommand')


class UpdateCommand(BaseCommand):
    """
    Update command
    """

    def execute(self, session=None, option=None, optional=None):
        UpdateModel = self._loader.get_model(self.res_name)
        model = UpdateModel()
        return model.manager().mutation(option, optional)
