# Project collateral

When organizing a new project, DataMade encourages producing a set of standard artifacts ("collateral") to facilitate collaboration. These standard artifacts help document the administrative requirements for a project, making it easier for the team to share assumptions about how work will proceed.

Project collateral generally includes the following artifacts:

- [Project plan](#project-plan)
    - [Responsibility matrix](#responsibility-matrix)
    - [Project timeline](#project-timeline)
- [Scope of work](#scope-of-work)
- [Repositories](#repositories)
- [Project board](#project-board)

## Project plan

_[Project plan template](https://docs.google.com/document/d/1rwMSxjZqrGxSRqmxSY35r5kBCfgSPEa59vRQtKydeD8/edit?usp=sharing)_

The project plan is the root document that represents the central store of administrative knowledge about a project. It should be a Google Doc with an obvious title (e.g. `LISC CNDA Site Redesign Project Plan`) stored in a Google Drive subfolder under the `Projects` folder. The project plan should contain links to all of the artifacts mentioned in this document. In the case of prose artifacts like the project timeline, the project plan may contain the artifacts themselves.

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
