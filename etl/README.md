# ETL

ETL refers to the general process of:

1. taking raw **source data** (*"Extract"*)
2. doing some stuff to get the data in shape, possibly involving intermediate **derived files** (*"Transform"*)
3. producing **final output** in a more usable form (for *"Loading"* into something that consumes the data - be it an app, a system, a visualization, etc.)

At DataMade, [GNU Make](https://www.gnu.org/software/make/) forms the cornerstone of our ETL pipeline. We maintain detailed documentation of our Make patterns and expanded Unix utility toolkit [here](https://github.com/datamade/data-making-guidelines).

Sometimes, we write ETL components, such as processors or data loading commands, in Python. This directory contains documentation for our preferred tooling for those components.

### Contents

- [Schema validation](schema-validation.md)
