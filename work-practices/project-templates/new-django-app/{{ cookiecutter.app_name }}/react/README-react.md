## React-Django integration

### How it works

DataMade's patterns for integrating Django with React are well documented, [here](https://github.com/datamade/how-to/blob/main/django/django-react-integration.md).
You can also learn more about how we use Django Compressor to transpile the React
we write, [here](https://github.com/datamade/how-to/blob/main/django/django-compressor.md).

### Ensuring browser compatibility

The default `babel.config.json` file will transpile JavaScript in your static
directory to syntax that's friendly to modern and legacy browsers but it will
not transpile third-party plug-ins by default.

Some plug-ins target Node versions above ES5, which means that they aren't
compatible for older browsers. Luckily, we can tell Babel to transpile these
dependencies to ensure our apps remain broadly compatible across browsers.

To identify problematic plug-ins, you can use [the `es6-sniffer` CLI](https://github.com/hancush/python-es6-sniffer).

```bash
# Build the es6-sniffer image from GitHub
docker build -t es6-sniffer https://github.com/hancush/python-es6-sniffer.git

# Sniff out potentially incompatible modules
docker run -v {{ cookiecutter.app_name }}_{{ cookiecutter.app_name }}-node-modules:/node_modules --rm es6-sniffer
```

Once you've found the culprits, add them to the `only` array in
`babel.config.json`. For example:

```json
{
    "only": [
        "./{{ cookiecutter.module_name }}/static", // Your JavaScript - default
        "./node_modules/problem_module_a",
        "./node_modules/problem_module_b"
    ],
    // The rest of your config
}
```
