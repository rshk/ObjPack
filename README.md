# ObjPack

ObjPack is a serialization format for objects.
It is a superset of JSON, meant to extend functionality in order
to allow some nicer features.

----------

**Warning:** this thing is still **very experimental** and
**not fully implemented yet**, (eg. serialization is missing)
so it should be quite obvious that it is
**not ready to be used in production** at all.

Please have a look, play with it, send feedback and try to
pinpoint bugs by writing test cases :)

----------


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

## TodoList (contributions welcome)

* Write the serialization part (+ tests)
* Make the Node interface more user-friendly (implement ``__getitem__`` etc.
  to access children -- how to access attributes?)
* Finish structuring the syntax (eg. string escapes are missing)
* Write down some RFC about the syntax (how do you write a proper rfc?)
* Write nice documentation about the syntax (see above)
* Port to other languages too :)


## Build status

[![Build Status](https://travis-ci.org/rshk/ObjPack.png)](https://travis-ci.org/rshk/ObjPack)
