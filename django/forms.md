# Django Forms

This document collects best practices for working with [the Django Forms API](https://docs.djangoproject.com/en/dev/topics/forms/).

## Contents

- [HTML5 form validation](#html5-form-validation)

## HTML5 form validation

[Most modern browsers](https://caniuse.com/#feat=form-validation) now support [client-side form validation](https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Form_validation). They do this by reading the [attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#Attributes) of input elements and providing corresponding feedback to the user when the form is submitted, before a request is sent to the server. For example, if you have a `first_name` input with the attribute `required`, most browsers will prevent the form from being submitted to the server until `first_name` has a value.

The instantaneous feedback provided by client-side validation can be nice for users, but it has the potential to interfere with [Django's server-side form validation](https://docs.djangoproject.com/en/2.2/ref/forms/validation/) because it means the automatic client-side validation will happen before any custom server-side validation has a chance to run. To extend the `required` example, if you have a [custom validator](https://docs.djangoproject.com/en/3.0/ref/validators/) that allows `first_name` to be empty if another field (like `last_name`) has a value instead, your validator may never run because most browsers will prevent the form from ever being submitted with an empty value for `first_name`.

This behavior can be particularly confusing because Django will automatically translate form attributes defined in Python into HTML input attributes by default. If the `first_name` field has the `required=True` keyword argument set in Python, the corresponding HTML input will have its `required` attribute set by default.

In general, we recommend that you preserve HTML5 validation wherever possible, since it's more convenient for users. However, if you need to do custom server-side validation that contradicts the default HTML5 validation, you can set [`use_required_attribute`](https://docs.djangoproject.com/en/2.2/ref/forms/api/#django.forms.Form.use_required_attribute) to `False` on your `Form` class in order to disable HTML5 form validation.
