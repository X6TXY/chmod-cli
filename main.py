import os

import inquirer
import pyfiglet
from colorama import Fore, init

init(autoreset=True)


def welcome():
    ascii_art = pyfiglet.figlet_format("chmod-cli")
    print(Fore.MAGENTA + ascii_art)


def help():
    print(Fore.YELLOW + "Help:")
    print(Fore.GREEN + "(↑) Move up")
    print(Fore.GREEN + "(↓) Move down")
    print(Fore.GREEN + "(→) for True")
    print(Fore.GREEN + "(←) for False")
    print(Fore.GREEN + "(Enter) for select")
    input("Press Enter to continue...")


def main():

    options_questions = [
        inquirer.Checkbox(
            'options',
            message=Fore.CYAN + "Options",
            choices=[
                ('Verbose (-v)', '-v'),
                ('Changes (-c)', '-c'),
                ('Silent (-f)', '-f'),
                ('Default (-R)', '-R')
            ],
        ),
        inquirer.List(
            'command_mode',
            message=Fore.CYAN + "Command Mode",
            choices=['Octal', 'Symbolic'],
        ),
        inquirer.List(
            'path_type',
            message=Fore.CYAN + "Path Type",
            choices=['File', 'Directory'],
        ),
    ]
    options_answers = inquirer.prompt(options_questions)
    permission_questions = [
        inquirer.Checkbox(
            'owner_perms',
            message=Fore.LIGHTMAGENTA_EX + "Select permissions for Owner",
            choices=[
                ('Read (r)', 'r'),
                ('Write (w)', 'w'),
                ('Execute (x)', 'x'),
            ],
        ),
        inquirer.Checkbox(
            'group_perms',
            message=Fore.LIGHTMAGENTA_EX + "Select permissions for Group",
            choices=[
                ('Read (r)', 'r'),
                ('Write (w)', 'w'),
                ('Execute (x)', 'x'),
            ],
        ),
        inquirer.Checkbox(
            'other_perms',
            message=Fore.LIGHTMAGENTA_EX + "Select permissions for Other",
            choices=[
                ('Read (r)', 'r'),
                ('Write (w)', 'w'),
                ('Execute (x)', 'x'),
            ],
        ),
    ]

    permission_answers = inquirer.prompt(permission_questions)
    path_question = [
        inquirer.Path(
            'path',
            message=Fore.CYAN + "Enter the path of the file or directory",
            path_type=inquirer.Path.FILE
            if options_answers['path_type'] == 'File'
            else inquirer.Path.DIRECTORY,
        ),
    ]
    path_answers = inquirer.prompt(path_question)
    chmod_command = build_chmod_command(
        options_answers,
        permission_answers,
        path_answers['path'],
    )
    print(Fore.YELLOW + "Command: " + chmod_command)
    execute = inquirer.confirm(
        "Do you want to execute the command?",
        default=True,
    )
    if execute:
        os.system(chmod_command)
        print(Fore.GREEN + "Command executed successfully")
    else:
        print(Fore.RED + "Command execution cancelled")


def build_chmod_command(options, permissions, path):
    command = "chmod "

    if options['options']:
        command += ''.join(options['options']) + ' '

    if options['command_mode'] == 'Octal':
        octal_perm = calc_octal_perm(permissions)
        command += f"{octal_perm} "
    else:
        symbolic_perm = calc_symbolic_perm(permissions)
        command += f"{symbolic_perm} "

    command += f"'{path}'"
    return command


def calc_octal_perm(permissions):
    perm_map = {'r': 4, 'w': 2, 'x': 1}
    owner = sum(perm_map[p] for p in permissions['owner_perms'])
    group = sum(perm_map[p] for p in permissions['group_perms'])
    other = sum(perm_map[p] for p in permissions['other_perms'])
    return str(owner) + str(group) + str(other)


def calc_symbolic_perm(permissions):
    perm_str = ''
    entities = {'u': 'owner_perms', 'g': 'group_perms', 'o': 'other_perms'}
    for entity, perm_key in entities.items():
        perms = permissions[perm_key]
        if perms:
            perm_str += f"{entity}="
            perm_str += ''.join(perms)
            perm_str += ','
    return perm_str.rstrip(',')


if __name__ == "__main__":
    welcome()
    help()
    main()
