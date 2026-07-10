# Investment Time

This directory contains documentation of DataMade's implementation of investment
time, as well as pointers to documents related to the proposal, pilot, and
adoption of investment time.

## Contents

- README – You are here! 🎉
- [Research](./research.md)

## Investment Time at DataMade

### How much investment time do I have?

DataMade employees earn investment time equal to 10% of hours worked in a given
two-week cycle.

Earned investment time is calculated from hours worked in the week preceding
investment day, as well as hours scheduled to be worked the week of investment
day.

Say a full-time staffer takes a day off and works 28 hours the week before
investment day, and plans to work 35 hours the week of investment day. They
earn `(28 + 35) * 0.1 = 6.3 hours` of investment time.

### When can I use investment time?

Investment time may be spent on designated, companywide investment days, which
take place every other Thursday. These days are marked on the DataMade calendar.
Investment time may not be spent outside of designated investment days.

Client work will be structured and staffed such that conflict with investment
time is minimized, e.g., no late-week launches, managed urgency, and reasonable
boundary setting. Partners and staff will (mutually) respect the use of
investment time and limit expectations of staff on investment days. In the rare
event that an urgent issue arises during investment day, staff should consult
their manager to determine next steps.

Planned investment time should be added to the weekly planning document so other
responsibilities can be scheduled accordingly.

### How can investment time be used?

Developers may use investment time for self-directed work to improve their
skills within the existing DataMade stack. Some example uses include:

- Completing an online course or tutorial
- Retrofitting an existing application to use a different stack, e.g.,
implementing a Django site in Gatsby
- Working on a new, non-client project that uses some part/s of the DataMade
stack, in consultation with their primary manager and potentially a partner
- Working on an R&D issue delegated by a lead developer

For lead developers, investment time encompasses all of the above, plus R&D, as
documented in [CONTRIBUTING.md](../CONTRIBUTING.md).

Developers should discuss their plans for investment time with their primary
managers during their regular 1:1. Managers can help to shape a proposal or come
up with an idea.

Investment time should produce some artifact, be it code, a document, or notes
from a meeting. These should be published in a place accessible to the entire
team and remain accessible in perpetuity, e.g., in a Google Document or GitHub
repository.

#### Investment time and client work

Investment time may only be used for an ongoing client project to accomplish
discrete tasks that improve upon an existing implementation or apply tools in
the DataMade stack in a novel way. It should be thought of as a release valve
for learning via experimentation or reducing technical debt, not a way to
stretch budgeted hours or add new features.

Some examples of acceptable use of investment time on an ongoing client project
include:

- Factoring a _specific_ code smell out of a project, e.g., inconsistent logging
practices or a sub-optimal caching strategy
- Spiking new applications of a tool in the DataMade stack, e.g., revisiting
use of Wagtail as a headless CMS

In certain situations, investment time may be applied to infrastructural
improvements for legacy applications if:

- they are not covered by an existing maintenance contract, and it is not
feasible to acquire new budget; and
- the maintenance outlook for the project could be reasonably estimated to last
several years; and
- the improvements would greatly reduce the maintenance overhead / technical
debt of the project moving forward.

Developers should work in consultation with their primary managers to determine
whether investment time can be used for a task related to an ongoing client
project.
