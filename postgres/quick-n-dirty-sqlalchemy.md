# A quick and dirty introduction to `sqlalchemy`

## Foreword

SQLAlchemy is arguably _the_ SQL toolkit for Python. A library of such stature requires encyclopedic documentation. In contrast to other libraries, where minutiae is relegated to the source code, the SQLAlchemy docs center details. This is wonderful for advanced use, but it makes it slightly harder (especially for beginners) to parse out answers to broader questions, like:

- When are connections to my database opened and closed?
- How many connections are available to my application?
- How can I reuse a connection, e.g., in a transaction?
- How do I tell SQLAlchemy I'm done with a connection?

During the course of a refactor of [Dedupe.io](https://dedupe.io/), DataMade's online interface for deduplicating data, we located the answers to these and other questions in the SQLAlchemy documentation and centralized them in a single document. We have taken care to link to the source documentation wherever possible. We hope that this document will enable you to make more productive expeditions into the broader SQLAlchemy documentation, as it has us.

(Note: The information herein applies to SQLAlchemy 1.2 – YMMV.)

## Engines <sup>[1](http://docs.sqlalchemy.org/en/latest/core/engines.html#engine-configuration)</sup>

The Engine is the foundation of interaction between your application and your database, because it provides access to Connections for querying in raw SQL or can be bound to Sessions for querying the ORM.

It is customary to create an Engine using the `create_engine` method **once per application**. The `create_engine` method accepts a database URI and determines the appropriate way to talk to your database (e.g., the appropriate [dialect](http://docs.sqlalchemy.org/en/latest/dialects/index.html?highlight=dialect)), establishes a [Pool](http://docs.sqlalchemy.org/en/latest/core/pooling.html?highlight=pool) of lazily initialized database connections, and emits an Engine object.

### Pools

To say a Pool "lazily initializes" database connections means no connections are actually opened until the application asks for one. At that time, the Pool opens a connection and a Connection object is made available to the application for transactions, queries, etc. When the application finishes with the Connection object, it is checked back into the Pool, and the underlying connection remains open for reuse.

The maximum number of connections the Pool _will **hold** open_ for reuse is called "Pool size." [The default `pool_size` is 5](http://docs.sqlalchemy.org/en/latest/core/pooling.html?highlight=pool#sqlalchemy.pool.QueuePool.params.pool_size).

"Overflow" is the number of connections the Pool _has opened_ in excess of `pool_size`. For example, if `pool_size` is 5, and 6 connections have been opened, the overflow is 1. Underlying connections in excess of `pool_size` will be closed as Connection objects are checked back in to an overflown Pool.

"Maximum overflow" is the maximum number of connections a Pool _will open_ in excess of `pool_size`. [The default `max_overflow` is 10](http://docs.sqlalchemy.org/en/latest/core/pooling.html?highlight=pool#sqlalchemy.pool.QueuePool.params.max_overflow). When a Connection is requested, but `max_overflow` has been met, the Pool will wait [a specified amount of time](http://docs.sqlalchemy.org/en/latest/core/pooling.html?highlight=pool#sqlalchemy.pool.QueuePool.params.timeout). If a Connection object is checked in, it will be reissued to the current request; if a Connection object is not checked in, the request will time out.

Thus, by default, Pools will open a maximum of 15 connections before hanging and potentially timing out.

`Engine.dispose()` [closes **checked in** connections](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine.dispose) and recreates the Pool, again opening new connections as Connection objects are requested. [Engine disposal should not be used for regular connection management](http://docs.sqlalchemy.org/en/latest/core/connections.html#engine-disposal).

**‼️ Note that Connections that are not checked in are dissociated from the Pool and _remain open_ when `Engine.dispose()` is called. ‼️**

## Transactions

A transaction is an operation or a group of related operations that you wish to complete on your database. All operations in a transaction must be completed successfully, or the entire transaction will be rolled back. This is called [atomicity](https://en.wikipedia.org/wiki/Atomicity_(database_systems)), and it prevents partial updates to your database.

### Transactions using the Engine and Connections <sup>[2](http://docs.sqlalchemy.org/en/latest/core/connections.html#using-transactions)</sup>

While SQLAlchemy provides an API for manually managing Transactions via the Connection object, we prefer to use the Transaction as a context manager because it handles committing and rolling back for you. Both Engine and Connection objects have a `begin` method that yields a Transaction you can use as a context manager.

`Engine.begin()` establishes a Transaction and emits a Connection object for use, like so:

```python
# assuming engine is an instance of Engine
with engine.begin() as connection:
    result = connection.execute('SELECT STATEMENT')
```

`Connection.begin()` establishes and emits a Transaction object like so:

```python
# assuming connection is an instance of Connection
with connection.begin() as transaction:
    connection.execute('UPDATE STATEMENT')
```

In both cases, when the context is exited, [the Transaction is committed or rolled back, and the Connection is checked back in to the Pool](https://github.com/zzzeek/sqlalchemy/blob/master/lib/sqlalchemy/engine/base.py#L1942-L1957).

**‼️ An important note about the `execute` method ‼️**

Both Connection and Engine objects have an `execute` method for issuing queries without the Transaction context. `Connection.execute()` requires an open Connection on which to call `execute`, e.g., it is readily apparent that there is an open Connection to close afterward.

```python
connection = engine.connect()  # Connection checked out from Pool
result = connection.execute('SOME QUERY')
connection.close()  # Connection checked in to Pool explicitly
```

It bears repeating that we like the context manager because it handles the Transaction, as well as closing out the Connection, for you.

```python
with engine.begin() as conn:  # Connection checked out from Pool
    result = conn.execute('SOME QUERY')

# Connection checked in to Pool on context exit
```

`Engine.execute()` is trickier, because it retrieves a Connection to issue the query and **leaves that Connection open until (A) the ResultProxy is exhausted, i.e., via iteration, or (B) explicitly closed.**

```python
result = engine.execute('SOME QUERY')  # Connection checked out from Pool

# No indication in the code a Connection is still checked out

# (A)
result = list(result)  # Connection checked in to Pool after ResultProxy exhausted

# (B)
for row in result:
    # ...
    break

# Connection _remains checked out_ because ResultProxy is not exhausted

result.close()  # Connection checked in to Pool explicitly
```

If you have a circumstance where you are iterating a ResultProxy of
indeterminate length which you may or may not end up exhausting all the way,
you can add a cleanup step that closes the connection for you regardless:


```python
connection = engine.connect()

try:
    for row in result:
        yield row
finally:
    connection.close()
```

The connection _should_ be returned to the pool once the generator is garbage
collected. If you'd like to make triply sure that the connection is returned as
soon as possible, you can delete the reference to the generator and manually
run the garbage collection:


```python
import gc

def yield_rows():
    connection = engine.connect()

    result = connection.execute('SELECT * FROM a_table')

    try:
        for row in result:
            yield row
    finally:
        connection.close()

generator_thing = yield_rows()

for index, thing in enumerate(generator_thing):

    # Create some circumstance where you may not exhaust the generator:
    if index >= 20:
        del generator_thing
        gc.collect()
        break

    # Otherwise do something with each yielded thing:
    print(thing)
```

Running `gc.collect()` might be a bit pedantic here but it makes it a bit
clearer what the intent of running `del generator_thing` is.

There are a few convenience functions for retrieving records from a ResultProxy object: `first` and `fetchall` exhaust the ResultProxy and release the Connection. `fetchmany` and `fetchone` do not exhaust the ResultProxy – even if fetching all the records, i.e., calling `fetchone` on a ResultProxy containing one record – and so the Connection remains checked out and must be checked in explicitly.

Because managing Connections from `Engine.execute()` is totally non-obvious, and there are more straightforward and equally convenient alternatives, **we recommend avoiding pattern altogether** (absent a compelling use case, of course).

### Transactions using Session and ORM <sup>[3](http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#unitofwork-transaction)</sup>

The Session provides an API for querying the ORM. The Session also [keeps track of the state](http://docs.sqlalchemy.org/en/latest/orm/session_state_management.html#quickie-intro-to-object-states) of objects you retrieve, add, or remove from it.

Generally, you retrieve Session objects from the `sessionmaker` factory function as you need them.

```python
# create the engine and session factory
engine = create_engine('SOME_URI')
Session = sessionmaker(bind=engine)

# instantiate a Session
session = Session()
```

To issue queries, you can use `Session.query()` for the ORM, or `Session.execute()` for raw SQL.

```python
# do some stuff
foo = session.query(YOURMODEL)
bar = session.execute('SELECT STATEMENT')
```

If you have a handle on an ORM object, but not the Session it belongs to, you can access the Session using `object_session`, provided the Session has not been closed.

```python
from sqlalchemy.orm import object_session

# Grab a dataset object
ds = session.query(DedupeDataset).first()

object_session(ds)  # <sqlalchemy.orm.session.Session at 0x11721acf8>

session.commit()
object_session(ds)  # <sqlalchemy.orm.session.Session at 0x11721acf8>

session.close()
object_session(ds)  # None
```

Basic Sessions can be closed when you are finished with them, though it is often protective rather than essential since cleanup is usually handled by the Transaction. (See the comment in the `finally` block of the code example [here](http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#managing-transactions).)

FlaskSQLAlchemy provides a Session scoped to the request/response cycle. (Note: Dedupe.io is a Flask application.) **This means it is instantiated for you when a request is made and closed when a request context is exited** – so, all you need to worry about is the Transaction.

The [Transaction life cycle](http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#managing-transactions) within a Session is as follows:

- The Session is initialized in a "begin", or empty, state.
- When the first Query is issued, a Connection is retrieved, and a Transaction is begun. Thus, the Session enters a "transactional" state.
- Subsequent queries are made using the same Connection, as part of the same Transaction.
- The Session is committed or rolled back. Both have the effect of [flushing](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.flush) the pending changes, committing or rolling back the Transaction, and releasing the Connection back to the Pool. This returns the Session to its "begin" state.
