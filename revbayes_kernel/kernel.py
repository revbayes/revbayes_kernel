from __future__ import print_function

import codecs
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from xml.dom import minidom

from metakernel import MetaKernel, ProcessMetaKernel, REPLWrapper, u
from metakernel.pexpect import which

from . import __version__


STDIN_PROMPT = '> '
STDIN_PROMPT_REGEX = re.compile(r'%s' % STDIN_PROMPT)
HELP_LINKS = [
    {
        'text': "RevBayes",
        'url': "https://revbayes.org",
    },
    {
        'text': "RevBayes Kernel",
        'url': "https://github.com/sdwfrost/revbayes_kernel",
    },

] + MetaKernel.help_links


class RevBayesKernel(ProcessMetaKernel):
    implementation = 'RevBayes Kernel'
    implementation_version = __version__,
    language = 'Rev'
    help_links = HELP_LINKS

    _revbayes_engine = None

    @property
    def language_info(self):
        return {'mimetype': 'text/x-rsrc',
                'name': 'RevBayes',
                'file_extension': '.Rev',
                'help_links': HELP_LINKS,
                'pygments_lexer': 'R',
                'codemirror_mode': {'name': 'r' }}

    @property
    def banner(self):
        msg = 'RevBayes Kernel v%s'
        return msg % (__version__)

    @property
    def revbayes_engine(self):
        if self._revbayes_engine:
            return self._revbayes_engine
        self._revbayes_engine = RevBayesEngine(error_handler=self.Error,
                                           stdin_handler=self.raw_input,
                                           stream_handler=self.Print,
                                           logger=self.log)
        return self._revbayes_engine

    def makeWrapper(self):
        """Start an RevBayes process and return a :class:`REPLWrapper` object.
        """
        return self.revbayes_engine.repl

    def do_execute_direct(self, code, silent=False, allow_stdin=True):
        if code.strip() in ['q()', 'quit()']:
            self._revbayes_engine = None
            self.do_shutdown(True)
            return
        val = ProcessMetaKernel.do_execute_direct(self, code, silent=silent)
        return val

    def get_kernel_help_on(self, info, level=0, none_on_fail=False):
        obj = info.get('help_obj', '')
        if not obj or len(obj.split()) > 1:
            if none_on_fail:
                return None
            else:
                return ""
        return self.revbayes_engine.eval('?%s' % obj, silent=True)

    def Print(self, *args, **kwargs):
        # Ignore standalone input hook displays.
        out = []
        for arg in args:
            if arg.strip() == STDIN_PROMPT:
                return
            if arg.strip().startswith(STDIN_PROMPT):
                arg = arg.replace(STDIN_PROMPT, '')
            out.append(arg)
        super(RevBayesKernel, self).Print(*out, **kwargs)

    def raw_input(self, text):
        # Remove the stdin prompt to restore the original prompt.
        text = text.replace(STDIN_PROMPT, '')
        return super(RevBayesKernel, self).raw_input(text)

class RevBayesEngine(object):

    def __init__(self, error_handler=None, stream_handler=None,
                 stdin_handler=None,
                 logger=None):
        self.logger = logger
        self.executable = self._get_executable()
        self.repl = self._create_repl()
        self.error_handler = error_handler
        self.stream_handler = stream_handler
        self.stdin_handler = stdin_handler
        self._startup()

    def eval(self, code, timeout=None, silent=False, allow_stdin=True):
        """Evaluate code using the engine.
        """
        stream_handler = None if silent else self.stream_handler
        if self.logger:
            self.logger.debug('RevBayes eval:')
            self.logger.debug(code)
        try:
            resp = self.repl.run_command(code.rstrip(),
                                         timeout=timeout,
                                         stream_handler=stream_handler,
                                         stdin_handler=self.stdin_handler)
            resp = resp.replace(STDIN_PROMPT, '')
            if self.logger and resp:
                self.logger.debug(resp)
            return resp
        except KeyboardInterrupt:
            return self._interrupt(True)
        except Exception as e:
            if self.error_handler:
                self.error_handler(e)
            else:
                raise e

    def _startup(self):
        here = os.path.dirname(os.path.realpath(__file__))
        self.eval('os.chdir("%s")' % here)

    def _create_repl(self):
        exec_name = os.path.split(self.executable)[-1]
        if exec_name == 'exe':
            exec_name = os.path.split(self.executable)[-2]
        if exec_name == 'rb-jupyter':
            cmd = self.executable
        else:
            cmd_string = self.executable + ' --jupyter'
            cmd = cmd_string
        # Interactive mode prevents crashing on Windows on syntax errors.
        # Delay sourcing the "~/.octaverc" file in case it displays a pager.

        repl = REPLWrapper(cmd_or_spawn=cmd,
                           prompt_regex=r'[>+] $',
                           prompt_change_cmd=None)

        if os.name == 'nt':
            repl.child.crlf = '\n'
        repl.interrupt = self._interrupt
        # Remove the default 50ms delay before sending lines.
        repl.child.delaybeforesend = None
        return repl
    def do_complete(self, code, cursor_pos):
        return {'status': 'ok',
             'cursor_start': ...,
             'cursor_end': ...,
             'matches': [...]}

    def _interrupt(self, silent=False):
        if (os.name == 'nt'):
            msg = '** Warning: Cannot interrupt RevBayes on Windows'
            if self.stream_handler:
                self.stream_handler(msg)
            elif self.logger:
                self.logger.warn(msg)
            return self._interrupt_expect(silent)
        return REPLWrapper.interrupt(self.repl)

    def _interrupt_expect(self, silent):
        repl = self.repl
        child = repl.child
        expects = [repl.prompt_regex, child.linesep]
        expected = uuid.uuid4().hex
        repl.sendline('print("%s");' % expected)
        if repl.prompt_emit_cmd:
            repl.sendline(repl.prompt_emit_cmd)
        lines = []
        while True:
            # Prevent a keyboard interrupt from breaking this up.
            while True:
                try:
                    pos = child.expect(expects)
                    break
                except KeyboardInterrupt:
                    pass
            if pos == 1:  # End of line received
                line = child.before
                if silent:
                    lines.append(line)
                else:
                    self.stream_handler(line)
            else:
                line = child.before
                if line.strip() == expected:
                    break
                if len(line) != 0:
                    # prompt received, but partial line precedes it
                    if silent:
                        lines.append(line)
                    else:
                        self.stream_handler(line)
        return '\n'.join(lines)

    def _get_executable(self):
        """Find the best RevBayes executable.
        """
        executable = os.environ.get('REVBAYES_JUPYTER_EXECUTABLE', None)
        if not executable or not which(executable):
            if which('rb'):
                executable = 'rb'
            else:
                msg = ('RevBayes Executable not found, please add to path or set',
                       '\"REVBAYES_JUPYTER_EXECUTABLE\" environment variable.',
                       'See README.md for instructions to build rb-jupyter.')
                raise OSError(msg)
        executable = executable.replace(os.path.sep, '/')
        return executable
