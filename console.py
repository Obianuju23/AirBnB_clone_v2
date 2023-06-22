#!/usr/bin/python3
"""Importing some Standard modules and modules from our packages"""
import cmd
import sys
from shlex import split
from models.base_model import BaseModel
from datetime import datetime
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


"""
This is a Python class that will act as an interface for the first phase
of the AirBnB Clone project.
"""


class HBNBCommand(cmd.Cmd):
    """
    This is a class modelling the inteface (CLI) for AirBnB Clone project.
    """

    """Specify the prompt for the CLI"""
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    dot_cmds = ['all', 'count', 'create', 'show', 'destroy', 'update']
    
    classes = {'BaseModel': BaseModel,
               'User': User,
               'Place': Place,
               'State': State,
               'City': City,
               'Amenity': Amenity,
               'Review': Review}

    types = {'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float}

    def preloop(self) -> None:
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, arg: any) -> True:
        """Issues a quit command to the CLI by returning True"""
        return True

    def help_quit(self) -> None:
        """ Prints the help documentation for quit """
        print("")
        print("The `quit` command issues a command to quit the CLI")
        print("with formatting.\n[Usage]:\n(hbnb) quit\n")

    def do_EOF(self, arg: any) -> True:
        """Returns True and breaks the cmdloop"""
        print("")
        return True

    def help_EOF(self) -> None:
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")
        print("The `EOF` command returns True to break the cmdloop\n", end="")
        print("and exits the CLI.\n")
        print("[Usage]:\n(hbnb) EOF\nor\n(hbnb) <CTRL + C>")
        print("or\n(hbnb) <CTRL + Z>\n")

    def emptyline(self) -> None:
        """Method that does nothing when the ENTER key is pressed without a
        command."""
        pass

    def do_create(self, args) -> None:
        """Public instance method that creates new instance of a class, save
        it to a JSON file and print the `id` of the instance"""

        try:
            if not args:
                raise SyntaxError()

            arg_num = args.split(" ")
            cls_inst = eval("{}()".format(arg_num[0]))

            for cmd_arg in arg_num[1:]:
                param = cmd_arg.split("=")
                key = param[0]
                value = param[1].replace("_", " ")

                if hasattr(cls_inst, key):
                    try:
                        setattr(cls_inst, key, eval(value))
                    except Exception:
                        pass

            cls_inst.save()

            print("{}".format(cls_inst.id))
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            pass

    def help_create(self) -> None:
        """ Help information for the create method """
        print("Creates a class of any type\n")
        print("The `create` command creates an instance of a class, ", end="")
        print("saves it to the storage and prints out the ID of the", end=" ")
        print("instance created.\n")
        print("Models available includes:\n")
        print("\tAmenity\n\tBaseModel\n\tCity\n\tPlace\n\tReview\n\t", end="")
        print("State\n\tUser\n")
        print("[Usage]: create <classname>\n")
        print("Sample:\n(hbnb) create User\n")

    def do_show(self, args=None) -> None:
        """Public instance method that displays the string instance of a
        class, based on the instance id and classname specified"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self) -> None:
        """ Help information for the show command """
        print("Shows an individual instance of a class\n")
        print("The `show` command displays the details and string", end=" ")
        print("representation of an instance based on class name", end=" ")
        print("and instance id provided.\n")
        print("[Usage]: show <className> <objectId>\n")
        print("Sample:\n(hbnb) show User abcd-1234-5678-0987")
        print("")

    def do_destroy(self, args) -> None:
        """Public instance method that deletes the instance of a class,
        based on the instance id and classname specified"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del (storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self) -> None:
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("The `destroy` command deletes the details of an ", end="")
        print("instance based on class name and instance id provided.\n")
        print("[Usage]: destroy <className> <objectId>\n")
        print("Sample:\n(hbnb) destroy User abcd-1234-5678-0987\n")

    def do_all(self, args) -> None:
        """Public instance method that displays the string instance of all
        the instances of a class based on the classname specified or no
        classname specified"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self) -> None:
        """ Help information for the all command """
        print("Shows all objects, or all of a class\n")
        print("The `all` command displays the string representation", end="")
        print(" of all class instances present in the storage.\n")
        print("[Usage]: all <className>\n")
        print("Sample:\n(hbnb) all User\nor\n(hbnb) User.all()\n")

    def do_update(self, args) -> None:
        """Public instance method that updates a specified instance of a class
        using the id and either adding more attributes or updating an
        attribute"""
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self) -> None:
        """Updates the help for update"""
        print("")
        print("The `update` command update a specified instance of a", end="")
        print(" using the class name and the ID of the instance, and", end="")
        print(" and the specifying the attribute to update or adding", end="")
        print(" a new attribute plus the value.\n")
        print("Usage:\n(hbnb) update User 1234-5678 email 'test@oop.com'\n")

    def do_count(self, args) -> None:
        """Public instance method that counts the instances of a class"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self) -> None:
        """ Help information for the count command """
        print("")
        print("The `count` command displays the number of instances", end="")
        print(" of a specified class found in the storage.", end="\n")
        print("[Usage]: count <class_name>")
        print("Sample:\n(hbnb) count User'\nor\n(hbnb) User.count()\n")


if __name__ == "__main__":
    commnd = HBNBCommand()
    commnd.cmdloop()
