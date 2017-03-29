from metakernel import REPLWrapper

# works with ``#define RB_XCODE``, i.e. no linenoise
cmd = '/usr/local/bin/rb'         

# possibly broken with the cmake version
# cmd = '/usr/local/bin/revbayes'


x = REPLWrapper(cmd_or_spawn=cmd,
                prompt_regex=r'[>+] ',
                prompt_change_cmd=None,
                echo=True)

# RevBayes uses u'\n\r' as CRLF
# x.child.crlf = '\n'

x.run_command('val <- [1,')
x.run_command('2]')
x.run_command('val')

#print(x.run_command('for (i in 1:10) z[i] ~ dnNormal(0,1)'))
#print(x.run_command('z'))

#print(x.run_command('for (i in 1:10) {'))
#print(x.run_command('  y[i] ~ dnNorm(0,1)'))
#print(x.run_command('}'))
#print(x.run_command('y'))
