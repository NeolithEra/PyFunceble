# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.helpers.dict

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io///en/master/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

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

from unittest import TestCase
from unittest import main as launch_tests

from PyFunceble.helpers import Dict, File


class TestDict(TestCase):
    """
    Tests of PyFunceble.helpers.dict.
    """

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.test_subject = {
            "Hello": "world",
            "World": {"world": "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
        }

    def test_has_same_keys_as(self):
        """
        Tests the method which let us know if the keys of
        2 dicts are the same.
        """

        # This is a.
        origin = {"a": 1, "b": 1}

        # This is b.
        target = {"a": 1, "b": 2, "c": {"a": 1, "b": 3, "c": {"x": "x"}}}

        # We want to test that all keys of a are into b.
        self.assertEqual(True, Dict(target).has_same_keys_as(origin))
        # We want to test that all keys of b are into a.
        self.assertEqual(False, Dict(origin).has_same_keys_as(target))

        origin["c"] = {"a": 1, "b": 3, "c": {"x": "x"}}

        # We want to test that all keys of a are in b.
        self.assertEqual(True, Dict(target).has_same_keys_as(origin))
        # We want to test that all keys of b are in a.
        self.assertEqual(True, Dict(origin).has_same_keys_as(target))

        del origin["c"]["c"]
        # We want to test that all keys of b are in a.
        self.assertEqual(False, Dict(origin).has_same_keys_as(target))

    def test_remove_key_not_dict(self):
        """
        Tests the method which let us remove a key for the case
        that the given subject is not a dict.
        """

        expected = None
        actual = Dict(["Hello", "World!"]).remove_key("Py")

        self.assertEqual(expected, actual)

    def test_remove_key(self):
        """
        Tests the method which let us remove a key.
        """

        expected = {
            "Hello": "world",
            "World": {"world": "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "pyfunceble": ["funilrys"],
        }

        actual = Dict(self.test_subject).remove_key("Py")

        self.assertEqual(expected, actual)

        actual = Dict(self.test_subject).remove_key(["Py", "test"])

        self.assertEqual(expected, actual)

    def test_remove_multiple_key(self):
        """
        Tests the method which let us remove a key with
        multiple key to remove.
        """

        expected = {
            "Hello": "world",
            "World": {"world": "hello"},
            "pyfunceble": ["funilrys"],
        }

        actual = Dict(self.test_subject).remove_key(["funilrys", "Py"])

        self.assertEqual(expected, actual)

    def test_remove_key_not_found(self):
        """
        Tests the method which let us remove a key for the case
        that the given key to remove does not exists.
        """

        expected = {
            "Hello": "world",
            "World": {"world": "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
        }

        actual = Dict(self.test_subject).remove_key("xxx")

        self.assertEqual(expected, actual)

    def test_rename_key_not_dict(self):
        """
        Tests the method which let us rename a key for the case
        that the given subject is not a dict.
        """

        expected = None
        actual = Dict(["Hello", "World!"]).rename_key({"Fun": "Ilrys"})

        self.assertEqual(expected, actual)

    def test_rename_key_strict_single(self):
        """
        Tests the method which let us rename a key for the case
        that we only want to strictly rename one key.
        """

        expected = {
            "Hello": "world",
            "World": {"world": "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "PyFunceble": "Funceble",
            "pyfunceble": ["funilrys"],
        }

        actual = Dict(self.test_subject).rename_key({"Py": "PyFunceble"})

        self.assertEqual(expected, actual)

    def test_rename_key_non_strict_single(self):
        """
        Tests the method which let us rename a key for the case
        that we only want to rename all occurences of the given
        key-string.
        """

        expected = {
            "Hello": "world",
            "World": {"world": "hello"},
            "nuilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "nuceble": ["funilrys"],
        }
        actual = Dict(self.test_subject).rename_key({"fun": "nuf"}, strict=False)

        self.assertEqual(expected, actual)

    def test_to_json_file_non_dict(self):
        """
        Tests the method which let us save a dict into a JSON file
        for the case that we don't given a dict.
        """

        output_file = "this_file_is_a_ghost"
        File(output_file).delete()

        self.assertRaises(TypeError, lambda: Dict(1).to_json_file(output_file))
        self.assertRaises(TypeError, lambda: Dict("100").to_json_file(output_file))
        self.assertRaises(
            TypeError, lambda: Dict("{'hello': 'world'}").to_json_file(output_file)
        )

        File(output_file).delete()

    def test_to_json_file(self):
        """
        Tests the method which let us save and load
        a dict into/from a JSON file.
        """

        output_file = "this_file_is_a_ghost"
        File(output_file).delete()

        Dict(self.test_subject.copy()).to_json_file(output_file)

        expected = self.test_subject.copy()

        actual = Dict().from_json_file(output_file)

        self.assertEqual(expected, actual)

        File(output_file).delete()

    def test_to_json(self):
        """
        Tests the method which let us get the JSON
        representation of the given dict.
        """

        expected = """{
    "Hello": "world",
    "Py": "Funceble",
    "World": {
        "world": "hello"
    },
    "funilrys": [
        "Fun",
        "Ilrys"
    ],
    "pyfunceble": [
        "funilrys"
    ]
}"""
        actual = Dict(self.test_subject.copy()).to_json()

        self.assertEqual(expected, actual)

        actual = Dict().from_json(expected)
        expected = self.test_subject.copy()

        self.assertEqual(expected, actual)

    def test_to_yaml_file_non_dict(self):
        """
        Tests the method which let us save a dict into a YAML file
        for the case that we don't given a dict.
        """

        output_file = "this_file_is_a_ghost"
        File(output_file).delete()

        self.assertRaises(TypeError, lambda: Dict(1).to_yaml_file(output_file))
        self.assertRaises(TypeError, lambda: Dict("100").to_yaml_file(output_file))
        self.assertRaises(
            TypeError, lambda: Dict("{'hello': 'world'}").to_yaml_file(output_file)
        )

        File(output_file).delete()

    def test_to_yaml_file(self):
        """
        Tests the method which let us save and load
        a dict into/from a YAML file.
        """

        output_file = "this_file_is_a_ghost"
        File(output_file).delete()

        Dict(self.test_subject.copy()).to_yaml_file(output_file)

        expected = self.test_subject.copy()

        actual = Dict().from_yaml_file(output_file)

        self.assertEqual(expected, actual)

        File(output_file).delete()

    def test_to_yaml(self):
        """
        Tests the method which let us get the YAML
        representation of the given dict.
        """

        expected = """Hello: world
Py: Funceble
World:
    world: hello
funilrys:
- Fun
- Ilrys
pyfunceble:
- funilrys
"""
        actual = Dict(self.test_subject.copy()).to_yaml()

        self.assertEqual(expected, actual, repr(actual))

        actual = Dict().from_yaml(expected)
        expected = self.test_subject.copy()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
