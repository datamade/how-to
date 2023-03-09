# Accessibility

Accessibility (often abbreviated to A11y — as in, "a", then 11 characters, and then "y") is the practice of making the tools and websites we build usable by everyone — however they encounter it. As designers of websites, we should try to accommodate all potential users in as many contexts of use as we can. Doing so has broader benefits — notably better designs for all. 

Accessibility is a growing practice at DataMade, and while many of our sites follow web best practices, explicitly testing for accessibility is only something we've started to undertake in 2021 and 2022.

## Beware of 'overlay' tools that 'solve' accessibility

There are a number of tools, like UserWay, that you can purchase that act as plugins to sit on top of your site and provide accessibility tools. However, accessibility advocates warn against using these tools:

> To laypersons, these features may seem beneficial, but their practical value is largely overstated because the end users that these features claim to serve will already have the necessary features on their computer, either as a built-in feature or as an additional piece of software that the user needs to access not only the Web but all software.
> 
> On this latter point, it is a mistake to believe that the features provided by the overlay widget will be of much use by end users because if those features were necessary to use the website, they'd be needed for all websites that the user interacts with. Instead, the widget is  —at best—redundant functionality with what the user already has.

For more on this, see https://overlayfactsheet.com

## Web Content Accessibility Guidelines - WCAG

The W3C has put together a set of guidelines called the Web Content Accessibility Guidelines (WCAG), with the goal of standardizing accessibility. This is occasionally updated, with the latest version being 2.1. These guidelines are made of testable criteria and are split into a few major sections:

* Perceivable - Info and ui components must be presentable to all users. They cannot be invisible to any of the user’s senses.
* Operable - UI and navigation must be operable. They cannot require operations that a user cannot perform.
* Understandable - Info and operation of UI must be understandable. This involves making sure that users know what to expect when interacting with the page.
* Robust - Content must be robust enough to be interpreted by a wide variety of user agents, including assistive tech. This means future proofing content against evolving technologies.

Every criteria, how to understand them, and how to meet them is described on the [official WCAG 2.1 page](https://www.w3.org/TR/WCAG21/).

Each criterion is associated with a level of conformance: A (lowest), AA, and AAA (highest). Projects with a focus on accessibility tend to aim for level AA. To satisfy any level, the site must adhere to every criterion in that, and previous levels. For example, level AA needs everything from A and AA to pass.

## Key accessibility considerations

The basic approach involves ensuring that the HTML and layout of our websites is structured properly, and that visual elements have `alt` tags or descriptions:  

* Use headings correctly to organize the structure of your content
* Include proper alt text for images
* Use [ARIA labels](https://developer.mozilla.org/en-US/docs/Learn/Accessibility/WAI-ARIA_basics) where appropriate
* Give your links unique and descriptive names
* Use color with care
* Ensure that all content can be accessed with the keyboard alone in a logical way

Refer to [MDN's accessibility docs](https://developer.mozilla.org/en-US/docs/Learn/Accessibility) for more details.

## Accessibility in our Site Launch Checklist

We have incorporated a list of steps to take in our [Site Launch Checklist](https://github.com/datamade/site-launch-checklist) with input from @vkoves. These steps are:

* [ ] Overview - test all pages with a tool like [Axe DevTools](https://chrome.google.com/webstore/detail/axe-devtools-web-accessib/lhdoppojpmngadmnindnejefpokejbdd) or [Google Lighthouse](https://developers.google.com/web/tools/lighthouse/)
* [ ] Keyboard - confirm all functionality works with a keyboard _only_. This includes logical focus order (typically left-right top-down) and no focus traps (except modals)
* [ ] Screen Reader - test pages with a screen reader like [NVDA](https://www.nvaccess.org/download/) on Windows or [VoiceOver on Mac](https://support.apple.com/guide/voiceover/turn-voiceover-on-or-off-vo2682/mac), confirming that all content is clear, including:
  * [ ] Confirm no repeat or unclear button titles (e.g. "Click here" or "View more")
  * [ ] Confirm images have proper alt tags for their context (including `alt=""` for decorative images)
* [ ] Structure - Using [Accessibility Insights for Web](https://chrome.google.com/webstore/detail/accessibility-insights-fo/pbjjkligggfmakdaogkfomddhfmpjeni) or another tool, confirm all pages have clear and sufficient heading levels. Keep in mind it should act like a table of contents, you want to have enough headings to be useful but not one for every paragraph.
* [ ] Color Blindness - make sure no information is conveyed via color only, potentially by testing using grayscale mode in [Accessibility Insights for Web](https://chrome.google.com/webstore/detail/accessibility-insights-fo/pbjjkligggfmakdaogkfomddhfmpjeni)

## Voluntary Product Accessibility Template - VPAT

If you wanted to go a little deeper into a11y with a project, you could check it against a VPAT. Created by the Information Technology Industry Council (ITI), a Voluntary Product Accessibility Template (VPAT) is essentially a checklist where you can document how the site performs against each criterion in each level. 

The WCAG 2.1 VPAT provided by the ITI is convenient, in that the criteria are separated by conformance. So if you wanted, you can just focus on all level A items. It also has links on each criterion that go back to their respective section on the WCAG page to help you understand the item a little more.

Check out the [ITI's page for more context on the VPAT](https://www.itic.org/policy/accessibility/vpat), or [download the WCAG 2.1 VPAT](https://www.itic.org/dotAsset/7edcd54d-c6a6-4649-8375-4a0f0c68eff2.doc).