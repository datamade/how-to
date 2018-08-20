# `lxml` for web scraping

## Getting started

### What is scraping?

Every webpage contains data. Sometimes, this data proves useful in a context other than the user interface of the webpage itself. Happily, with the right tools, we can extract data from any webpage. Indeed, we might think of a webpage as a "really bad" API (credit: Forest Gregg), with which we can interact and collect information.

At DataMade, we use [the `lxml` library](https://lxml.de/) to access webpages. The `lxml` library parses and processes HTML. It’s well-documented, expansive, and popular.

### Want to read more?

The [`lxml` documentation](http://lxml.de/lxmlhtml.html) provides extensive discussion of the library and all it has to offer. And [this guide](http://docs.python-guide.org/en/latest/scenarios/scrape/) gives a snappy overview of scraping, in general.

For now, we will cover a few basics and then consider a sophisticated scraper: [`python-legistar`](https://github.com/opencivicdata/python-legistar-scraper).

## Fundamentals of `lxml`: A Tutorial

Keep your project organized with a virtualized environment, which safely isolates requirements for a unique Python app. We recommend [using `virtualenv` and `virtualenvwrapper`](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).

```bash
mkvirtualenv scraper-tutorial
pip install requests
pip install lxml
```

Next, let’s write some code. Create a new Python file (e.g., `new_scraper.py`), and import two libraries at the top of the file:

```python
import requests
import lxml.html
from lxml.etree import tostring
```

Now, identify a website that holds useful, precious, and/or interesting data. For this tutorial, we will use the calendar of events available in Legistar [from the Los Angeles Metro Transportation Authority](https://metro.legistar.com/Calendar.aspx).

Get the text of the webpage, using the `requests` library:

```python
entry = requests.get(‘ https://metro.legistar.com/Calendar.aspx ‘).text
```

Then, parse the retrieved page with the `lxml` library:

```python
page = lxml.html.fromstring(entry)
```

The `fromstring` method returns HTML – either a full HTML document or an HTML fragment, depending on the input.

Next, we need to locate and isolate elements within the DOM. We can do this with `xpath` - a collection of precise expressions used to traverse an XML document. (Here's [a cheatsheet](https://devhints.io/xpath).)

Let’s first inspect the webpage in question: [Visit the site](https://metro.legistar.com/Calendar.aspx), right click, and select "Inspect" to open the Elements tab of the developer console. You'll see a little something like this:

```html
<body>
…
<form>
	…
	<div id=’ctl00_Div1’>
		<div id=’ctl00_Div2’>
			<div id=’ctl00_divMiddle’>
				…
				<div id=’ctl00_ContentPlaceHolder1_MultiPageCalendar’>
					…
					<table>
					...
					...

</body>
```

That’s a messy DOM! Notice that the page contains a body (of course) and a form with several nested divs and tables.

We want to access a particular table, i.e., the table with information about Metro meetings. To do so, we can write something like this:

```python
div_id = 'ctl00_ContentPlaceHolder1_divGrid'
events_table = page.xpath("//body/form//div[@id='%s']//table" % div_id)[0]
```

Let’s break this down.

"/" tells `xpath` to look for direct children: with "body/form," `xpath` looks for instances of forms that sit directly within the body, rather than forms nested further within the DOM.

On the other hand, "//" tells `xpath` to look for all descendents: with "//table," `xpath` looks for all table descendants of the specified div. How do you specify a div? @id allows us to search for a div with a unique identifier. It prevents the hassle of iterating over handfuls of nested divs, which – in this example – could get rather sticky.

`xpath` returns a list. In this example, we know that we want the first element in this list - so we conclude the above code snippet by grabbing the zeroeth index.

Want to see what’s inside the element? You can print your table to the console. Call the `tostring` function, and check out the results.

```python
print(tostring(events_table))
```

We want to get content inside the table cells. First, get all table rows, and then, iterate over each row, get tds from the row, and iterate over the tds - isolating the content of individual table cells.

```python
table_rows = events_table.xpath(".//tr")

for row in table_rows:
    tds = row.xpath("./td")
    for td in tds:
        print(td.text_content())
```

You can do whatever you like with the the table cell content. Save it in a list! Create a dict with the headers! Import it to the database! Or simply print it, and enjoy your mastery over the DOM.

### `python-legistar`

_Coming soon!_
