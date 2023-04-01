from dataclasses import dataclass

from llm_strategy import llm_function
from llm_strategy.testing.fake_llm import FakeLLM


def test_llm_function_add_two_ints():
    def add_two_ints(a: int, b: int) -> int:
        """Add two integers."""
        raise NotImplementedError

    def add_two_ints_with_default(a: int, b: int = 1) -> int:
        """Add two integers with a default value."""
        raise NotImplementedError

    def add_two_ints_with_default_and_kwarg(*, a: int, c: int = 2) -> int:
        """Add two integers with a default value."""
        raise NotImplementedError

    llm = FakeLLM(
        texts={
            (
                'Add two integers.\nThe inputs are formatted as JSON using the following schema:\n```\n{"properties":'
                ' {"a": {"title": "A", "type": "integer"}, "b": {"title": "B", "type": "integer"}}, "required": ["a",'
                ' "b"]}\n```\n\nThe output should be formatted as a JSON instance that conforms to the JSON schema'
                ' below.\n\nAs an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a'
                ' list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}}\nthe object'
                ' {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo":'
                ' ["bar", "baz"]}} is not well-formatted.\n\nHere is the output schema:\n```\n{"properties":'
                ' {"return_value": {"title": "Return Value", "type": "integer"}}, "required":'
                ' ["return_value"]}\n```\nNow output the results for the following inputs:\n```\n{"a": 1, "b":'
                ' 2}\n```\n{"return_value": 3}'
            ),
            (
                "Add two integers with a default value.\nThe inputs are formatted as JSON using the following"
                ' schema:\n```\n{"properties": {"a": {"title": "A", "type": "integer"}, "b": {"title": "B", "default":'
                ' 1, "type": "integer"}}, "required": ["a"]}\n```\n\nThe output should be formatted as a JSON instance'
                ' that conforms to the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo":'
                ' {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}},'
                ' "required": ["foo"]}}\nthe object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema.'
                ' The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.\n\nHere is the output'
                ' schema:\n```\n{"properties": {"return_value": {"title": "Return Value", "type": "integer"}},'
                ' "required": ["return_value"]}\n```\nNow output the results for the following inputs:\n```\n{"a": 1,'
                ' "b": 1}\n```\n{"return_value": 2}'
            ),
            (
                "Add two integers with a default value.\nThe inputs are formatted as JSON using the following"
                ' schema:\n```\n{"properties": {"a": {"title": "A", "type": "integer"}, "c": {"title": "C", "default":'
                ' 2, "type": "integer"}}, "required": ["a"]}\n```\n\nThe output should be formatted as a JSON instance'
                ' that conforms to the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo":'
                ' {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}},'
                ' "required": ["foo"]}}\nthe object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema.'
                ' The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.\n\nHere is the output'
                ' schema:\n```\n{"properties": {"return_value": {"title": "Return Value", "type": "integer"}},'
                ' "required": ["return_value"]}\n```\nNow output the results for the following inputs:\n```\n{"a": 1,'
                ' "c": 2}\n```\n{"return_value": 3}'
            ),
        },
        # external_llm=OpenAI(),
    )

    assert llm_function(llm)(add_two_ints)(1, 2) == 3
    assert llm_function(llm)(add_two_ints_with_default)(1) == 2
    assert llm_function(llm)(add_two_ints_with_default_and_kwarg)(a=1) == 3


@dataclass
class Foo:
    a: int
    b: int

    @property
    def c(self: "Foo") -> int:
        """Add the two integer fields self.a and self.b."""
        raise NotImplementedError


def test_llm_function_property():
    llm = FakeLLM(
        texts={
            "Add the two integer fields self.a and self.b.\nThe inputs are formatted as JSON using the following"
            ' schema:\n```\n{"properties": {"self": {"$ref": "#/definitions/Foo"}}, "required": ["self"],'
            ' "definitions": {"Foo": {"title": "Foo", "type": "object", "properties": {"a": {"title": "A", "type":'
            ' "integer"}, "b": {"title": "B", "type": "integer"}}, "required": ["a", "b"]}}}\n```\n\nThe output should'
            " be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema"
            ' {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items":'
            ' {"type": "string"}}}, "required": ["foo"]}}\nthe object {"foo": ["bar", "baz"]} is a well-formatted'
            ' instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.\n\nHere'
            ' is the output schema:\n```\n{"properties": {"return_value": {"title": "Return Value", "type":'
            ' "integer"}}, "required": ["return_value"]}\n```\nNow output the results for the following'
            ' inputs:\n```\n{"self": {"a": 1, "b": 2}}\n```\n{"return_value": 3}'
        },
        # external_llm=OpenAI()
    )
    Foo.c = llm_function(llm)(Foo.c)
    assert Foo(1, 2).c == 3
