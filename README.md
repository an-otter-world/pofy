# Pofy (Python yaml objects)

[![WTFPL license](https://img.shields.io/badge/License-WTFPL-blue.svg)](https://raw.githubusercontent.com/an-otter-world/pofy/master/COPYING)
[![Actions Status](https://github.com/an-otter-world/pofy/workflows/Checks/badge.svg)](https://github.com/an-otter-world/pofy/actions)
[![Coverage Status](https://coveralls.io/repos/github/an-otter-world/pofy/badge.svg)](https://coveralls.io/github/an-otter-world/pofy)

## Overview

Pofy is a tiny library allowing to declare classes that can be deserialized
from YAML, using pyyaml. Classes declares a schema as a list of fields, used
to check for data validation during deserialization.

Pofy is distributed under the term of the WTFPL V2 (See COPYING file).

## Installation

Pofy is tested with Python 3.8. It be installed through pip :

  `pip install pofy`

## Quickstart

To use Pofy, you must declare a schema in the class you want to deserialize :

  ```python
      from pofy import StringField, load

      class SomeObject:
          class Schema:
              field = StringField()

      deserialized_object = load(SomeObject, 'field: value')
      assert deserialized_object.field == 'value`
  ```
