# Recommendation of Adoption: GitHub Actions Ongoing Scraping

We recommend GitHub Actions as DataMade’s preferred scraping platform when ongoing scraping is required.


## Proof of Concept and Pilot

We have completed three projects that use GitHub Actions for Scraping. 



* [Airline scraping](https://github.com/datamade/airline-points/)
* [Florida Sex Offender Registry](https://github.com/datamade/florida-sex-offender-registry)
* [Chicago Council Scrapers](https://github.com/datamade/chicago-council-scrapers/)


## Prerequisite Skills

GitHub actions has its own YAML configuration syntax. Familiarity with this syntax is helpful, though there [is excellent documentation](https://docs.github.com/en/actions).


## Maintenance and Cost Outlook

GitHub Actions is a deeply integrated feature of GitHub, and it is not accessible from outside GitHub. Using GitHub actions extensively will make it more difficult to switch to an alternative code repository in the future. GitLab has an equivalent feature, but the configuration syntax is not the same.

It is unlikely that GitHub will stop supporting Actions, but it is possible that they will increase costs at some point in the future. GitHub Actions offers a way to use self-hosted runners, which mitigates that risk. For the airline scraping, we are currently using [cirun.io](https://cirun.io), a service that makes it easy to set up self-hosted action runners on various cloud platforms. We use cirun.io with Azure spot instances to get a cost that is much better than EC2.


## Comparison to Existing Tools

DataMade has used two other approaches for running ongoing scrapers. Cron-scheduled processes on EC2 and AirFlow. Here’s how those approaches compare to GithubActions.

The only advantage that Airflow has over GitHub actions is that it is easy to see the next scheduled run, and that there is no limit on the length of time a job takes.

The only advantage that EC2 has is that there is no limit on the length of time a job takes.


<table>
  <tr>
   <td>
   </td>
   <td><strong>EC2 Process</strong>
   </td>
   <td><strong>Airflow</strong>
   </td>
   <td><strong>GitHub Actions</strong>
   </td>
  </tr>
  <tr>
   <td>view logs of particular run
   </td>
   <td>manually set up logging to disk. to view logs, we would ssh into the server and grep the logs.
   </td>
   <td>not possible?
   </td>
   <td>integrated
   </td>
  </tr>
  <tr>
   <td>dashboard to see status of a runs
   </td>
   <td>no
   </td>
   <td>yes
   </td>
   <td>yes
   </td>
  </tr>
  <tr>
   <td>error logs
   </td>
   <td>sentry integration
   </td>
   <td>sentry integration
   </td>
   <td>integrated
   </td>
  </tr>
  <tr>
   <td>deploy changes to scraper
   </td>
   <td>codedeploy
   </td>
   <td>codedeploy
   </td>
   <td>git push
   </td>
  </tr>
  <tr>
   <td>manual dispatch
   </td>
   <td>ssh into server
   </td>
   <td>press-button
   </td>
   <td>press-button
   </td>
  </tr>
  <tr>
   <td>see upcoming run
   </td>
   <td>inspect crontab
   </td>
   <td>integrated
   </td>
   <td>inspect workflow file
   </td>
  </tr>
  <tr>
   <td>scheduling
   </td>
   <td>crontab
   </td>
   <td>Airflow Task definition
   </td>
   <td>workflow syntax
   </td>
  </tr>
  <tr>
   <td>precise scheduling
   </td>
   <td>yes
   </td>
   <td>yes
   </td>
   <td>can delayed by a few minutes
   </td>
  </tr>
  <tr>
   <td>time limits on a scrape
   </td>
   <td>no
   </td>
   <td>no
   </td>
   <td>6 hours on GitHub hosted actions and 24 hours on self-hosted
   </td>
  </tr>
</table>

