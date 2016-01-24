Domain models
============

Domain models framework for Python projects

+---------------------------------------+---------------------------------------------------------------------------------------------------+
| *PyPi*                                | .. image:: https://img.shields.io/pypi/v/domain_models.svg?style=flat-square                      |
|                                       |    :target: https://pypi.python.org/pypi/domain_models/                                           |
|                                       |    :alt: Latest Version                                                                           |
|                                       | .. image:: https://img.shields.io/pypi/dm/domain_models.svg?style=flat-square                     |
|                                       |    :target: https://pypi.python.org/pypi/domain_models/                                           |
|                                       |    :alt: Downloads                                                                                |
|                                       | .. image:: https://img.shields.io/pypi/l/domain_models.svg?style=flat-square                      |
|                                       |    :target: https://pypi.python.org/pypi/domain_models/                                           |
|                                       |    :alt: License                                                                                  |
+---------------------------------------+---------------------------------------------------------------------------------------------------+
| *Python versions and implementations* | .. image:: https://img.shields.io/pypi/pyversions/domain_models.svg?style=flat-square             |
|                                       |    :target: https://pypi.python.org/pypi/domain_models/                                           |
|                                       |    :alt: Supported Python versions                                                                |
|                                       | .. image:: https://img.shields.io/pypi/implementation/domain_models.svg?style=flat-square         |
|                                       |    :target: https://pypi.python.org/pypi/domain_models/                                           |
|                                       |    :alt: Supported Python implementations                                                         |
+---------------------------------------+---------------------------------------------------------------------------------------------------+
| *Builds and tests coverage*           | .. image:: https://img.shields.io/travis/ets-labs/domain_models/master.svg?style=flat-square      |
|                                       |    :target: https://travis-ci.org/ets-labs/domain_models                                          |
|                                       |    :alt: Build Status                                                                             |
|                                       | .. image:: https://img.shields.io/coveralls/ets-labs/domain_models/master.svg?style=flat-square   |
|                                       |    :target: https://coveralls.io/r/ets-labs/domain_models                                         |
|                                       |    :alt: Coverage Status                                                                          |
+---------------------------------------+---------------------------------------------------------------------------------------------------+

Introduction
~~~~~~~~~~~~

Use cases:

- Writing some HTTP API client library, that is based on domain models pattern.

  + Examples:

    - Twitter API client library.

- Using NoSQL services with manual mapping to domain models.

  + Examples:

    - Redis.
    - Cassandra CQL.

- Using classic SQLAlchemy mapping.

  + Examples:

    - http://docs.sqlalchemy.org/en/latest/orm/mapping_styles.html#classical-mappings
