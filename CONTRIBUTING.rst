.. highlight:: shell

============
Contributing
============

N.B. -- UNDER CONSTRUCTION -- The following all still needs to be verified and updated.

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/genuinemerit/saskan-app/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

The sakan-wiki can always use more documentation, either for developers or users.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/genuinemerit/saskan-app/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `saskan-app` for local development.

1. Fork the `saskan-app` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/saskan-app.git

3. This is how you set up your fork for local development::

    $ cd saskan-app/
    [this needs work to explain using mamba...
    $ python3 -m venv venv
    $ python setup.py develop
    ]


4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8, isort and the
   tests::

    $ make lint
    $ python setup.py test

   Include flake8 and isort (and...) in your mamba set up. See saskan.yml.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.12. Check
   # https://travis-ci.org/genuinemerit/saskan-app/pull_requests
   # https://github.com/genuinemerit/saskan-app/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::


    $ python -m pytest tests.test_saskantinon

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bumpversion patch # possible: major / minor / patch / dev
$ git push
$ git push --tags
