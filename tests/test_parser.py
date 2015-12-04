from kermit.ast import (
    Stmt, Block, ConstantInt, ConstantFloat, Function, Call,
    ConstantString, BinOp, Variable, Assignment, While, If, Print
)

from kermit.parser import parse


def test_parse_basic():
    assert parse('13;') == Block([Stmt(ConstantInt(13))])
    assert parse('1 + 2;') == Block([Stmt(BinOp("+", ConstantInt(1),
                                                ConstantInt(2)))])
    assert parse('1 + a;') == Block([Stmt(BinOp('+', ConstantInt(1),
                                                Variable('a')))])


def test_float():
    assert parse('1.0;') == Block([Stmt(ConstantFloat(1.0))])
    assert parse('0.5;') == Block([Stmt(ConstantFloat(0.5))])
    assert parse('0.0;') == Block([Stmt(ConstantFloat(0.0))])
    assert parse('-1.0;') == Block([Stmt(ConstantFloat(-1.0))])
    assert parse('10.0;') == Block([Stmt(ConstantFloat(10.0))])
    assert parse('.1;') == Block([Stmt(ConstantFloat(.1))])
    assert parse('1.0e5;') == Block([Stmt(ConstantFloat(1.0e5))])
    assert parse('1.0E-5;') == Block([Stmt(ConstantFloat(1.0E-5))])
    assert parse('1.0e+11;') == Block([Stmt(ConstantFloat(1.0e11))])


def test_string():
    assert parse('"foo";') == Block([Stmt(ConstantString("foo"))])
    assert parse('"foo" + "bar";') == Block(
        [
            Stmt(
                BinOp(
                    "+",
                    ConstantString("foo"),
                    ConstantString("bar")
                )
            )
        ]
    )


def test_multiple_statements():
    assert parse('''
    1 + 2;
    c;
    e;
    ''') == Block([Stmt(BinOp("+", ConstantInt(1), ConstantInt(2))),
                   Stmt(Variable('c')),
                   Stmt(Variable('e'))])


def test_assignment():
    assert parse('a = 3;') == Block([Assignment('a', ConstantInt(3))])


def test_while():
    assert parse('while (1) { a = 3; }') == Block(
        [While(ConstantInt(1), Block([Assignment('a', ConstantInt(3))]))])


def test_if():
    assert parse("if (1) { a; }") == Block([If(ConstantInt(1),
                                               Block([Stmt(Variable("a"))]))])


def test_func_decl():
    assert parse("func foo() { print 1; }") == Block([
        Function("foo", Block([
            Print(ConstantInt(1))
        ]))
    ])


def test_func_call():
    assert parse("foo();") == Block([Stmt(Call(Variable("foo")))])


def test_print():
    assert parse("print x;") == Block([Print(Variable("x"))])
