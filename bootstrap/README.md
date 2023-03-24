# Bootstrap

We use bootstrap in all of our apps to add consistent styles and functionality using pre-defined classes. This document is intended to primarily point to Bootstrap's excellent documentation on lesser-known bootstrap classes and functionality.

## Versioning
We currently use [Bootstrap 4.6](https://getbootstrap.com/docs/4.6/getting-started/introduction/). Though Bootstrap 5 is around, it does not provide support for Internet Explorer, which we still intend to support as it continues to be an important tool for some clients.

## Guiding Principles
* **Prioritize Grid over Flexbox**: Aim to only use `d-flex` and related classes in situations where you have a variable number of child elements, to space them evenly
* **Roles, not functionality**: Each Bootstrap component is intended for a specific kind of role, but there are a variety of ways to accomplish similar functionality using different classes and components. This also helps keep code DRY and accessible, as many Bootstrap components
* **Accessibility**: The Components subsections of the Bootstrap 4.6 docs all contain a `Sass > Variables` section so you know how to override styles. Many component subsections, particularly the ones that help structure a page or provide site navigation, also contain `Accessibility` sections with tips on how to utilize [ARIA roles and labels](https://www.w3.org/WAI/ARIA/apg/) properly

## Reading the Docs
The Bootstrap docs are very well-organized and thorough, but to make sure you're getting full use of them, here's an overview of the sections and when to look in each one:

1. **Getting started**: downloading Bootstrap; discussion on key issues like accessibility, browser support, and Webpack; and understanding how Bootstrap works
2. **Layout**: understanding how to use Bootstrap classes and [the grid](https://getbootstrap.com/docs/4.6/layout/grid/) to lay out a page.
3. **Content**: fonts, tables, and code
4. **Components**: on-the-page items like buttons, cards, navs, and progress bars
5. **Utilities**: closer looks at important across-the-board tools like colors, spacing, and sizing, as well as funtionality like stretched links
6. **Extend**: build your own styling tool based on Bootstrap
7. **Migration**: info about switching to Bootstrap 5
8. **About**: licensing, translations, etc.

### Hidden gem components
1. [Badges on buttons](https://getbootstrap.com/docs/4.6/components/badge/#example)
2. [Breadcrumb dividers](https://getbootstrap.com/docs/4.6/components/breadcrumb/#changing-the-separator) are `/` characters by default, but you can use any character or image as a divider by setting the inline style && updating a single Sass variable
3. [Button groups](https://getbootstrap.com/docs/4.6/components/button-group/) are a major section in the `Components` part of the documentation, but we don't generally take advantage of these as a way to change up our form layouts
4. [Card headers and footers](https://getbootstrap.com/docs/4.6/components/card/#header-and-footer) could be used as a way of adding metadata for the info on a card
5. [Split dropdown buttons](https://getbootstrap.com/docs/4.6/components/dropdowns/#split-button) a way of including primary functionality of the main part of a button while still providing additional options in an attached dropdown
6. [Dropup, -left, and -right](https://getbootstrap.com/docs/4.6/components/dropdowns/#directions)
7. [Dropdown content](https://getbootstrap.com/docs/4.6/components/dropdowns/#menu-content) can include anything from headers and non-anchored info text to full-on forms
8. [Modals](https://getbootstrap.com/docs/4.6/components/modal/) are quite fully fleshed out in their functionality, with options to control placement, how to close out of them, and handling transitions
9. [Navs](https://getbootstrap.com/docs/4.6/components/navs/) are helpful if you want to incorporate navbar-like functionality somewhere other than the header of your site
10. [Scrollspy](https://getbootstrap.com/docs/4.6/components/scrollspy/) allows you to highlight the nav item that is currently in the viewport. Very handy for helping users keep track of where they are when on a page with lots of well-organized text

### Helpful Helpers
1. [Visually hidden](https://getbootstrap.com/docs/4.6/utilities/visibility/) to make certain tools accessible for assistive tech only
2. [Text overflow and truncation](https://getbootstrap.com/docs/4.6/utilities/text/#text-wrapping-and-overflow)
