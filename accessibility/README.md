# Accessibility

Accessibility is the practice of making the tools and websites we build usable by everyone — however they encounter it. As designers of websites, we should try to accommodate all potential users in as many contexts of use as we can. Doing so has broader benefits — notably better designs for all. 

Accessibility is a growing practice at DataMade, and while many of our sites follow web best practices, explicitly testing for accessibility is only something we've started to undertake in 2021 and 2022.

## Beware of 'overlay' tools that 'solve' accessibility

There are a number of tools, like UserWay, that you can purchase that act as plugins to sit on top of your site and provide accessibility tools. However, accessibility advocates warn against using these tools:

> To laypersons, these features may seem beneficial, but their practical value is largely overstated because the end users that these features claim to serve will already have the necessary features on their computer, either as a built-in feature or as an additional piece of software that the user needs to access not only the Web but all software.
> 
> On this latter point, it is a mistake to believe that the features provided by the overlay widget will be of much use by end users because if those features were necessary to use the website, they'd be needed for all websites that the user interacts with. Instead, the widget is  —at best—redundant functionality with what the user already has.

For more on this, see https://overlayfactsheet.com

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
