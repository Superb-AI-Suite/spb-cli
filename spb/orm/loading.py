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

# It is comming from Django loading code snippet. So, if you want to look into details
# please visit to

import sys
import os
import glob
import importlib
import threading
from spb.orm.model import Model
from spb.exceptions import ResourceIsNotExistedException


class Loader(object):
    """
    A cache that stores installed applications and their models. Used to
    provide reverse-relations and for app introspection (e.g. admin).
    """
    # Use the Borg pattern to share state between all instances. Details at
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66531.
    __model_classes_ = dict(
        loaded=False,
        write_lock=threading.RLock(),
        models={}
    )

    def __init__(self):
        self.__dict__ = self.__model_classes_

    def _populate(self):
        """
        Fill in all the cache information. This method is threadsafe, in the
        sense that every caller will see the same state upon return, and if the
        cache is already initialised, it does no work.
        """
        if self.loaded:
            return
        self.write_lock.acquire()
        try:
            if self.loaded:
                return
            self.load_model()
            self.loaded = True
        finally:
            self.write_lock.release()

    def get_model(self, res_model):
        """
        Given a module containing models, returns a list of the models.
        Otherwise returns a list of all installed models.
        """
        if not self.loaded:
            self._populate()

        return self.models[res_model]

    def load_model(self):
        BASE_BASE_DIR = (os.sep).join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-1])
        BASE_DIR = os.path.join(BASE_BASE_DIR, 'models')
        file_list = glob.glob(os.path.join(BASE_DIR, '*.py'))
        for module in file_list:
            if module.find('__init__') == -1:
                # module_file = os.path.join(BASE_DIR, module)
                module_file = module.replace(os.sep, '/')
                # TODO:// object -> Base class
                inherited_class = self._import_class(module_file, Model)
                self.models[inherited_class.__name__.lower()] = inherited_class

    def _import_class(self, implementation_filename, base_class):
        impl_dir, impl_filename = os.path.split(implementation_filename)
        module_name, _ = os.path.splitext(impl_filename)

        try:
            sys.path.insert(0, impl_dir)
            module = importlib.import_module(module_name)
            for name in dir(module):
                obj = getattr(module, name)
                if (type(obj) == type(base_class)
                    and issubclass(obj, base_class)
                        and obj != base_class):
                    return obj
            raise ResourceIsNotExistedException(
                f"No subclass of {base_class.__name__} in {implementation_filename}")
        finally:
            sys.path.pop(0)
