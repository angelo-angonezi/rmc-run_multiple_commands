#!/usr/bin/python3

# 'run multiple commands based on txt file' module
# Code destined to running multiple system commands
# with python, based on a text file

######################################################################
# imports

from time import time
from argparse import ArgumentParser
from os import system

#####################################################################
# argument parsing related functions


def get_args_dict() -> dict:
    """
    Parses the arguments and returns a dictionary of the arguments.
    :return: Dictionary. Represents the parsed arguments.
    """
    # defining program description
    description = "run multiple commands is a script for "
    description += "sequentially executing multiple commands "
    description += "based on a txt file (one command per line)"

    # creating a parser instance
    parser = ArgumentParser(description=description)

    # adding arguments to parser
    parser.add_argument('-c', '--commands',
                        dest='commands',
                        help='defines path to text file containing multiple commands',
                        required=True)

    parser.add_argument('-e', '--enter',
                        dest='enter',
                        action='store_true',
                        help='defines whether or not to require "enter" inputs from user between commands',
                        required=False)

    parser.add_argument('-l', '--log',
                        dest='log',
                        help='defines whether or not to save log info, and save path to log info.',
                        required=False,
                        default=None)

    # creating arguments dictionary
    args_dict = vars(parser.parse_args())

    # returning the arguments dictionary
    return args_dict


######################################################################
# defining auxiliary functions


def execute_multiple_commands(path_to_commands_txt: str,
                              enter_param: bool,
                              log_path: str or None
                              ) -> None:
    """
    Given a path to a txt file containing multiple commands (one command per line),
    executes each command sequentially using python os.system function.
    :param path_to_commands_txt: String. Represents a path to a txt file.
    :param enter_param: Boolean. Defines whether or not to require an 'enter' input
    from user between commands execution.
    :param log_path: String or None. Represents path to save an execution log file.
    :return: None.
    """
    # defining spacer string
    spacer = '_' * 50

    # starting total time variable
    total_time = 0
    
    # opening commands txt file
    with open(path_to_commands_txt, 'r') as open_txt_file:

        # getting lines as commands
        commands = open_txt_file.readlines()

        # filtering comments (lines starting with #s)
        commands = [command for command in commands if (not command.startswith('#'))]

        # getting total number of commands
        commands_num = len(commands)

        # iterating over commands
        for index, command in enumerate(commands, 1):

            # removing 'enters' from command
            command = command.replace('\n', '')

            # getting start time
            t_start = time()

            # printing spacer string
            print(spacer)
            f_string = f'executing command {index} of {commands_num}: {command}'
            print(f_string)

            # checking if save info has to be saved
            if log_path is not None:
                current_command_log_index = f'_cmd{index}.txt'
                current_log_path = log_path.replace('.txt', current_command_log_index)
                log_add = f' | tee {current_log_path}'
                command += log_add

            # executing command
            system(command)

            # getting end time
            t_end = time()

            # getting time difference and updating total time
            t_diff = t_end - t_start
            total_time += t_diff
            t_diff = round(t_diff, 2)
            t_string = f'executed command in {t_diff} seconds'
            print(t_string)

            # checking if user input is required to proceed
            if enter_param:
                input("press 'enter' to continue")

        # printing spacer string
        print(spacer)
        total_time = round(total_time, 2)
        end_string = f'all {commands_num} commands executed in {total_time} seconds'
        print(end_string)

######################################################################
# defining main function


def main():
    """
    Runs main code.
    """
    # getting args dict
    args_dict = get_args_dict()

    # getting path to commands text file
    commands = args_dict['commands']

    # getting enter input requirement parameter
    enter_param = args_dict['enter']

    # getting log path parameter
    log_param = args_dict['log']

    # running function
    execute_multiple_commands(path_to_commands_txt=commands,
                              enter_param=enter_param,
                              log_path=log_param)

######################################################################
# running main function


if __name__ == '__main__':
    main()

######################################################################
# end of current module
