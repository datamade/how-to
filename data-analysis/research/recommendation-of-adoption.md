# Recommendation of Adoption

We recommend RMarkdown for authoring literate research reports when the following conditions pertain:

1. The report is for a client
2. When the report contains graphs or statistics.
3. When we use code to generate the graphs or statistics. If we are doing an quick analysis in Excel, because that is what a client needs, then a literate research report would not be useful approach.

RMarkdown should be used even if it the report seems like it will be quick and lightweight. Experience tells us that it is not easy to predict when an analysis will grow in complexity or when a client may return months later to ask about a detail in a quick analysis.

## Proof of concept and pilot

RMarkdown has been the tool of choice for authoring reports in the Courts project. DataMade staff familiar with Pweave have picked it up quickly and journalists without a deep background in programming have also been able to use it successfully (within the RStudio environment).

## Prerequisite Skills

RMarkdown's interleaving of text and code adds another layer to interact with code. As such, we advise that staff not be introduced to RMarkdown until they are familiar with the programming language they will be using in the report. If the report will depend on SQL code, the developer should be familiar with how write and debug SQL code in the terminal or by writing SQL scripts. 

If something is not working within a RMarkdown file, it's very useful to be able to work on the code in familiar environment in order to narrow the possible considerations while debugging.

Experience with the R programming language is not a prerequisite, unless that's the language that most of the analysis will be done in.

## Maintenance outlook

It is already DataMade's experience that literate research reports are more maintainable than alternative report authoring workflows.

As far as RMarkdown in particular, the longterm outlook for this tool is excellent. 

1. RMarkdown is maintained by RStudio, the major commercial player in R.
2. The R community has settled on RMarkdown (and RStudio) as not just an report authoring tool, but as their notebooking tool. Any possible successor to RMarkdown will have significant pressure to be backwards compatible.
3. RMarkdown, as a file format, is very lightweight and convertible.

## Editors

[RStudio](https://rstudio.com/) is an excellent IDE for RMarkdown. We recommend that people new to RMarkdown start with using RStudio.