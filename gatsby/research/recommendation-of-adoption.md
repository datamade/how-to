# Recommendation of adoption: GatsbyJS

Based on our research, we recommend adopting Gatsby as our framework of choice for the following types of projects:

1. Static sites (that is, sites that can be deployed with pure HTML/CSS/JavaScript)
2. Small dynamic sites with a limited range of simple server-side functions **not** including faceted search, user administration, or admin interfaces

The following document records our recommended path forward for adopting Gatsby.

## Prerequisite skills

The biggest obstacle to incorporating Gatsby into our standard stack is a lack of prerequisite skills among developers. Specifically, Gatsby requires that new developers be comfortable with:

- GraphQL
- ES6 (modern JavaScript)
- React

Lack of familiarity with GraphQL is not a pressing challenge, since Gatsby makes only very limited use of GraphQL. Based on our pilot project, we recommend allocating 2 hours for a developer to follow [The Fullstack Tutorial for GraphQL](https://www.howtographql.com/) when working on their first Gatsby project.

Lack of familiarity with ES6 and React is a more important challenge, since both tools are used extensively in Gatsby and neither tool integrates easily with our current stack. Based on our experience in the pilot project, it's particularly important that we invest time in learning ES6 separate from Gatsby projects, since ES6 is important for understanding the Gatsby and React documentation.

In sum, we make the following recommendations for developing prerequisite skills among our staff:

1. Adopt ES6 as our new standard for JavaScript, and invest R&D time in creating a templated build environment for using it with Django projects
2. Set aside ~2 hours per new dev for Gatsby projects for them to do the GraphQL tutorial
3. Do one (or both) of two things to encourage React learning:
    - Set aside ~4 hours per new dev for Gatsby projects for them to do the React and Gatsby tutorials
    - Try to lead some sort of company-wide Gatsby/React learning group, where we would all do the tutorial and come together to share challenges and lessons
