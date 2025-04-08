from xcvr_emu.cli import Context, Command

from prompt_toolkit.completion import WordCompleter

import pytest


@pytest.fixture
def cmdClass():
    class A(Command):
        def exec(self, line):
            return line

        def arguments(self):
            return ["Ethernet1_1", "Ethernet2_1"]

    class Test(Context):
        def __init__(self, fuzzy):
            super().__init__(None, fuzzy)

            @self.command(WordCompleter(["a", "aaa", "b", "bbb"], sentence=True))
            def test(line):
                pass

            @self.command(WordCompleter(["c", "cc", "b", "bbb2"], sentence=True))
            def test2(line):
                pass

            self.add_command("a", A)

    return Test


def test_basic_help(cmdClass: type):
    t = cmdClass(False)  # no fuzzy completion
    assert t.help("") == "quit, exit, test, test2, a"
    assert t.help("t") == "test, test2"
    assert t.help("t ") == ""
    assert t.help("test") == "test, test2"
    assert t.help("test ") == "a, aaa, b, bbb"
    assert t.help("test a") == "a, aaa"
    assert t.help("test a ") == ""
    assert t.help("test2") == "test2"
    assert t.help("test2 ") == "c, cc, b, bbb2"
    assert t.help("test2 b") == "b, bbb2"
    assert t.help("tes b") == ""
    assert t.help("2 b") == ""
    assert t.help("a") == "a"
    assert t.help("a ") == "Ethernet1_1, Ethernet2_1"
    assert (
        t.help("a 2") == "Ethernet1_1, Ethernet2_1"
    )  # help show candidates when no match
    assert t.exec("a Ethernet1_1 B C", no_fail=False) == ["Ethernet1_1", "B", "C"]


def test_fuzzy_help(cmdClass: type):
    t = cmdClass(True)  # fuzzy completion
    assert t.help("") == "quit, exit, test, test2, a"
    assert t.help("t") == "test, test2"
    assert t.help("es") == "test, test2"
    assert t.help("te") == "test, test2"
    assert t.help("2") == "test2"
    assert t.help("test2 b") == "b, bbb2"
    assert t.help("test2 2") == "bbb2"
    assert t.help("a 2") == "Ethernet2_1"  # help show candidates when no match
    assert t.exec("a 2 B C", no_fail=False) == ["Ethernet2_1", "B", "C"]
