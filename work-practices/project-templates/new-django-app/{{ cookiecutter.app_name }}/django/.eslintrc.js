module.exports = {
  globals: {
    __PATH_PREFIX__: true,
  },
  extends: ["eslint:recommended", "prettier"],
  rules: {
    indent: ["error", 2],
    "no-console": "off",
    strict: ["error", "global"],
    curly: "warn",
    semi: ["error", "never"],
    "space-in-parens": ["error", "never"],
    "space-before-blocks": ["error", "always"],
  },
  ignorePatterns: [
    "{{ cookiecutter.module_name }}/static/js/lib/**/*.js",
    "venv/**/*",
    "/static/**/*",
  ],
  parserOptions: {
    sourceType: "module",
    allowImportExportEverywhere: true,
  },
  env: {
    browser: true,
    node: true,
    es2022: true,
  },
}
