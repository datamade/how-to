# Best practices for working with source control

Most of the work we do at DataMade is done in the context of source control (e.g. GitHub or GitLab). Most of the time this means committing code, but sometimes it means doing more "meta" work on the project: creating issues, reviewing pull requests, or organizing branches and deployments. As a result, we've developed a set of best practices that we try to adhere to when working with source control for our projects.

Our current best practices include guidance for the following aspects of source control:

- [Issues](#issues)
- [Pull requests](#pull-requests)
- [Branches](#branches)

## Issues

[Issues](https://guides.github.com/features/issues/) are the primary way that work at DataMade is planned, tracked, and preserved for posterity. We work with issues every day, and we try to stick to some basic practices:

- **Don't start coding until there's a relevant issue**. Issues help teammates understand what everyone else is up to, and they provide a natural place to look in the future when trying to figure out how a particular problem was solved in the past. Because of this, all work that takes longer than half an hour should typically have an issue tracking it.
- **Use [issue templates](https://help.github.com/en/articles/creating-issue-templates-for-your-repository) where possible**. Issue templates can be especially useful when working on projects where the client has access to source control, but it can also be helpful for setting expectations among your team for how much information should be conveyed in an issue. For an example issue template, see the [bug report template in this repo](/.github/ISSUE_TEMPLATE/bug.md).
- **Link to other relevant issues and PRs**. If you're referencing work done elsewhere, make use of the ability to [link other issues and PRs](https://help.github.com/en/articles/autolinked-references-and-urls) so that your readers can follow the threads of your work. When in doubt, link it.
- **Log progress in detail**. If you figure out something tricky, or if a new development changes the course of the planned work, leave a comment. Leaving new comments is usually preferable to editing old comments because it helps other readers understand how the flow of work proceeded.

## Pull requests

Pull requests are the core of a project: they're how changes actually get made, and how work gets pushed live to our clients and their users. Pull requests are important enough that we spend a lot of time thinking about how to do them better, including:

- **Confirm your build succeeds before requesting review.** If the failure is expected, make note of why in your PR description.
- **Seek code review**. At DataMade, we expect virtually all changes to source code to be reviewed by another developer. There are occasional exceptions to this, such as when working on a very tight budget or when addressing an emergency in production, but in general you should expect all your code to be reviewed before merging.
- **Use [pull request templates](https://help.github.com/en/articles/creating-a-pull-request-template-for-your-repository) wherever possible**. Like issue templates, pull request templates provide clear guidance on how much detail teammates expect from each other when seeking code review. For an example pull request template, see the [template in this repo](/.github/PULL_REQUEST_TEMPLATE.md).
- **Provide a summary of your work**. A reader should be able to quickly glance at your pull request description and come away with an understanding of how it changes the source code.
- **Offer testing instructions**. A bulleted list of testing instructions will help your reviewers evaluate your pull request more efficiently. Like unit tests, these instructions also have the benefit of requiring you to clearly think through the changes that you expect your code to make.
- **Leave comments to explain tricky or counterintuitive choices**. If you think a future developer will need to understand the context of the choice you made, leave it as a comment in the code. If you think the choice you made is only relevant to the current reviewer (for example, it goes outside the scope of the issue at hand to implement a refactor that ulimately makes the code more obvious) leave the explanation as a comment on your pull request.
- **Read your code before requesting review**. The easiest way to catch small mistakes is to read your own code before you request someone else do so. Once you open up a pull request, look through the diff to make sure everything looks good before requesting review. This can also be a good opportunity to add extra comments for your reviewer.
- **Be kind and courteous, both as an author and a reviewer**. We recommend [ThoughtBot's guide to code review](https://github.com/thoughtbot/guides/tree/master/code-review) for an overview of how to be a good author/reviewer. Code review is the primary way that we collaborate at work, so it's important that we try hard to make it a fun and fulfilling process.

## Branches

In general, our projects center around the `main` branch. Continuous integration hooks from our hosting platforms (e.g., Heroku, Netlify) should point to `main`, such that all commits to `main` are deployed to a staging instance.

We deploy to production from a dedicated `deploy` branch. To deploy to production, merge your change into main, pull the changes down locally, and then run `git push origin main:deploy`. That way, the `main` and `deploy` branches will always be fully in sync.

We _do not_ use a `dev` branch for the vast majority of projects. During active development, create feature branches off `main`. It is often helpful to open pull requests for these feature branches during the course of work. When doing so, mark your pull request [as a draft](https://github.blog/2019-02-14-introducing-draft-pull-requests/).

For long running PRs, be sure to `rebase` (don't `merge`) your feature branch onto `main` from time to time to capture any underlying changes from bug fixes or integration of other feature branches.

```bash
git checkout main
git pull
git checkout ${YOUR BRANCH}
git rebase main
```

When you have completed work on your feature branch, mark your PR as ready for review (if it was previously a Draft) and [request a review](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/requesting-a-pull-request-review). Once your changes are accepted, merge the feature branch into `main`. If your pull request involved a lot of extraneous commits, such as debugging CI, merge your pull request using the [squash and merge](https://help.github.com/articles/about-pull-request-merges/#squash-and-merge-your-pull-request-commits) option. This will combine all commits on your feature branch into a single commit, eliminating the extraneous commits.
