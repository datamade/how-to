# Project collateral

When organizing a new project, DataMade encourages producing a set of standard artifacts ("collateral") to facilitate collaboration. These standard artifacts help document the administrative requirements for a project, making it easier for the team to share assumptions about how work will proceed.

Project collateral generally includes the following artifacts:

- [Project folder](#project-folder)
- [Project plan](#project-plan)
    - [Responsibility matrix](#responsibility-matrix)
    - [Project timeline](#project-timeline)
- [Scope of work](#scope-of-work)
- [Repositories](#repositories)
- [Project board](#project-board)
- [FreshBooks projects](#freshbooks-projects)
- [Research](#research)

## Project folder

The project folder is the central repository for all documents related to the project. It should be a Google Drive subfolder under the `Projects` folder in the shared `DataMade` drive.

## Project plan

_[Project plan template](https://docs.google.com/document/d/1rwMSxjZqrGxSRqmxSY35r5kBCfgSPEa59vRQtKydeD8/edit?usp=sharing)_

The project plan is the root document that represents the central store of administrative knowledge about a project. It should be a Google Doc with an obvious title (e.g. `LISC CNDA Site Redesign Project Plan`) stored in the project folder. The project plan should contain links to all of the artifacts mentioned in this document. In the case of prose artifacts like the project timeline, the project plan may contain the artifacts themselves.

For an example project plan, DataMade employees can see the [LISC CNDA Site Redesign Project Plan](https://docs.google.com/document/d/1lZS-_Pr3P5dcrabnZ_e270lAl0l2Hqmzy2gSsKj_nIs/edit?usp=sharing).

The project plan typically collects a few different artifacts, which are documented below.

### Responsibility matrix

Responsibility matrices (sometimes called "RACI matrices") help define which teammates are delegated authority over different aspects of a project. A responsibility matrix specifies four "roles":

- **Responsible**: The teammates who will execute the project. Developers and lead developers are typically _responsible_ for client projects.
- **Accountable**: The teammates who ultimately must answer for the success or failure of the project. Lead developers or other teammates in managerial roles are typically _accountable_ for client projects.
- **Consulted**: The teammates who will offer opinions and advice on different aspects of the project, but who will not be directly involved in the execution or oversight of the work. Lead developers and partners are typically _consulted_ for client projects.
- **Informed**: The teammates who will be reported to about progress on the project. Partners are typically _informed_ for client projects.

Note that for DataMade projects, we will often define the four roles above as a list, not a matrix per se. This is because project teams are often small enough (and not specialized enough) such that a teammate that performs a specific role typically performs that role for all aspects of the project.

For more detail on responsibility matrices, [see the Wikipedia article](https://en.wikipedia.org/wiki/Responsibility_assignment_matrix).

### Project timeline

A project timeline gives a rough estimate of how the manager expects work to proceed on a project. Since we practice Agile development, project timelines shouldn't be treated as concrete plans; instead, they should be thought of as providing a general overview of the manager's expectations for how long different phases of the project will take.

A sample project timeline might look something like this:

> Weeks 1-2: User research report
>
> Week 3: Wireframes
>
> Weeks 4-5: Data import pipeline
>
> Weeks 6-8: Website draft
>
> Weeks 8-10: Polish website draft and iterate with client

## Scope of work

_[Scope of work template](https://docs.google.com/document/d/1IprTA6ikNz6e0BCW086_qXIB_oZGQJpOt8vcaS2ubw0/edit?usp=sharing)_

Scopes of work represent the contracts that we sign before starting work on projects. They are typically drafted by partners, or by lead developers in consultation with partners. When the time comes to collect project collateral, a scope of work will already exist for a project, and the relevant task is simply to link to it for future reference.

## Repositories

Practically all DataMade projects involve source code, meaning that practically all DataMade projects require remote source repositories. Typically we use GitHub repos under the `@datamade` account, but we will occasionally use GitLab in cases where we need to use many private repos or have them be owned by an external organization, such as for work with the Chicago Data Collaborative.

In general, we "default to openness" with public repositories. Sometimes a client will specify that source data should remain private, in which case we will use private repositories. When in doubt, check in with a partner to see whether a repo should be public or private.

Often, we will keep separate repositories for the server configuration for a project, such as [`server-bga-pensions`](https://github.com/datamade/server-bga-pensions). This repo should always be private, to prevent attackers from sniffing out how our servers are configured, and it should be linked to in the project plan along with any other source repositories for the project.

## Project board

All client projects should have open issues organized in a project board, preferably on ZenHub. (We recommend the [ZenHub browser extensions](https://www.zenhub.com/extension) for integrating ZenHub with GitHub.) Project boards are typically configured with the following columns (or "lanes"):

- **Icebox**: Issues we're keeping track of but not actively planning to work on
- **Backlog**: Issues that are on deck for active development
- **In progress**: Issues that are assigned to a developer and are currently being worked on
- **In review**: Issues that are waiting for code review
- **Done/closed**: Issues that have been merged and fixed

Sometimes, project owners will keep a `Done` column in addition to a `Closed` column. In these cases, issues addressed by merged PRs should be moved into `Done` and remain open until sprint planning meetings, when we reflect on them and close them as a group. We typically follow this practice with larger projects like Dedupe.io that involve a substantial budget and time for reflection.

## FreshBooks projects

Time is tracked at DataMade using [FreshBooks](https://my.freshbooks.com). For each item in the scope of work, create [a new FreshBooks project](https://my.freshbooks.com/#/projects) with the following configuration:

- **Name**: The name of the project and scope item. Follow the naming convention `Project title – Scope item title`, e.g., `Payroll Phase 3 – Meetings and Project Planning`.
- **Client**: Add the name, organization, and email of the client contact.
    - Repeat clients should already exist in FreshBooks. Type their name, organization, or email address into the corresponding field, and FreshBooks will autosuggest matching clients in the system.
    - If your project is for a new client, you can add them to FreshBooks from the project creation screen. Simply fill in their information in the Client form, and they will be added to the system. If you aren't sure who the client contact is, consult a partner or lead developer.
- **Project members**: Select all staff assigned to the project. Note, if a staff member is not assigned to the project, it will not show up in their list of projects to track time against.
- **Project type**: Always select `Hourly Project`. **Do not use `Flat Rate Project`, as it will set all tracked time to non-billable.**
- **Set hourly rates**: Under "Select a billing method", select "Team Member Rates". Team member rates are set based on position. Default rates have been set for each team member in FreshBooks, but can be altered based on project in this screen.
- **Project services**: Select relevant services from the existing list. `Research`, `Development`, `Project Management`, and `Meetings` is a good starting point for most projects.
- **Hourly budget**: Divide the cost of the scope item by $175 to estimate the number of hours budgeted for this scope item.
    - FreshBooks does not allow you to input a budget in dollars for hourly projects, so we use this hours estimate to calculate cost [in our project budget script](https://github.com/datamade/project_budget/).
    - The hours budget will provide a rough signal of progress in FreshBooks, but it may become noisy when project staff are working at different rates. Use [the project budget script](https://github.com/datamade/project_budget/) to monitor budget in terms of dollars.
- **End date**: Optionally, add the project deadline. We usually don't track this in FreshBooks.

Here's an example FreshBooks project for a scope item in the CalFWD project:

![CalFWD project in FreshBooks](../images/freshbooks-calfwd.png)

For further reference, FreshBooks maintains [its own documentation on how projects work](https://www.freshbooks.com/support/which-billing-method-should-i-choose).

## Research

DataMade work is guided by a broad mission statement:

> DataMade is a data and web consultancy for civil society. We support our partners in working toward democracy, justice, and equity.

This mission is underpinned by more specific points of view in topic areas
that underpin civil society, e.g., [policing](https://datamade.us/blog/accounting-for-our-part-in-supporting-systems-of-oppression/).

DataMade staff are not expected to be policy experts in every project they take
on. Instead, some projects include hours specifically earmarked for research, so
staff are able to acquire and/or deepen expertise prior to implementation.
Consult the scope of work and/or project manager to clarify how much time you
should spend researching for a given project.

At DataMade, project research usually takes the following shape:

1. **Define the scope of your research.** Talk to the project manager and/or
partners to acquire important context and concepts in your research area.
Identify gaps in your understanding and/or key research questions.
2. **Independently investigate.** Use your preferred search engine (scholarly
search engines, such as [Google Scholar](https://scholar.google.com/), are great, too) to gather materials relevant to your blind spots and research questions.
Share things that surprise or excite or enrage you with other staff – we love
puzzling about the world together!
3. **Tap an expert.** Soliciting help from an expert can be a useful tool to
synthesize what you've learned and add clarity and nuance to your research.
Be sure to follow [this high level advice](https://academia.stackexchange.com/a/63860)
for strategies (and courtesies!) to use when asking for help.

Deeper and more democratized topical expertise helps us identify and execute
better and more sophisticated work, so it's ideal for project research to also
support team learning. That can look like a polished notes document, research
report, or even a slide deck to support a tea time conversation. This artifact
can live in your project folder while it's in progress, but be sure to move it
(or a copy) into the `Research > Topical research` folder in our team Drive
once it's ready to share.
