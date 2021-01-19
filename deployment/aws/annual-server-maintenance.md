# Annual server maintenance

DataMade maintains about two dozen EC2 instances that host a number of legacy
applications. An inventory of applications deployed on AWS infrastructure can
be found [here](https://docs.google.com/spreadsheets/d/1_c1_v4IJ5wLpjUt0p0Feq3LXskItu5Ml9J6gZucSqpw/edit?usp=sharing) (internal link).

Our EC2 instances are generally stable and self-sustaining, however [cruft can
build up over time](https://github.com/datamade/how-to/issues/156#issue-778165823). On an annual basis, perform the following steps to free up
space so applications can chug on.

1. Truncate system journal files: `sudo journalctl --vacuum-size=100M`
2. Purge unneeded apt packages: `sudo apt-get autoremove`
    - You may be prompted to run `apt --fix-broken-install`. Go ahead and do this, selecting "Keep local version" if you see any warnings that a file may have changed. You should then be able to run `autoremove` without issues.

Taken together, these steps should clear up 2-3 GB of space.
