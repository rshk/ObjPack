# ObjPack

ObjPack is a serialization format for objects.
It is a superset of JSON, meant to extend functionality in order
to allow some nicer features.

## Example

Ever wanted to put comments in JSON? Now you can!

```python
{

# Database configuration goes here
'database': 'postgresql://user:pass@host/dbname',

# This is your email address
'email_from': 'foo@bar.baz',
'email_password': 'spam-eggs-spam',  # hide this!

}
```

Do you hate this kind of syntax, when using JSON as DSL?

```json
{"or": [
    {"cond1": "value1"},
    {"cond1": "whatever"}
]}
```

Now, it can be rewritten in a nicer way!

```python
OR(
    {'cond1': 'value1'},
    {'cond1': 'whatever'})
```

You can have objects, like this:

```python
MyObject('hello', 'world')
```

and, they support keyword arguments too!

```python
MyObject('hello', 'world', example=1, another='blah')
```

you can also put kwargs in front, for example, to define
some {xml,html}-like syntax!

```python
Html(
	Head(
		Title("This is a title"),
		Link(rel='stylesheet', type='text/css', href='style.css')
	),
	Body(
		H1("The main headline"),
		Table(
			class="nice-table",
			Tr(Td("One"), Td("Two"), Td("Three")),
			Tr(Td("One2"), Td("Two2"), Td("Three2")),
			Tr(Td("One3"), Td("Two3"), Td("Three3"))
		)
	)
)
```


## Build status

[![Build Status](https://travis-ci.org/rshk/ObjPack.png)](https://travis-ci.org/rshk/ObjPack)
