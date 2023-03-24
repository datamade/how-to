# Bootstrap

## Guiding Principles & Tips
* **Prioritize Grid over Flexbox**: Aim to only use `d-flex` and related classes in situations where you have a variable number of child elements, to space them evenly
* **Roles, not functionality**: Each Bootstrap component is intended for a specific kind of role, but there are a variety of ways to accomplish similar functionality using different classes and components. This also helps keep code DRY and accessible, as many Bootstrap components
* **Accessibility** Using Bootstrap appropriately helps keep code DRY and accessible. Keep in mind that many component subsections, particularly the ones that help structure a page or provide site navigation, contain `Accessibility` sections with tips on how to utilize [ARIA roles and labels](https://www.w3.org/WAI/ARIA/apg/) properly

## Reading the Docs
The Bootstrap docs are very well-organized and thorough, but to make sure you're getting full use of them, here's an overview of the sections and when to look in each one:

1. **Getting started**: downloading Bootstrap; discussion on key issues like accessibility, browser support, and Webpack; and understanding how Bootstrap works
2. **Customize**: overriding default styles
3. **Layout**: understanding how to use Bootstrap classes to lay out a page. Do note: we do not use the CSS Grid, but primarily use the [standard grid](https://getbootstrap.com/docs/5.1/layout/grid/) to structure our sites
4. **Content**: fonts, tables, and figures
5. **Forms**: forms, inputs, and validation classes
6. **Components**: on-the-page items like buttons, cards, navs, and progress bars
7. **Helpers**: a few classes that add desired functionality and behavior
8. **Utilities**: closer looks at important across-the-board tools like colors and opacity; flexbox; and sizing
9. **Extend**: build your own styling tool based on Bootstrap
10. **About**: licensing, translations, etc.

### Hidden gem components
1. [Badges on buttons](https://getbootstrap.com/docs/5.1/components/badge/#buttons) and [positioned badges](https://getbootstrap.com/docs/5.1/components/badge/#positioned)
2. [Breadcrumb dividers](https://getbootstrap.com/docs/5.1/components/breadcrumb/#dividers) are `/` characters by default, but you can use any character or image as a divider by setting the inline style && updating a single Sass variable
3. [Button groups](https://getbootstrap.com/docs/5.1/components/button-group/) are a major section in the `Components` part of the documentation, but we don't generally take advantage of these as a way to change up our form layouts
4. [Card headers and footers](https://getbootstrap.com/docs/5.1/components/card/#header-and-footer) and [card navigation](https://getbootstrap.com/docs/5.1/components/card/#navigation) could be used as a way of making more complex jumbotrons or announcements
5. [Card borders](https://getbootstrap.com/docs/5.1/components/card/#border) are a visually distinctive way of categorizing large groups of cards, similarly to the [CPS SSCE dashboard Partner directory](https://cps-ssce-dashboard-staging.herokuapp.com/community-partners/partner-list/)
6. [Split dropdown buttons](https://getbootstrap.com/docs/5.1/components/dropdowns/#split-button) a way of including primary functionality of the main part of a button while still providing additional options in an attached dropdown
7. [Dropup](https://getbootstrap.com/docs/5.1/components/dropdowns/#dropup), [dropleft](https://getbootstrap.com/docs/5.1/components/dropdowns/#dropleft), and [dropright](https://getbootstrap.com/docs/5.1/components/dropdowns/#dropright)
8. [Dropdown/up/right/left content](https://getbootstrap.com/docs/5.1/components/dropdowns/#menu-content) can include anything from headers and non-anchored info text to full-on forms
9. [List groups](https://getbootstrap.com/docs/5.1/components/list-group/) as separate from [accordion components](https://getbootstrap.com/docs/5.1/components/accordion/)
10. [Modals](https://getbootstrap.com/docs/5.1/components/modal/) are quite fully fleshed out in their functionality, with options to control placement, how to close out of them, and pre-filling modal form information
11. [Navs](https://getbootstrap.com/docs/5.1/components/navs-tabs/) are helpful if you want to incorporate navbar-like functionality somewhere other than the header of your site
12. [Offcanvas](https://getbootstrap.com/docs/5.1/components/offcanvas/) refers to hidden sidebars that hold content similarly to a modal; a classic use case is a shopping cart
13. [Placeholders](https://getbootstrap.com/docs/5.1/components/placeholders/) might be an interesting substitute for our current use of lorem text and placeholder text for things like Bootstrap cards and accordions. Placeholders retain colors and other styles to give a more accurate sense of what content will look like, and make use of a loading cursor on hover
14. [Scrollspy](https://getbootstrap.com/docs/5.1/components/scrollspy/#example-with-nested-nav) allows you to highlight the nav item that is currently in the viewport. Very handy for helping users keep track of where they are when on a page with lots of well-organized text

### Helpful Helpers
1. [Colored links](https://getbootstrap.com/docs/5.1/helpers/colored-links/)
2. [Ratio classes](https://getbootstrap.com/docs/5.1/helpers/ratio/) to maintain certain aspect ratios regardless of screen size
3. [Flexbox stacks](https://getbootstrap.com/docs/5.1/helpers/stacks/) allow you to quickly organize flex children vertically or horizontally
4. [Visually hidden](https://getbootstrap.com/docs/5.1/helpers/visually-hidden/) to make certain tools accessible for assistive tech only
5. [Text truncation](https://getbootstrap.com/docs/5.1/helpers/text-truncation/)
6. [Vertical rule](https://getbootstrap.com/docs/5.1/helpers/vertical-rule/), this class styles a div exactly like an hr element, but vertical
