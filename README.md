# pylambdac

A lambda calculus interpreter in Python.

This is not meant for some serious end; I created it to play around with ways of representing very
large numbers in lambda calculus, in particular the [fast growing
hierarchy](http://googology.wikia.com/wiki/Fast-growing_hierarchy). It's a design goal that the
computation be easy to follow as it's printed, so instead of eg converting to de Bruijn form, we
preserve variable names and rename as appropriate during beta reduction.

Install [poetry](https://python-poetry.org/), then try

    alias poetry='python3 $HOME/.poetry/bin/poetry'

    poetry update
    poetry run ./trylambda --outdir=/tmp/out demofiles/*

This is not an officially supported Google product.
