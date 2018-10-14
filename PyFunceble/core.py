#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check the availability of domains, IPv4 or URL.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This module is half of the brain of PyFunceble.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long
# pylint: disable=bad-continuation, too-many-lines

from domain2idna import get as domain2idna

import PyFunceble
from PyFunceble import Fore, Style, path, repeat
from PyFunceble.auto_continue import AutoContinue
from PyFunceble.auto_save import AutoSave
from PyFunceble.check import Check
from PyFunceble.database import Database
from PyFunceble.directory_structure import DirectoryStructure
from PyFunceble.execution_time import ExecutionTime
from PyFunceble.expiration_date import ExpirationDate
from PyFunceble.helpers import Command, Download, List, Regex
from PyFunceble.mining import Mining
from PyFunceble.percentage import Percentage
from PyFunceble.prints import Prints
from PyFunceble.sort import Sort
from PyFunceble.url import URL


class Core:  # pragma: no cover
    """
    Main entry to PYFunceble. Brain of the program. Also known as "put everything
    together to make the system works".

    Arguments:
        - domain: str
            A domain or IP to test.
        - file_path: str
            A path to a file to read.
    """

    def __init__(self, domain=None, file_path=None, **args):
        # We initiate our list of optional arguments with their default values.
        optional_arguments = {
            "url_to_test": None,
            "url_file": None,
            "modulo_test": False,
            "link_to_test": None,
        }

        # We initiate our optional_arguments in order to be usable all over the
        # class.
        for (arg, default) in optional_arguments.items():
            setattr(self, arg, args.get(arg, default))

        # We manage the entries.
        self._entry_management(domain, file_path)

    @classmethod
    def _entry_management_url_download(cls, passed):
        """
        This method will check if the given information is a URL.
        If it is the case, it download and change the file to test.

        Argument:
            - passed: str
                The argument passed to the system.
        """

        if passed and Check().is_url_valid(passed):
            # The passed string is an URL.

            # We get the file name based on the URL.
            # We actually just get the  string after the last `/` in the URL.
            file_to_test = passed.split("/")[-1]

            if (
                not path.isfile(file_to_test)
                or PyFunceble.CONFIGURATION["counter"]["number"]["tested"] == 0
            ):
                # The filename does not exist in the current directory
                # or the currently number of tested is equal to 0.

                # We download the content of the link.
                Download(passed, file_to_test).text()

            # The files does exist or the currently number of tested is greater than
            # 0.

            # We initiate the file we have to test.
            PyFunceble.CONFIGURATION["file_to_test"] = file_to_test

            # We return true to say that everything goes right.
            return True

        # The passed string is not an URL.

        # We do not need to do anything else.
        return False

    def _entry_management_url(self):
        """
        This method will manage the loading of the url system.
        """

        if (
            self.url_file  # pylint: disable=no-member
            and not self._entry_management_url_download(
                self.url_file  # pylint: disable=no-member
            )
        ):  # pylint: disable=no-member
            # The current url_file is not a URL.

            # We initiate the filename as the file we have to test.
            PyFunceble.CONFIGURATION[
                "file_to_test"
            ] = self.url_file  # pylint: disable=no-member

    def _entry_management(self, domain, file_path):
        """
        This method avoid to have 1 millions line into self.__init__()

        Arguments:
            - domain: string
                The domain parsed to Core().
            - file_path: string
                The file_path parsed to Core().
        """

        if not self.modulo_test:  # pylint: disable=no-member
            # We are not in a module usage.

            # We set the file_path as the file we have to test.
            PyFunceble.CONFIGURATION[
                "file_to_test"
            ] = file_path  # pylint: disable=no-member

            # We check if the given file_path is an url.
            # If it is an URL we update the file to test and download
            # the given URL.
            self._entry_management_url()

            if PyFunceble.CONFIGURATION["travis"]:
                # The Travis CI mode is activated.

                # We fix the environnement permissions.
                AutoSave().travis_permissions()

            # We check if we need to bypass the execution of PyFunceble.
            self.bypass()

            # We set the start time.
            ExecutionTime("start")

            if domain:
                # The given domain is not empty or None.

                # We deactivate the showing of percentage as we are in a single
                # test run.
                PyFunceble.CONFIGURATION["show_percentage"] = False

                if PyFunceble.CONFIGURATION["idna_conversion"]:
                    domain = domain2idna(domain.lower())
                else:
                    domain = domain.lower()

                # We test the domain after converting it to lower case.
                self.domain(domain)
            elif self.url_to_test and not file_path:  # pylint: disable=no-member
                # An url to test is given and the file path is empty.

                # We deactivate the showing of percentage as we are in a single
                # test run.
                PyFunceble.CONFIGURATION["show_percentage"] = False

                # We test the url to test.
                self.url(self.url_to_test)  # pylint: disable=no-member
            elif (
                self._entry_management_url_download(
                    self.url_file  # pylint: disable=no-member
                )
                or self.url_file  # pylint: disable=no-member
            ):
                # * A file full of URL is given.
                # or
                # * the given file full of URL is a URL.

                # * We deactivate the whois subsystem as it is not needed for url testing.
                # * We activate the generation of plain list element.
                # * We activate the generation of splited data instead of unified data.
                PyFunceble.CONFIGURATION["no_whois"] = PyFunceble.CONFIGURATION[
                    "plain_list_domain"
                ] = PyFunceble.CONFIGURATION["split"] = True

                # We deactivate the generation of hosts file as it is not relevant for
                # url testing.
                PyFunceble.CONFIGURATION["generate_hosts"] = False

                # And we test the given or the downloaded file.
                self.file_url()
            elif (
                self._entry_management_url_download(
                    self.link_to_test  # pylint: disable=no-member
                )
                or self._entry_management_url_download(file_path)
                or file_path
            ):
                # * A file path is given.
                # or
                # * The given file path is an URL.
                # or
                # * A link to test is given.

                # We test the given or the downloaded file.
                self.file()
            else:
                # No file, domain, single url or file or url is given.

                # We print a message on screen.
                print(Fore.CYAN + Style.BRIGHT + "Nothing to test.")

            # We stop and log the execution time.
            ExecutionTime("stop")

            # We log the current percentage state.
            Percentage().log()

            if domain:
                # We are testing a domain.

                # We show the colored logo.
                self.colored_logo()
        else:
            # We are used as an imported module.

            # We activate the simple mode as the table or any full
            # details on screen are irrelevant.
            PyFunceble.CONFIGURATION["simple"] = True

            # We activate the quiet mode.
            PyFunceble.CONFIGURATION["quiet"] = True

            # And we deactivate the generation of files.
            PyFunceble.CONFIGURATION["no_files"] = True

            if domain:
                # A domain is given.

                # We set the domain to test.
                PyFunceble.CONFIGURATION["domain"] = domain.lower()

    def test(self):
        """
        This method avoid confusion between self.domain which is called into
        __main__ and test() which should be called out of PyFunceble's scope.

        Returns: str
            ACTIVE, INACTIVE or INVALID.

        Raise:
            - Exception: when this method is called under __name___
        """

        if not self.modulo_test:  # pylint: disable=no-member
            # We are not used as an imported module.

            # We inform the user that they should not use this method.
            raise Exception(
                "You should not use this method. Please prefer self.domain()"
            )

        else:
            # We are used as an imported module.

            # We return the status of the parsed domain.
            return ExpirationDate().get()

    @classmethod
    def bypass(cls):
        """
        Exit the script if `[PyFunceble skip]` is matched into the latest
        commit message.
        """

        # We set the regex to match in order to bypass the execution of
        # PyFunceble.
        regex_bypass = r"\[PyFunceble\sskip\]"

        if (
            PyFunceble.CONFIGURATION["travis"]
            and Regex(
                Command("git log -1").execute(), regex_bypass, return_data=False
            ).match()
        ):
            # * We are under Travis CI.
            # and
            # * The bypass marker is matched into the latest commit.

            # We save everything and stop PyFunceble.
            AutoSave(True, is_bypass=True)

    @classmethod
    def _print_header(cls):
        """
        Decide if we print or not the header.
        """

        if (
            not PyFunceble.CONFIGURATION["quiet"]
            and not PyFunceble.CONFIGURATION["header_printed"]
        ):
            # * The quiet mode is not activated.
            # and
            # * The header has not been already printed.

            # We print a new line.
            print("\n")

            if PyFunceble.CONFIGURATION["less"]:
                # We have to show less informations on screen.

                # We print the `Less` header.
                Prints(None, "Less").header()
            else:
                # We have to show every informations on screen.

                # We print the `Generic` header.
                Prints(None, "Generic").header()

            # The header was printed.

            # We initiate the variable which say that the header has been printed to True.
            PyFunceble.CONFIGURATION["header_printed"] = True

    def _file_decision(self, current, last, status=None):
        """
        Manage the database, autosave and autocontinue systems for the case that we are reading
        a file.

        Arguments:
            - status: str
                The current status of current.
            - current: str
                The current domain or URL we are testing.
            - last: str
                The last domain or URL of the file we are testing.
        """

        if status:
            # The status is given.

            if (
                not PyFunceble.CONFIGURATION["simple"]
                and PyFunceble.CONFIGURATION["file_to_test"]
            ):
                # * The simple mode is deactivated.
                # and
                # * A file to test is set.

                # We run the mining logic.
                Mining().process()

                # We delete the currently tested element from the mining
                # database.
                # Indeed, as it is tested, it is already in our
                # testing process which means that we don't need it into
                # the mining database.
                Mining().remove()

                if status.lower() in PyFunceble.STATUS["list"]["up"]:
                    # The status is in the list of up status.

                    # We remove the currently tested element from the
                    # database.
                    Database().remove()
                else:
                    # The status is not in the list of up status.

                    # We add the currently tested element to the
                    # database.
                    Database().add()

                # We backup the current state of the file reading
                # for the case that we need to continue later.
                AutoContinue().backup()

                if current != last:
                    # The current element is not the last one.

                    # We run the autosave logic.
                    AutoSave()
                else:
                    # The current element is the last one.

                    # We stop and log the execution time.
                    ExecutionTime("stop")

                    # We show/log the percentage.
                    Percentage().log()

                    # We reset the counters as we end the process.
                    self.reset_counters()

                    # We backup the current state of the file reading
                    # for the case that we need to continue later.
                    AutoContinue().backup()

                    # We show the colored logo.
                    self.colored_logo()

                    # We save and stop the script if we are under
                    # Travis CI.
                    AutoSave(True)

        for index in ["http_code", "referer"]:
            # We loop through some configuration index we have to empty.

            if index in PyFunceble.CONFIGURATION:
                # The index is in the configuration.

                # We empty the configuration index.
                PyFunceble.CONFIGURATION[index] = ""

    def domain(self, domain=None, last_domain=None):
        """
        Manage the case that we want to test only a domain.

        Argument:
            - domain: str
                The domain or IP to test.
            - last_domain: str
                The last domain of the file we are testing.
        """

        # We print the header.
        self._print_header()

        if domain:
            # A domain is given.

            # We format and set the domain we are testing and treating.
            PyFunceble.CONFIGURATION["domain"] = self._format_domain(domain)
        else:
            # A domain is not given.

            # We set the domain we are testing and treating to None.
            PyFunceble.CONFIGURATION["domain"] = None

        if PyFunceble.CONFIGURATION["domain"]:
            # The domain is given (Not None).

            # We test and get the status of the domain.
            status = ExpirationDate().get()

            # We run the file decision logic.
            self._file_decision(domain, last_domain, status)

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the domain and the status.
                print(domain, status)

    @classmethod
    def reset_counters(cls):
        """
        Reset the counters when needed.
        """

        for string in ["up", "down", "invalid", "tested"]:
            # We loop through to the index of the autoContinue subsystem.

            # And we set their counter to 0.
            PyFunceble.CONFIGURATION["counter"]["number"].update({string: 0})

    @classmethod
    def colored_logo(cls):
        """
        This method print the colored logo based on global results.
        """

        if not PyFunceble.CONFIGURATION["quiet"]:
            # The quiet mode is not activated.

            if PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] >= 50:
                # The percentage of up is greater or equal to 50%.

                # We print the CLI logo in green.
                print(Fore.GREEN + PyFunceble.ASCII_PYFUNCEBLE)
            else:
                # The percentage of up is less than 50%.

                # We print the CLI logo in red.
                print(Fore.RED + PyFunceble.ASCII_PYFUNCEBLE)

    @classmethod
    def _format_domain(cls, extracted_domain):
        """
        Format the extracted domain before passing it to the system.

        Argument:
            extracted_domain: str
                The extracted domain from the file.

        Returns: str
            The domain to test.
        """

        if not extracted_domain.startswith("#"):
            # The line is not a commented line.

            if "#" in extracted_domain:
                # There is a comment at the end of the line.

                # We delete the comment from the line.
                extracted_domain = extracted_domain[
                    : extracted_domain.find("#")
                ].strip()

            if " " in extracted_domain or "\t" in extracted_domain:
                # A space or a tabs is in the line.

                # We remove all whitestring from the extracted line.
                splited_line = extracted_domain.split()

                # As there was a space or a tab in the string, we consider
                # that we are working with the hosts file format which means
                # that the domain we have to test is after the first string.
                # So we set the index to 1.
                index = 1

                while index < len(splited_line):
                    # We loop until the index is greater than the length of
                    #  the splited line.

                    if splited_line[index]:
                        # The element at the current index is not an empty string.

                        # We break the loop.
                        break

                    # The element at the current index is an empty string.

                    # We increase the index number.
                    index += 1

                # We return the last read element.
                return splited_line[index]

            # We return the extracted line.
            return extracted_domain

        # The extracted line is a comment line.

        # We return an empty string as we do not want to work with commented line.
        return ""

    @classmethod
    def _format_adblock_decoded(cls, to_format, result=None):
        """
        Format the exctracted adblock line before passing it to the system.

        Arguments:
            - to_format: str
                The extracted line from the file.
            - result: None or list
                The list of extracted domain.

        Returns: list
            The list of extracted domains.
        """

        if not result:
            # The result is not given.

            # We set the result as an empty list.
            result = []

        for data in List(to_format).format():
            # We loop through the different lines to format.

            if data:
                # The currently read line is not empty.

                if "^" in data:
                    # There is an accent in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return cls._format_adblock_decoded(data.split("^"), result)

                if "#" in data:
                    # There is a dash in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return cls._format_adblock_decoded(data.split("#"), result)

                if "," in data:
                    # There is a comma in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return cls._format_adblock_decoded(data.split(","), result)

                if "!" in data:
                    # There is an exclamation mark in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return cls._format_adblock_decoded(data.split("!"), result)

                if "|" in data:
                    # There is a vertival bar in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return cls._format_adblock_decoded(data.split("|"), result)

                if data:
                    # * The currently read line is not empty.

                    if Check().is_domain_valid(data) or Check().is_ip_valid(data):
                        # * The currently read line is a valid domain.
                        # or
                        # * The currently read line is a valid IP.

                        # We append the currently read line to the result.
                        result.append(data)
                    else:
                        # * The currently read line is not a valid domain.
                        # or
                        # * The currently read line is not a valid IP.

                        # We try to get the url base.
                        url_base = Check().is_url_valid(data, return_formated=True)

                        if url_base:
                            # The url_base is not empty or equal to False or None.

                            # We appent the url base to the result.
                            result.append(url_base)

        # We return the result element.
        return result

    def _adblock_decode(self, list_to_test):
        """
        Convert the adblock format into a readable format which is understood
        by the system.

        Argument:
            - list_to_test: list
                The read content of the given file.

        Returns: list
            The list of domain to test.
        """

        # We initiate a variable which will save what we are going to return.
        result = []

        # We initiate the first regex we are going to use to get
        # the element to format.
        regex = r"^(?:.*\|\|)([^\/\$\^]{1,}).*$"

        # We initiate the third regex we are going to use to get
        # the element to format.
        regex_v3 = (
            r"(?:#+(?:[a-z]+?)?\[[a-z]+(?:\^|\*)\=(?:\'|\"))(.*\..*)(?:(?:\'|\")\])"
        )

        # We initiate the fourth regex we are going to use to get
        # the element to format.
        regex_v4 = r"^\|(.*\..*)\|$"

        for line in list_to_test:
            # We loop through the different line.

            if (
                line.startswith("!")
                or line.startswith("@@")
                or line.startswith("/")
                or line.startswith("[")
            ):
                continue

            # We extract the different group from our first regex.
            rematch = Regex(
                line, regex, return_data=True, rematch=True, group=0
            ).match()

            # We extract the different group from our fourth regex.
            #
            # Note: We execute the following in second because it is more
            # specific that others.
            rematch_v4 = Regex(
                line, regex_v4, return_data=True, rematch=True, group=0
            ).match()

            # We extract the different group from our third regex.
            rematch_v3 = Regex(
                line, regex_v3, return_data=True, rematch=True, group=0
            ).match()

            if rematch:
                # The first extraction was successfull.

                # We extend the result with the extracted elements.
                result.extend(rematch)

            if rematch_v4:
                # The fourth extraction was successfull.

                # We extend the formated elements from the extracted elements.
                result.extend(List(self._format_adblock_decoded(rematch_v4)).format())

            if rematch_v3:
                # The second extraction was successfull.

                # We extend the formated elements from the extracted elements.
                result.extend(List(self._format_adblock_decoded(rematch_v3)).format())

        # We return the result.
        return result

    @classmethod
    def _extract_domain_from_file(cls):
        """
        This method extract all non commented lines.

        Returns: list
            Each line of the file == an element of the list.
        """

        # We initiate the variable which will save what we are going to return.
        result = []

        if path.isfile(PyFunceble.CONFIGURATION["file_to_test"]):
            # The give file to test exist.

            with open(PyFunceble.CONFIGURATION["file_to_test"]) as file:
                # We open and read the file.

                for line in file:
                    # We loop through each lines.

                    if not line.startswith("#"):
                        # The currently read line is not a commented line.

                        # We append the current read line to the result.
                        result.append(line.rstrip("\n").strip())
        else:
            # The given file to test does not exist.

            # We raise a FileNotFoundError exception.
            raise FileNotFoundError(PyFunceble.CONFIGURATION["file_to_test"])

        # We return the result.
        return result

    def _file_list_to_test_filtering(self):
        """
        This method will unify the way we work before testing file contents.
        """

        # We get the list to test from the file we have to test.
        list_to_test = self._extract_domain_from_file()

        # We get the list of mined.
        mined_list = Mining().list_of_mined()

        if mined_list:
            list_to_test.extend(mined_list)

        # We restore the data from the last session if it does exist.
        AutoContinue().restore()

        if PyFunceble.CONFIGURATION["adblock"]:
            # The adblock decoder is activated.

            # We get the list of domain to test (decoded).
            list_to_test = self._adblock_decode(list_to_test)
        else:
            # The adblock decoder is not activated.

            # We get the formated list of domain to test.
            list_to_test = list(map(self._format_domain, list_to_test))

        # We clean the output directory if it is needed.
        PyFunceble.Clean(list_to_test)

        # We get the list we have to test in the current session (from the database).
        Database().to_test()

        if (
            PyFunceble.CONFIGURATION["file_to_test"]
            in PyFunceble.CONFIGURATION["inactive_db"]
            and "to_test"
            in PyFunceble.CONFIGURATION["inactive_db"][
                PyFunceble.CONFIGURATION["file_to_test"]
            ]
            and PyFunceble.CONFIGURATION["inactive_db"][
                PyFunceble.CONFIGURATION["file_to_test"]
            ]["to_test"]
        ):
            # * The current file to test in into the database.
            # and
            # * The `to_test` index is present into the database
            #   related to the file we are testing.
            # and
            # * The `to_test` index content is not empty.

            # We extend our list to test with the content of the `to_test` index
            # of the current file database.
            list_to_test.extend(
                PyFunceble.CONFIGURATION["inactive_db"][
                    PyFunceble.CONFIGURATION["file_to_test"]
                ]["to_test"]
            )

        # We set a regex of element to delete.
        # Understand with this variable that we don't want to test those.
        regex_delete = r"localhost$|localdomain$|local$|broadcasthost$|0\.0\.0\.0$|allhosts$|allnodes$|allrouters$|localnet$|loopback$|mcastprefix$|ip6-mcastprefix$|ip6-localhost$|ip6-loopback$|ip6-allnodes$|ip6-allrouters$|ip6-localnet$"  # pylint: disable=line-too-long

        # We get the database content.
        database_content = Database().content()

        # We remove the element which are in the database from the
        # current list to test.
        list_to_test = List(
            list(
                set(Regex(list_to_test, regex_delete).not_matching_list())
                - set(database_content)
            )
        ).format()

        if PyFunceble.CONFIGURATION["filter"]:
            # The filter is not empty.

            # We get update our list to test. Indeed we only keep the elements which
            # matches the given filter.
            list_to_test = List(
                Regex(
                    list_to_test, PyFunceble.CONFIGURATION["filter"], escape=True
                ).matching_list()
            ).format()

        list_to_test = List(list(list_to_test)).custom_format(Sort.standard)

        if PyFunceble.CONFIGURATION["hierarchical_sorting"]:
            # The hierarchical sorting is desired by the user.

            # We format the list.
            list_to_test = List(list(list_to_test)).custom_format(Sort.hierarchical)

        # We generate the directory structure.
        DirectoryStructure()

        # We update the status of the file testing.
        PyFunceble.CONFIGURATION["file_testing"] = False

        # We return the final list to test.
        return list_to_test

    def file(self):
        """
        Manage the case that need to test each domain of a given file path.
        Note: 1 domain per line.
        """

        # We get, format, filter, clean the list to test.
        list_to_test = self._file_list_to_test_filtering()

        if PyFunceble.CONFIGURATION["idna_conversion"]:
            # We have to convert domains to idna.

            # We convert if we need to convert.
            list_to_test = domain2idna(list_to_test)

            if PyFunceble.CONFIGURATION["hierarchical_sorting"]:
                # The hierarchical sorting is desired by the user.

                # We format the list.
                list_to_test = List(list_to_test).custom_format(Sort.hierarchical)
            else:
                # The hierarchical sorting is not desired by the user.

                # We format the list.
                list_to_test = List(list_to_test).custom_format(Sort.standard)

        # We test each element of the list to test.
        list(
            map(
                self.domain,
                list_to_test[PyFunceble.CONFIGURATION["counter"]["number"]["tested"] :],
                repeat(list_to_test[-1]),
            )
        )

    def url(self, url_to_test=None, last_url=None):
        """
        Manage the case that we want to test only a given url.

        Arguments:
            - url_to_test: str
                The url to test.
            - last_url: str
                The last url of the file we are testing.
        """

        # We print the header.
        self._print_header()

        if url_to_test:
            # An url to test is given.

            # We set the url we are going to test.
            PyFunceble.CONFIGURATION["URL"] = url_to_test
        else:
            # An URL to test is not given.

            # We set the url we are going to test to None.
            PyFunceble.CONFIGURATION["URL"] = None

        if PyFunceble.CONFIGURATION["URL"]:
            # An URL to test is given.

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the URL informations.
                print(PyFunceble.CONFIGURATION["URL"], URL().get())
            else:
                # The simple mode is not activated.

                # We get the status of the URL.
                status = URL().get()

            # We run the file decision logic.
            self._file_decision(url_to_test, last_url, status)

    def file_url(self):
        """
        Manage the case that we have to test a file
        Note: 1 URL per line.
        """

        # We get, format, clean the list of URL to test.
        list_to_test = self._file_list_to_test_filtering()

        # We test each URL from the list to test.
        list(
            map(
                self.url,
                list_to_test[PyFunceble.CONFIGURATION["counter"]["number"]["tested"] :],
                repeat(list_to_test[-1]),
            )
        )

    @classmethod
    def switch(
        cls, variable, custom=False
    ):  # pylint: disable=inconsistent-return-statements
        """
        Switch PyFunceble.CONFIGURATION variables to their opposite.

        Arguments:
            - variable: str
                The PyFunceble.CONFIGURATION[variable_name] to switch.
            - custom: bool
                Tell the system if we want to switch a specific variable different
                from PyFunceble.CONFIGURATION

        Returns: bool
            The opposite of the installed value of Settings.variable_name.

        Raise:
            - Exception: When the configuration is not valid. In other words,
                if the PyFunceble.CONFIGURATION[variable_name] is not a bool.
        """

        if not custom:
            # We are not working with custom variable which is not into
            # the configuration.

            # We get the current state.
            current_state = dict.get(PyFunceble.CONFIGURATION, variable)
        else:
            # We are working with a custom variable which is not into the
            # configuration
            current_state = variable

        if isinstance(current_state, bool):
            # The current state is a boolean.

            if current_state:
                # The current state is equal to True.

                # We return False.
                return False

            # The current state is equal to False.

            # We return True.
            return True

        # The current state is not a boolean.

        # We set the message to raise.
        to_print = "Impossible to switch %s. Please post an issue to %s"

        # We raise an exception inviting the user to report an issue.
        raise Exception(
            to_print % (repr(variable), PyFunceble.LINKS["repo"] + "/issues.")
        )
