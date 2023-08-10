# Static IP Addresses
Applications deployed on Heroku don't have a static IP address. But you might need a static IP address to connect with servers outside of Heroku, like a remote database or Solr instance.

## QuotaGuard Static
We recommend the QuotaGuard Static Heroku add-on to manage static IP addresses for your Django application.

## Examples
We've used it in these projects:
1. ccfp-asset-dashboard
    - the app runs with the qgtunnel process. connects with a remote database that required an IP address.
    - [PR example](https://github.com/fpdcc/ccfp-asset-dashboard/pull/91)

2. Illinois Wastewater Surveillance System
    - run the qgtunnel process for a scheduled ETL, because it connects to a remote database.
    - [PR example](https://github.com/datamade/il-nwss-dashboard/pull/172)
