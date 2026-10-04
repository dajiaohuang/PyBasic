#! /usr/bin/python

# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import contextlib
import io
import unittest

from lexer import Lexer
from program import Program


class ProgramRegressionTests(unittest.TestCase):
    def test_replacing_data_statement_removes_data(self):
        lexer = Lexer()
        program = Program()
        program.add_stmt(lexer.tokenize("10 DATA 42"))
        program.add_stmt(lexer.tokenize("20 READ A"))
        program.add_stmt(lexer.tokenize("30 PRINT A"))

        program.add_stmt(lexer.tokenize("10 PRINT 0"))

        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, r"\? OUT OF DATA in line 20"):
                program.execute()

    def test_conditional_jump_inside_while_preserves_loop_frame(self):
        lexer = Lexer()
        program = Program()
        for statement in (
            "10 LET I=0",
            "20 WHILE I<2",
            "30 LET I=I+1",
            "40 IF I=1 THEN 30",
            "50 WEND",
            "60 PRINT I",
        ):
            program.add_stmt(lexer.tokenize(statement))

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            program.execute()

        self.assertEqual(output.getvalue().strip(), "2")


if __name__ == "__main__":
    unittest.main()
