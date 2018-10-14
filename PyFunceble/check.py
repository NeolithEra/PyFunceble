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

This submodule will provide a checking interface.

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

import PyFunceble
from PyFunceble.helpers import Regex
from PyFunceble.publicsuffix import PublicSuffix


class Check:
    """
    This class provide some method to check several things around URL, IP or domain format.

    Argument:
        - element: str
            The element to check.
    """

    def __init__(self, element=None):
        self.element = element

        try:
            PyFunceble.CONFIGURATION["psl_db"]
        except KeyError:
            PublicSuffix(False).load()

    def is_url_valid(self, url=None, return_formated=False):
        """
        Check if the domain of the given URL is valid.

        Argument:
            - url: str
                The url to validate.
            - return_formated: bool
                True: We return the url base.

        Returns: bool|str
            - True: is valid.
            - False: is invalid.
            - str: return_formated is true and the url base is valid.
        """

        if url:
            # The given url is not empty.

            # We initiate the element to test.
            to_test = url
        elif self.element:
            # The globaly given url is not empty.

            # We initiate the element to test.
            to_test = self.element
        else:
            # The given url is empty.

            # We initiate the element to test from the globaly URl to test.
            to_test = PyFunceble.CONFIGURATION["URL"]

        if to_test.startswith("http"):
            # The element to test starts with http.

            try:
                # We initiate a regex which will match the domain or the url base.
                regex = r"(^(http:\/\/|https:\/\/)(.+?(?=\/)|.+?$))"

                # We extract the url base with the help of the initiated regex.
                formated_base = Regex(
                    to_test, regex, return_data=True, rematch=True
                ).match()[2]

                # We check if the url base is a valid domain.
                domain_status = self.is_domain_valid(formated_base)

                # We check if the url base is a valid IP.
                ip_status = self.is_ip_valid(formated_base)

                if domain_status or ip_status:
                    # * The url base is a valid domain.
                    # and
                    # * The url base is a valid IP.

                    if return_formated:
                        return formated_base

                    # We return True.
                    return True
            except TypeError:
                pass

        # We return False.
        return False

    def is_domain_valid(self, domain=None):
        """
        Check if PyFunceble.CONFIGURATION['domain'] is a valid domain.

        Argument:
            - domain: str
                The domain to validate.

        Returns: bool
            - True: is valid.
            - False: is invalid.
        """

        # We initate our regex which will match for valid domains.
        regex_valid_domains = r"^(?=.{0,253}$)(([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9])\.)+((?=.*[^0-9])([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9]))$"  # pylint: disable=line-too-long

        # We initiate our regex which will match for valid subdomains.
        regex_valid_subdomains = r"^(?=.{0,253}$)(([a-z0-9_][a-z0-9-_]{0,61}[a-z0-9_-]|[a-z0-9])\.)+((?=.*[^0-9])([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9]))$"  # pylint: disable=line-too-long

        if domain:
            # A domain is given.

            # We set the element to test as the parsed domain.
            to_test = domain
        elif self.element:
            # A domain is globally given.

            # We set the globally parsed domain.
            to_test = self.element
        else:
            # A domain is not given.

            # We set the element to test as the currently tested element.
            to_test = PyFunceble.CONFIGURATION["domain"]

        if Regex(to_test, regex_valid_domains, return_data=False).match():
            # The element pass the domain validation.

            # We return True. The domain is valid.
            return True

        # The element did not pass the domain validation. That means that it has invalid character
        # or the position of - or _ are not right.

        try:
            # We get the position of the last point.
            last_point_index = to_test.rindex(".")
            # And with the help of the position of the last point, we get the domain extension.
            extension = to_test[last_point_index + 1 :]

            if extension in PyFunceble.CONFIGURATION["psl_db"]:
                # The extension is into the psl database.

                for suffix in PyFunceble.CONFIGURATION["psl_db"][extension]:
                    # We loop through the element of the extension into the psl database.

                    try:
                        # We try to get the position of the currently read suffix
                        # in the element ot test.
                        suffix_index = to_test.rindex("." + suffix)

                        # We get the element to check.
                        # The idea here is to delete the suffix, then retest with our
                        # subdomains regex.
                        to_check = to_test[:suffix_index]

                        if "." in to_check:
                            # There is a point into the new element to check.

                            # We check if it passes our subdomain regex.
                            # * True: It's a valid domain.
                            # * False: It's an invalid domain.
                            return Regex(
                                to_check, regex_valid_subdomains, return_data=False
                            ).match()

                    except ValueError:
                        # In case of a value error because the position is not found,
                        # we continue to the next element.
                        pass

            # * The extension is not into the psl database.
            # or
            # * there was no point into the suffix checking.

            # We get the element before the last point.
            to_check = to_test[:last_point_index]

            if "." in to_check:
                # There is a point in to_check

                # We check if it passes our subdomain regex.
                # * True: It's a valid domain.
                # * False: It's an invalid domain.
                return Regex(
                    to_check, regex_valid_subdomains, return_data=False
                ).match()

        except (ValueError, AttributeError):
            # In case of a value or attribute error we ignore them.
            pass

        # And we return False, the domain is not valid.
        return False

    def is_ip_valid(self, ip_to_check=None):
        """
        Check if PyFunceble.CONFIGURATION['domain'] is a valid IPv4.

        Argument:
            - ip_to_check: str
                The ip to test

        Note:
            We only test IPv4 because for now we only support domain and IPv4.

        Returns: bool
            - True: is valid.
            - False: is invalid.
        """

        # We initate our regex which will match for valid IPv4.
        regex_ipv4 = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,})$"  # pylint: disable=line-too-long

        if ip_to_check:
            # An element is localy given.

            # We consider it as the element to test.
            to_test = ip_to_check
        elif self.element:
            # An element is given globally.

            # We consider it as the element to test.
            to_test = self.element
        else:
            # An element is not localy given.

            # We consider the global element to test as the element to test.
            to_test = PyFunceble.CONFIGURATION["domain"]

        # We check if it passes our IPv4 regex.
        # * True: It's a valid IPv4.
        # * False: It's an invalid IPv4.
        return Regex(to_test, regex_ipv4, return_data=False).match()