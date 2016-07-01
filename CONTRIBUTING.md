# Contributing to Slack Data Collector

SDC uses [Github](https://github.com/mena-devs/slack_data_collector) to manage
contributions. It's expected that you create yourself an account on this
platform. We assume prior familiarity with Git. This document will not
cover basic Git operations like committing or pushing to a remote.

## Open an issue in the bug tracker

We do not require opening a ticket in the Github issue tracker. However if there
are feature requests or discussions you'd like to have before submitting your
code, this is the preferable place to do it.

## How to submit your code

Follow a classic Github workflow:

1. Fork the repository to your personal Github account.
2. Clone your personal repository to your local machine.
3. (Optional but highly recommended) On your local machine create a branch for
   your development. If you're planning on sending multiple contributions, it's
   a wise idea to keep your `master` branch in sync with the upstream and keep
   your own modifications limited to local branches.
4. Modify the code and commit your changes.
5. Push the branch/commits you made to your personal fork on Github.
6. Use the Github UI to send a Pull Request to the upstream.

## Tests, gating and tox

SDC comes with a suite of automated tests that you can use to validate your
development. Upstream, we use
[Travis CI](https://travis-ci.org/mena-devs/slack_data_collector) as a gating
mechanism to validate contributions. Note that you can save a lot of time by
running the exact same tests locally before sending your contribution.

SDC uses `tox` to launch the tests. The simplest way to execute them is by
running:

``` sh
tox
```

If all is good you should see something like:

```
___________________________________ summary ____________________________________
  linters: commands succeeded
  py27: commands succeeded
  py35: commands succeeded
  congratulations :)
```

`tox` will execute by default 3 test targets:

* linters
* py27
* py35

`linters` are a bunch of automated static analysis checks. They help maintain
uniform style throughout the code as well as avoiding certain pitfalls.

`py27` and `py35` execute the unit tests using respectively Python 2.7 and
Python 3.5 as a runtime. Obviously, the tests will fail if you don't have these
interpreters installed. In this case, you can specify the version of python you
have installed from the command line:

``` sh
# execute tests with Python 3.3
tox -e py33
```

It should go without saying but we do not accept a contribution that will break
any of these tests.
