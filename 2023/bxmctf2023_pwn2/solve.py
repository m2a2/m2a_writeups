import re
from pwn import process, context, remote


def solve_add(arg1, arg2):
    return arg1 + arg2


def solve_sub(arg1, arg2):
    return arg1 - arg2


def parse_line_and_solve(q_line):
    args = list(q_line.split())
    return solve_add(int(args[0].strip()), int(args[2].strip()))


def locate_line_solve(the_argument):
    with open(r'./m2a.out', 'r', encoding="utf-8") as fp:
        lines = fp.readlines()
        for the_line in lines:
            # check if the string is present on a current line
            if the_argument in the_line:
                if 'The equation was ?' in the_line:
                    # print('Line Number:', lines.index(line))
                    print('Line:', the_line)
                    the_args = re.findall(r'\d+', the_line)
                    the_result = solve_sub(int(the_args[1]), int(the_args[0]))
                    return the_result


script = process("./run_mult.sh")
# context.log_level = 'debug'
io = remote('198.199.90.158', 32830)
# io = process("./main")
banner = io.recvuntil(b'math!\n')
print(banner)

for i in range(5):
    qustion_line = io.recvuntil(b'=')
    b'' == io.recv(timeout=0.01)  # collecting extra data (which we discard)
    print(qustion_line)
    result = parse_line_and_solve(qustion_line)
    print(result)
    io.sendline('{}\n'.format(result))

banner2 = io.recvuntil(b'rest!\n')
print(banner2)

# if True:
for i in range(10):
    rcev_line = str(io.recvuntil(b'\n', timeout=0.5))
    # b'' == io.recv(timeout=0.5)
    print(rcev_line)
    if '#' in rcev_line:
        the_arg = re.findall(r'\d+', rcev_line)[0]
        result = locate_line_solve(the_arg)
        print(result)
        b'' == io.recv(timeout=0.5)  # collecting extra data (which we discard)
        io.sendline(str(result))


banner3_and_flag = io.recv(timeout=5)
print(banner3_and_flag)
