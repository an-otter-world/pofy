# Pofy (Python yaml objects)

[![WTFPL license](https://img.shields.io/badge/License-WTFPL-blue.svg)](https://raw.githubusercontent.com/an-otter-world/pofy/master/COPYING)
[![Actions Status](https://github.com/an-otter-world/pofy/workflows/Checks/badge.svg)](https://github.com/an-otter-world/pofy/actions)
[![Coverage Status](https://coveralls.io/repos/github/an-otter-world/pofy/badge.svg)](https://coveralls.io/github/an-otter-world/pofy)
[![Matrix](https://img.shields.io/matrix/python-pofy:matrix.org?server_fqdn=matrix.org)](https://matrix.to/#/!SwCyFpSTQTLiPCNKTO:matrix.org?via=matrix.org)

Pofy is a tiny library allowing to declare classes that can be deserialized
from YAML, using pyyaml. Classes declares a schema as a list of fields, used
to validate data during deserialization. Features include YAML inclusion,
custom fields & validation.

Pofy is distributed under the term of the WTFPL V2 (See COPYING file).

Contribution are very welcome. Don't hesitate to send pull requests. As English
isn't my native language, I'd be very happy with documentation correction or
improvements. Feel free to join [the Pofy channel on Matrix](https://matrix.to/#/!SwCyFpSTQTLiPCNKTO:matrix.org?via=matrix.org).

- [Pofy (Python yaml objects)](#pofy-python-yaml-objects)
  - [Installation](#installation)
  - [Quickstart](#quickstart)
  - [Reference](#reference)
    - [Fields](#fields)
      - [Common Parameters](#common-parameters)
      - [BoolField](#boolfield)
      - [StringField](#stringfield)
      - [IntField](#intfield)
      - [FloatField](#floatfield)
      - [EnumField](#enumfield)
      - [PathField](#pathfield)
      - [ListField](#listfield)
      - [DictField](#dictfield)
      - [ObjectField](#objectfield)
    - [Tag Handlers](#tag-handlers)
      - [env](#env)
      - [glob](#glob)
      - [import / try-import](#import--try-import)
    - [Hooks](#hooks)
      - [Field validation](#field-validation)
      - [Oject validation](#oject-validation)
      - [Post-load hook](#post-load-hook)
      - [Error handling](#error-handling)
    - [Creating Custom Fields](#creating-custom-fields)

## Installation

Pofy is tested with Python 3.8. It be installed through pip :

  `pip install pofy`

## Quickstart

To use Pofy, you must declare a schema in the class you want to deserialize :

  ```python
      from pofy import StringField, load

      class Test:
          class Schema:
              field = StringField()

      test = load(SomeObject, 'field: value')
      assert test.field == 'value`
  ```

## Reference

### Fields

Pofy fields are defined in a 'Schema' inner class of the object you want to
deserialize. Pofy comes with predefined fields described below. You can
declare custom fields, to do so, refer to the [Custom Fields][#custom-fields]
section.

#### Common Parameters

All field types accept a 'required' boolean parameter. If it's set and the
field is not declared when loading a YAML document, a
MissingRequiredFieldError will be raised, or the [error handler](#error-handler)
you defined will be called with ErrorCode.MISSING_REQUIRED_FIELD as the
error_code parameter :

```python
  from pofy import StringField, load

  class Test:
    class Schema:
      required_field = StringField(required=True)
      optional_field = StringField()

  load('optional_field: some_value', Test) # Raises MissingRequiredFieldError
```

All field types accept a 'validate' parameter. It's meant to be a python
callable object accepting a ILoadingContext and the field deserialized
object, and returning a boolean. If the returned value is False, pofy will
raise a ValidationError or the [error handler](#error-handler) you defined will
be called with ErrorCode.VALIDATION_ERROR as the error_code parameter. Notice
that whole loaded objects can also be validated.

```python
  from pofy import StringField, load

  def _validate(context, value):
    if value not in ['red', 'green', 'blue']:
      return False

    return True

  class Test:
    class Schema:
      color = StringField()

  load('color: yellow', Test) # Raises ValidationError
  load('color: blue', Test) # Raises ValidationError
```

#### BoolField

BoolField loads a boolean from YAML. No additional parameter is available. The following values are accepted when loading a YAML object :

- For true : y, Y, yes, Yes, YES, true, True, TRUE, on, On, ON
- For false : n, N, no, No, NO, false, False, FALSE, off, Off, OFF

Any other value will raise a ValidationError, or call the defined error_handler
with VALIDATION_ERROR as the error_code parameter.

```python
  from pofy import BoolField, load

  class Test:
    class Schema:
      some_flag = BoolField()

  test = load('some_flag: on', Test)
  assert test.some_flag
  test = load('some_flag: NotValid', Test) # Raises ValidationError
```

#### StringField

StringField loads a string from YAML. The field constructor accept a 'pattern'
parameter, that is meant to be a regular expression that deserialized values
should match. If pattern is defined and the deserialized values doesn't match
it, a ValidationError will be raised or the [error handler](#error-handler) you
defined will be called with ErrorCode.VALIDATION_ERROR as the error_code
parameter.

```python
  from pofy import StringField, load

  class Test:
    class Schema:
      string_field = StringField()
      pattern_field = StringField(pattern='[0-9]*')

  test = load('string_field: "foo bar"', Test)
  assert test.string_field == 'foo bar'
  test = load('pattern_field: NotValid', Test) # Raises ValidationError
  test = load('pattern_field: 10', Test)
  assert test.pattern_field == '10'
```

#### IntField

IntField loads an int from YAML. In addition to the common fields parameters,
it accept several parameters :

- base: An integer, giving the base to use when loading the integer. IntField
  uses the int(...) python function to get the integer, so even without this
  parameter, hexadecimal and octal notation are taken into account. Use this
  parameter if you don't want to have the 0x or 0o prefix in front of the
  number, or if you want to use an exotic base.
- minumum, maximum : Acceptable boundaries for the loaded value. If the value
  is out of bounds, a ValidationError will be raised, or the defined
  error_handler will be called with ErrorCode.VALIDATION_ERROR as the error_code
  parameter.

```python
  from pofy import IntField, load

  class Test:
    class Schema:
      int_field = IntField(minimum=0, maximum=16)
      hex_field = IntField(base=16)

  assert load('int_field: 10', Test).int_field == 10
  assert load('int_field: 0xF', Test).int_field == 15
  assert load('int_field: 0o12', Test).int_field == 12
  assert load('int_field: 100', Test) # Raises ValidationError
  assert load('hex_field: F', Test).hex_field == 15
```

#### FloatField

Float Field loads a float from YAML. In addition to the common fields
parameters, it accept several specific ones :

- minumum, maximum : Acceptable boundaries for the loaded value. If the value
  is out of bounds, a ValidationError will be raised, or the defined
  error_handler will be called with ErrorCode.VALIDATION_ERROR as the error_code
  parameter.

```python
  from pofy import FloatField, load

  class Test:
    class Schema:
      float_field = FloatField(minimum=.0, maximum=10.0)

  assert load('float_field: 10.0', Test).float_field == 10
  assert load('int_field: 100.0', Test) # Raises ValidationError
```

#### EnumField

#### PathField

#### ListField

#### DictField

#### ObjectField

### Tag Handlers

Pofy allows you to plug custom deserialization behavior when encountering yaml
tags. These custom behaviors are called tag handlers. Pofy comes with some
predefined tag handlers, described below. Custom tag handlers are defined the
following way :

```python
from pofy import TagHandler
from pofy import ILoadingContext
from pofy import IBaseField

class ReverseHandler(TagHandler):
    tag_pattern = '^reverse$' # Regex pattern that this tag handler matches

    def load(self, context: ILoadingContext, field: IBaseField) \
            -> Any:
        # Check that the type of the node is correct, and fail if not :
        if not context.expect_scalar(
            _('!reverse must be set on a string node.')
        ):
            return UNDEFINED

        # Return the value of the current yaml node reversed.
        node = context.current_node()
        return node.value.reverse()
```

Check the API reference to see the methods available on ILoadingContext, 
containing the current YAML document loading state, and IBaseField,
representing the currently deserialized field.

To use it, the handler should be passed to the pofy 'load' methods through the
'tag_handlers' arguments :

```python

  class Test:
    class Schema:
      string_field = StringField()

  test = load(
    'string_field: !reverse Hello world',
    Test,
    tag_handlers=[ReverseHandler()]
  )
  assert test.string_field == 'dlrow olleH'
```

Pofy comes with some predefined tag handlers that are automatically registered
when calling load, so the following tags are usable out of the box :

#### env

#### glob

#### import / try-import

The import and try import tags allows to import another YAML file as a field of
the currently deserialized object :

### Hooks

#### Field validation

#### Oject validation

#### Post-load hook

#### Error handling

### Creating Custom Fields

A field should always return object of the same type (MergeHandler expects this)
