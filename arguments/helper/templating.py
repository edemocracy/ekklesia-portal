# -*- coding: utf-8 -*-

import os
from pyjade.ext.jinja import Compiler as JinjaCompiler
from pyjade.ext.jinja import PyJadeExtension as JinjaJadeExtension
from pyjade.utils import process


class JinjaAutoescapeCompiler(JinjaCompiler):
    autocloseCode = 'if,for,block,filter,autoescape,with,trans,spaceless,comment,cache,macro,localize,compress,call'.split(',')


    def visitCode(self, code):
        if code.buffer:
            val = code.val.lstrip()
            val = self.var_processor(val)
            self.buf.append('%s%s%s' % (self.variable_start_string, val,
                                        self.variable_end_string))
        else:
            self.buf.append('{%% %s %%}' % code.val)

        if code.block:
            self.visit(code.block)
            if not code.buffer:
                codeTag = code.val.strip().split(' ', 1)[0]
                if codeTag in self.autocloseCode:
                    self.buf.append('{%% end%s %%}' % codeTag)


class PyJadeExtension(JinjaJadeExtension):

    def preprocess(self, source, name, filename=None):
        if (not name or
                (name and not os.path.splitext(name)[1] in self.file_extensions)):
            return source
        return process(source, filename=name, compiler=JinjaAutoescapeCompiler, **self.options)
