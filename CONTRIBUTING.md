# Making changes to the stack

## Background

Thanks to the addition of a formal research and development process, we have begun to identify opportunities for changing portions of the DataMade Standard Stack™. This process is intended to guide, but not hinder, the exploration of new tooling. Our goal is to empower lead developers to move as fast as possible in adopting new tools that will help the team work more productively, while minimizing the number of stray projects that we must maintain using tools that no one knows how to use.

This process will:

- Enable partners to confidently delegate authority for technical leadership
- Empower lead developers to pursue and implement technical changes
- Make transparent to developers the standard toolkit and process for changes
- Minimize maintenance burden for future developers

This document is a work in progress. If any step in this process is consistently and unnecessarily painful, it is subject to amendment. Amendments to this process should be proposed and agreed upon by lead developers, and approved by partners.

## Process

This process may be exited at any step if lead developers decide that a tool is not a good fit for the team. Lead developers should agree on abandoning a new tool, and the decision should be documented on the research issue tracking work on the tool. For an example of documented abandonment, see the [R&D project on Netlify Add-ons](https://github.com/datamade/ops/issues/610).

### 1. Propose research project to team of lead developers

Lead developers are the primary drivers of the research process. As such, all lead developers should comment and give approval on a research proposal before research begins.

Lead developers should log proposals as issues in this repository (`datamade/how-to`) and tag them appropriately. Proposals should follow the R&D issue template, available as an option when opening new issues in `how-to`.

### 2. Conduct research and develop proof of concept

Proofs of concept are analogous to a spike. They should answer key questions and provide enough signal to indicate whether an approach can produce the desired result. They can take the form of a refactor or rewrite of an existing app, or a toy app. Depending on the complexity of the tool, this step can take anywhere from one to four R&D days to finish.

A proof of concept either builds sufficient confidence to proceed with a pilot project or fails to meet our expectations. In either case, leads should document proof of concept outcomes in the relevant R&D issue.

### 3. Pilot use of the tool on a project

If a proof of concept builds sufficient confidence in an approach, Leads will pilot the new tool on a project.

Piloting new tools should be undertaken carefully. At this point it’s likely that only one developer has expertise in the tool, and we would like to avoid above all a situation where we have to maintain technology that we have decided not to adopt.

Developers should make the following considerations when embarking on a pilot project:

- **Set a contingency plan** in case the tool doesn't work.
- Keep an eye out for signs that the tool is **difficult to debug,** e.g., differences between development and production environments, or hidden logging output.
- **Timebox the learning curve.** If you find yourself going down rabbit holes related to the piloted tool (e.g., a whole day debugging one problem), fall back to your contingency plan.

Some ideal projects on which to pilot a new tool might include:

- A small, self-contained feature being implemented in a mature codebase
- A one-off project that we don’t expect to spend much time maintaining in the future
- A small greenfield project that will involve chunks of major development in the future, offering the possibility to refactor

This phase should be conducted in collaboration with another developer in order to diversify perspectives on the new tool. Collaborators should be selected based on a demonstrated foundation of knowledge that will allow them to adapt to the new tool quickly.

If no other developers yet have the necessary foundation of knowledge to make use of the tool, lead developers will coordinate with partners to plan time for training the collaborator before project work begins.

### 4. Recommend adoption, further research, or abandonment

There are three outcomes that we expect from a pilot:

1. The tool works as advertised, and lead developers recommend its adoption.
2. The tool has mixed results, and lead developers recommend more research.
3. The tool does not work as advertised, and lead developers recommend abandoning it.

Whatever the outcome, the recommendation should include a cost/benefit analysis comparing the tool to other tools that DataMade uses to solve similar problems on a number of levels, including implementation time, prerequisite skills, and maintenance outlook. This cost/benefit analysis will be a draft and will be updated if developers recommend adoption, as they learn more about the tool.

Lead developers should make this recommendation as a group. If one lead developer is leading up the research effort, this collaboration can take the form of a draft that other lead developers help revise. If the lead developers are doing research collaboratively, they might consider collaborating on a recommendation. Either way, the group should reach consensus before moving on.

If lead developers recommend adoption, move on to step 5. If lead developers recommend further research, return to step 1. If lead developers recommend abandonment, document the reasons for abandonment and exit this process.

### 5. Notify partners of recommendation

Formal notification of the partners is not always necessary, in particular when a partner has been apprised of the R&D process and/or the change to our stack is minor, e.g., recommending a preferred package for an existing framework, like Django or React.

In the event that the new tool requires a billing account or additional staff training, Leads should forward their recommendation to partners for review. Partners may seek clarification, request further research, or approve the recommendation and begin planning for the next step.

### 6. Produce adoption artifacts

After the pilot project is complete, lead developers should schedule a retrospective to gather feedback and learning about the tool from all developers involved. The retrospective is intended to help produce adoption artifacts that will guide future use of the tool, including:

- Any updates to initial materials produced during R&D
- A list of lessons learned about the tool, including links to helpful resources
- If applicable, a template for bootstrapping a project with the tool in the future
- If applicable, a plan for providing training for pre-requisite skills to the broader team
    - Training plans may make use of team investment time and should include estimated hours so teammates can plan accordingly

These artifacts should be written up as a pull request against this repo, which serves as the central knowledge store for the DataMade Standard Stack™. Templates or other documentation may exist in separate docs/repos, but they should still be referenced in the `datamade/how-to` repo in order to encourage centralization of knowledge.

If developers somehow reach this step and decide to abandon the tool, they should devise a plan for dealing with future maintenance of the project. This plan might include:

- Refactoring the code to remove the tool
    - Ideally this should happen during the course of normal business, but if no budget is available for the project, lead developers should expect to have to use R&D time to do this cleaning
- Adding extra documentation to help future developers understand the context of the tool
