# ETL

<blockquote>
<p>ETL refers to the general process of:</p>

<p>
    <ol>
        <li>taking raw <strong>source data</strong> (<em>"Extract"</em>)</li>
        <li>doing some stuff to get the data in shape, possibly involving intermediate <strong>derived files</strong> (<em>"Transform"</em>)</li>
        <li>producing <strong>final output</strong> in a more usable form (for <em>"Loading"</em> into something that consumes the data - be it an app, a system, a visualization, etc.)</li>
    </ol>
</p>
</blockquote>

At DataMade, [GNU Make](https://www.gnu.org/software/make/) forms the cornerstone of our ETL pipeline. We maintain detailed documentation of our Make patterns and expanded Unix utility toolkit [here](https://github.com/datamade/data-making-guidelines).

Sometimes, we write ETL components, such as processors or data loading commands, in Python. This directory contains documentation for our preferred tooling for those components.

### Contents

- [Schema validation](schema-validation.md)
