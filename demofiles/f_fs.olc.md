# Large numbers using the fast-growing hierarchy

A nice way to describe a really large number is to describe a big ordinal, and plug it in to the
[fast-growing hierarchy](http://googology.wikia.com/wiki/Fast-growing_hierarchy). For this, some
familiarity with countable ordinals is needed; everything I know about the subject is in John Baez's
excellent series of blog posts Large Countable Ordinals ([part
1](https://johncarlosbaez.wordpress.com/2016/06/29/large-countable-ordinals-part-1/), [part
2](https://johncarlosbaez.wordpress.com/2016/07/04/large-countable-ordinals-part-2/), [part
3](https://johncarlosbaez.wordpress.com/2016/07/07/large-countable-ordinals-part-3/)).

Let's start by looking at the standard way to define natural numbers (**N**), using [Church
encoding](https://en.wikipedia.org/wiki/Church_encoding). Though this is the untyped lambda
calculus, it can help to think of functions as having "types" indicating their purpose, so
we'll call Church integers **N**, and zero is
`c0`: **N**

    let c0 = λf x. x;

while the successor function is
`csucc`: **N** → **N**, ie a function from N to N.

    let csucc = λn f x. n f (f x);

We could define integers above zero as eg `let c1 = csucc c0`, but I'm optimizing for fewer bits in
the final expression here, so let's define these by hand:
`c1, c2, c3, c4`: **N**

    let c1 = λx. x;
    let c2 = λf x. f (f x);
    let c3 = λf x. f (f (f x));
    let c4 = λf x. f (f (f (f x)));

With this structure, we say that if you have some function on natural numbers
such that you know *F*(0) = *z*, and there exists a function *s* such that
*F*(*n* + 1) = *s*(*F*(*n*)), then the lambda calculus representation of
*F*(*x*) is simply `x s z`.

We can extend this idea to represent countable ordinals with fundamental sequences
in lambda calculus if we add a way of handling limits.
For this we ask for a function *l* such that where *α* is a limit ordinal,
*F*(*α*) = *l*(λ*i*. *F*(*α*[*i*])); in other words, we hand *l* a function
that maps integers to *F* applied to that index in the limit sequence. Thus
an ordinal *α* is a function which takes these three parameters *l*, *s*, *z*,
and returns *F*(*α*) ie `α l s z` = *F*(*α*).

Let's call the type of computable countable ordinals with fundamental
sequences **Ord**, and suppose *F* is a function which takes an ordinal
and returns some type **T**. Then the three parts we'll use to represent *F*
have types:

* *l*: (**N** → **T**) → **T**
* *s*: **T** → **T**
* *z*: **T**

and the type **Ord** takes one of each:

* **Ord** = ((**N** → **T**) → **T**) → (**T** → **T**) → **T** → **T**

Note that "**A** → **B** → **C**" should be interpreted as
"**A** → (**B** → **C**)" as per the usual convention for representing
multi-argument functions in the lambda calculus; see also
[Currying](https://en.wikipedia.org/wiki/Currying).

Ordinal zero
`o0`: **Ord**

    let o0 = λl s z. z;

Ordinal successor
`osucc`: **Ord** → **Ord**

    let osucc = λα l s z. s (α l s z);

We define limits using a function which takes an index and returns the ordinal
at that index in the fundamental sequence.
`olim`: (**N** → **Ord**) → **Ord**

    let olim = λf l s z. l (λi. f i l s z);

Converting a Church integer to an ordinal integer is easy (again we optimize for bits):
`to_ord`: **N** → **Ord**

    # let to_ord = λn. n osucc o0;
    let to_ord = λn l. n; # optimized

`o1`, `o2`: **Ord**

    let o1 = to_ord c1;
    let o2 = to_ord c2;

The first infinite ordinal
`ω`: **Ord**

    #let ω = olim to_ord; # Straightforward definition
    let ω = λl s z. l (λi. i s z); # Optimized definition

Next we need ordinal arithmetic. We reverse the arguments of our ordinal arithmetic functions
so that partial application is more useful.

Almost all of the **Ord** → **Ord** functions we define here are continuous.
Defining a continuous function is easy with this representation, just
pass `olim` as the first argument. For example, ordinal addition (in which α + 0 = α,
α + (β + 1) = (α + β) + 1) we define as
`oadd`: **Ord** → **Ord** → **Ord**

    # let oadd = λβ α. β olim osucc α;
    let oadd = λβ. β olim osucc; # Optimized

Ordinal multiplication α * 0 = 0, α * (β + 1) = (α * β) + α as
`omul`: **Ord** → **Ord** → **Ord**

    let omul = λβ α. β olim (oadd α) o0;

and powers α^0 = 1, α^{β + 1} = α^β * α as
`opow`: **Ord** → **Ord** → **Ord**

    let opow = λβ α. β olim (omul α) o1;

With these we can define ordinals like ω^ω^ω + ω^ω2 + 4. To go further,
we define an operator that takes fixed points, given a starting point *α* and a normal function
*F*:
`fixedp`: (**Ord** → **Ord**) → **Ord** → **Ord**

    let fixedp = λf α. olim λn. n f α;

At this point it's handy to define the [C
combinator](https://en.wikipedia.org/wiki/B,_C,_K,_W_system) which swaps arguments:
`C`: (**T** → **U** → **V**) → (**U** → **T** → **V**)

        let C = λf x y. f y x;

which allows us to define
`epsilon0`: **Ord**

    let epsilon0 = fixedp (C opow ω) o0;

If `f α` finds the least ordinal no less than `α` with some property, `stepfix` enumerates the
solutions by ordinal (where this is continuous); to get the successor value, add one to the value
you have and search again.
`stepfix`: (**Ord** → **Ord**) → **Ord** → **Ord**

    let stepfix = λf α. α olim (λp. f (osucc p)) (f o0);

Putting these together we can take derivatives.
`deriv`: (**Ord** → **Ord**) → **Ord** → **Ord**

    let deriv = λf. stepfix (fixedp f);

Two-argument [Veblen function](https://en.wikipedia.org/wiki/Veblen_function). Note the caution in
Paul Budnik, [An overview of the ordinal
calculator](https://www.mtnmath.com/ord/ordinalarith.pdf): "if the least significant parameter is a
successor and the the next least significant parameter is a limit, one must exercise care to make
sure both parameters affect the result" (thanks to [John
Baez](https://twitter.com/ciphergoth/status/1234653144082042880)). For a limit ordinal γ, one
cannot assume that φ\_γ(α + 1) = \\lim\_{β<γ} φ\_γ(α); see this paper for a counterexample.
Instead, one must explicitly find new fixed points for every
function in the limit sequence, starting from the previous fixed point found for the whole limit
function.

Because this takes two arguments, it recursively builds an **Ord** → **Ord** function. At zero
this function is just *x* → ω^*x*. The successor of each function is the derivative.
For the limit, the variable `lf` in the lambda below is of type **N** → **Ord** → **Ord**,
and we must return an **Ord** → **Ord**. Bearing in mind the above caution, we use `stepfix` to
step through the limit fixed points.
`veblen2`: **Ord** → **Ord** → **Ord**

    let veblen2 = λα. α
        (λlf. stepfix λostart. olim λn. fixedp (lf n) ostart)
        deriv
        (C opow ω);

By taking fixed points one more time, we can enumerate solutions of `x = veblen2 x o0` and thus
define the Feferman-Schütte ordinal Γ\_0
`feferman_schuette`: **Ord**

    let feferman_schuette = deriv (C veblen2 o0) o0;

Now that we have some ordinals, we can define the fast-growing hierarchy `fgh`: **Ord** → **N** → **N**

    let fgh = λ α. α (λlf n. lf n n) (λ f n. n f n) csucc;

And with that we're finally ready to write some programs which reduce to Church integers.

    let f_0 = fgh o0 c4;
    draw f_0;

    let f_1 = fgh o1 c4;
    draw f_1;

    let f_2 = fgh o2 c4;
    draw f_2;

    let f_omega = fgh ω c4;
    draw f_omega;

    let f_omega1 = fgh (osucc ω) c4;
    draw f_omega1;

    let f_e0 = fgh (osucc epsilon0) c4;
    draw f_e0;

But we didn't build all this just to define pocket calculator stuff like `fgh (osucc epsilon0) c4`.
Let's use our biggest ordinal so far, the Feferman-Schütte ordinal:

    let f_FS = fgh (osucc (osucc feferman_schuette)) c3;
    draw f_FS;

This is larger than many numbers on the [Googology
Wiki](https://googology.wikia.org/wiki/Googology_Wiki); consider for example that [Graham's
Number](https://googology.wikia.org/wiki/Graham%27s_number) is approximated there as
`fgh (osucc omega) c64` (where of course `c64 = c3 c4`).

We can of course go on to define larger ordinals like this (eg by taking derivatives)
and thus larger integers, but the next ordinal that is different in kind is the small Veblen
ordinal, followed by the large Veblen ordinal. I haven't tried to define these because I don't
fully understand them yet; there's room to express even vaster numbers with this system.

## Copyright notice

Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
