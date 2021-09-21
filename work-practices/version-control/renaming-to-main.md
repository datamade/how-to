## Changing your default branch to main

Starting in June 2020, all new repositories created in GitHub have their default branch set to `main` instead of `master`. For repositories created before this date, the default branch must be renamed manually. As we have a number of repositories at DataMade created before this date, our policy is to make this change to any repositories we are actively working on.

## Context - why are we moving away from the term 'master'?

We are making this small change to our code repositories to remove the unnecessary reference of `master`, a term that invokes human slavery and contributes to making our community and work less inclusive.

You can read more about the context about this name change here:

* https://www.theregister.com/2020/06/15/github_replaces_master_with_main/
* https://twitter.com/mislav/status/1270388510684598272
* https://www.theregister.com/2020/06/08/developers_renew_push_to_get/

## Steps to migrate from master to main

GitHub offers a number of helpful tools in their platform and guides to make this change easier: https://github.com/github/renaming. Here are the steps to follow:

1. For the repository you want to update, go to the GitHub Settings page and click on Branches.
2. Edit the Default branch and change it to `main`. This will update all open pull requests as well.
3. All local environments will need to be updated. Everyone with a local copy will need to run:

```bash
git branch -m master main
git fetch origin
git branch -u origin/main main
git remote set-head origin -a
```

4. Do a global find for references to 'master' in your code and update where appropriate. This is typically in places like `README.md` and `.github/workflows/main.yml`
5. For apps deployed to Heroku, it should automatically pick up on the new default branch. However, if you had any automatic deploys set up off that branch, you will need to go into the settings and re-enable them off the new `main` branch.
6. For apps deployed on Netlify, you will need to edit the Deploy settings and update the Production branch to `main`.


## Renaming examples

- [CPS SSCE Dashboard - Pull Request #290](https://github.com/datamade/cps-ssce-dashboard/pull/290)
- [Erikson Risk & Reach - Pull Request #262](https://github.com/datamade/risk-and-reach/issues/262)