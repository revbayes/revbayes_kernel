import pexpect.replwrap
import re

from metakernel import REPLWrapper



change_prompt = None
prompt_cmd = 'printf("> ")'
x = REPLWrapper(cmd_or_spawn='/usr/local/bin/rb',
                prompt_regex=r'[>+] ',
                prompt_change_cmd=None)

x.run_command('x <- [1,')
x.run_command('2]')
x.run_command('x')

#print(x.run_command('for (i in 1:10) z[i] ~ dnNormal(0,1)'))
#print(x.run_command('z'))

#print(x.run_command('for (i in 1:10) {'))
#print(x.run_command('  y[i] ~ dnNorm(0,1)'))
#print(x.run_command('}'))
#print(x.run_command('y'))
