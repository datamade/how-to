# Django-React Integration

There are many ways of integrating Django and React. At DataMade, our preferred
method is a so-called "hybrid" approach, where Django builds React components into its templates
by using a context variable for props and bundling components with Babel, Browserify, and
`django-compressor`. This allows a developer to opt-in to using React components
in some templates, while still retaining the full expressive power of Django's
templating system.

At a high level, this is how the stack renders a React component for a given
Django view:

1. A user sends a request for a particular route to Django;
2. The route's view passes props to a Django template using a dedicated `props` key in the
   view's context dictionary, and also specifies a React component file to use for
   that view using a `component` attribute;
3. The Django template for the view reads the `props` key from the view's context
   dictionary, santizes its data, and saves it on the global `window` object;
4. `django-compressor` locates `compress` tags in the Django template and uses Babel and
   Browserify to compile the scripts contained within the tags to vanilla JavaScript.
   It also automatically compiles the file containing the React component for the
   view as specified in the `view.component` attribute;
5. The React component uses the `window.props` object to render once the page
   loads in the user's browser.

This guide provides detailed instructions on configuring and developing an
application to use a hybrid Django-React integration.

## Contents

- [Installation](#installation)
- [Usage](#usage)
    - [Create a static JSX file for your React component](#create-a-static-jsx-file-for-your-react-component)
    - [Define a view with a path to your component](#define-a-view-with-a-path-to-your-component)
    - [Add a `props` key to your view context dictionary](#add-a-props-key-to-your-view-context-dictionary)
    - [Create a Django template for your React component](#create-a-django-template-for-your-react-component)
        - [Define a React root element](#define-a-react-root-element)
        - [Set React props and root element on the `window` object](#set-react-props-and-root-element-on-the-window-object)
        - [Bundle and load your component with `django-compressor`](#bundle-and-load-your-component-with-django-compressor)
        - [Putting it all together](#putting-it-all-together)
- [Project fit considerations](#project-fit-considerations)
- [Further reading](#further-reading)

## Installation

Setting up a hybrid Django-React application requires installing a number of
Node packages, including Babel, Babelify, and Browserify, and then installing
and configuring `django-compressor` to use these packages to bundle your
React components. To set up your application for a Django-React integration,
start by following our documentation for [installing
`django-compressor`](django-compressor.md).

**Note**: If you're using our [`new-django-app` Cookiecutter template](/docker/templates/)
to create your app, these installation steps will already be taken care of for you
and you can skip ahead to [Usage](#usage).


## Usage

Once your Django app is configured to bundle React components with `django-compressor`,
you can bundle React components into your Django templates.

Here are the steps for adding a React component to a template. The examples included
in these steps are taken from the [`django-react-templates`
repo](https://github.com/datamade/django-react-templates), which serves as a
reference for this pattern.

### Create a static JSX file for your React component

In a dedicated static file directory, something like `static/js/pages`, create
a file representing your React component.

As an example, here's a simple component `index.js` that displays the name of a user:

```jsx
import React from 'react'
import ReactDOM from 'react-dom'

const Home = (props) => (
  <>
    <div className="container-fluid mb-1 jumbotron">
      <div className="row">
        <div className="col-sm-10 offset-sm-1">
          <h1 className="mb-3">Django-React Integration</h1>
        </div>
      </div>
    </div>
    <div className="container">
      <div className="row pt-5 pb-4 text-center">
        <p>Welcome, {props.user}!</p>
      </div>
    </div>
  </>
)

ReactDOM.render(
  React.createElement(Home, window.props),
  window.reactMount,
)
```

Note that the component needs to be rendered with the `ReactDOM.render()` method,
and should use the `window.props` object as its props. Later on when we define the
Django template for this component, we'll make sure to save our props to this variable.

### Define a view with a path to your component

Define a Django view that includes a `component` attribute with a staticfile
path to the component you've defined, as well as the typical `template_name`
attribute representing the path to a Django template. The combination of these
two attributes will allow us to render the component in the view's template.

```python
class Home(TemplateView):
    title = 'Home'
    template_name = 'my_new_app/index.html'
    component = 'js/pages/index.js'  # Staticfile path to your component code
```

### Add a `props` key to your view context dictionary

In the context dictionary for your view, add a `props` key representing the props
that you want to pass into your React component. If you're using class-based views,
you can update your context dictionary using the `get_context_data()` method.

```python
class Home(TemplateView):
    title = 'Home'
    template_name = 'example_app/index.html'
    component = 'js/pages/index.js'  # Staticfile path to your component code

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['props'] = {'user': 'foobar'}  # Set React props here
        return context
```

### Create a Django template for your React component

In order to render the React component we just defined, we need a Django template
that can mark the component for bundling. Save this template to the path
defined in your `template_name` view attribute.

There are a few key components to this template. We'll consider them one by one.

#### Define a React root element

The template needs to have an element that React can use as a root to mount
your component. For a better user experience, make sure to embed a loading animation
like a spinner in this element so the user can see that your component is rendering.

As an example, a simple root element might look like this:

```html
<div id="App">
  <!-- Contents get replaced by mounted React.Component -->
  <div class="text-center">
    <i class="fa fa-lg fa-spinner fa-spin"></i><br><br>
    <i class="pending">Loading components...</i><br><br>
  </div>
</div>
```

#### Set React props and root element on the `window` object

In order to make your props and root element available to your React component, add
a simple script to the end of your template to set them on the global `window`
object.

```html
{{ props|json_script:"props" }}  // Serialize and safely sanitize the props
<script type="text/javascript">
  window.props = JSON.parse(document.getElementById('props').textContent)
  window.reactMount = document.getElementById('App')
</script>
```

#### Bundle and load your component with `django-compressor`

Finally, use the `compress` template tag provided by `django-compressor` and the
`view.component` attribute to bundle and load your component as an external script.

```html
{% load compress %}
{% compress js %}
  <!-- The text/jsx type will trigger the COMPRESS_RECOMPILERS command specific to React -->
  <script type="text/jsx" src="{% static view.component %}"></script>
{% endcompress %}
```

#### Putting it all together

With all of these components included, your template will look something like
this:

```html
{% extends "example_app/base.html" %}
{% load static %}

{% block title %}{{ view.title }}{% endblock %}

{% block body %}
<div id="App">
  <!-- Contents get replaced by mounted React.Component -->
  <div class="text-center">
    <i class="fa fa-lg fa-spinner fa-spin"></i><br><br>
    <i class="pending">Loading components...</i><br><br>
  </div>
</div>
{% endblock %}

{% block extra_js %}
{% load compress %}
{{ props|json_script:"props" }}
<script type="text/javascript">
  window.props = JSON.parse(document.getElementById('props').textContent)
  window.reactMount = document.getElementById('App')
</script>
{% compress js %}
  <script type="text/jsx" src="{% static view.component %}"></script>
  <script type="module" src="{% static 'js/base.js' %}"></script>
{% endcompress %}
{% endblock %}
```

Once you add your view to your app's URL patterns, you should be able to
reload your app and view your rendered React component.

## Project fit considerations

Not all projects will be a good fit for the hybrid approach to Django-React integration.
Projects that are a **good fit** will have the following characteristics:

- A small, distinct set of pages that require a **high degree of interactivity**, in the context of
  a larger app that is more straightforward (e.g. a data-management app with an interactive
  data-driven map or dashboard)
- Some degree of flexibility about **how fast the interactive pages load**, since hybrid
  Django-React apps cannot be rendered on the server and so will have a brief extra loading
  animation (e.g. a map that can load under a spinner animation)
- Sufficient backend functionality that **a static app is not feasible** (e.g. an app
  that requires user management)

If your app does not have these characteristics, but a high degree of interactivity
is still required, talk to a lead developer to discuss your options. There may
be a way of factoring out certain portions of your app and deploying them as
standalone [Gatsby apps](/gatsby).

## Further reading

This approach is heavily inspired by Nick Sweeting's blog post
[How to build a frontend without making a Single-Page
App](https://hackernoon.com/reconciling-djangos-mvc-templates-with-react-components-3aa986cf510a).
If you'd like to get a better sense of the logic behind this pattern we strongly
reccommend reading the post.

For more background on the research that led us to adopt this approach, see
[the corresponding R&D issue](https://github.com/datamade/how-to/issues/66).
