Start here: [Large Countable Ordinals](https://johncarlosbaez.wordpress.com/2016/07/07/large-countable-ordinals-part-3/) by John Baez.

Church integers
c0, c1... : N

    let c0 = λf x. x;
    let c1 = λx. x;
    let c2 = λf x. f (f x);
    let c3 = λf x. f (f (f x));
    let c4 = λf x. f (f (f (f x)));

csucc: N -> N

    let csucc = λn f x. n f (f x);


A function F on ordinals we define in three parts z s l:
* F(0) = z
* F(α + 1) = s F(α)
* F(α) = l (λi. F(α[i])) where α is a limit ordinal

We express an ordinal as a thing that calculates F given z s l

* F(α) = α z s l

Let T be whatever type F returns

* F: Ord -> T
* z: T
* s: T -> T
* l: (N -> T) -> T
* Ord = T -> (T -> T) -> ((N -> T) -> T) -> T

o0: Ord

    let o0 = λz s l. z;

osucc: Ord -> Ord

    let osucc = λα z s l. s (α z s l);

olim: (N -> Ord) -> Ord

    let olim = λf z s l. l (λi. f i z s l);

Finite numbers
to_ord: N -> Ord

    # let to_ord = λn. n osucc o0;
    let to_ord = λn z s l. n s z; # optimized

o1, o2: Ord

    let o1 = to_ord c1;
    let o2 = to_ord c2;

ω: Ord

    #let ω = olim to_ord; # Straightforward definition
    let ω = λz s l. l (λi. i s z); # Optimized definition

For a continuous function, where α is a limit ordinal
F(α)[n] = F(α[n])
so l is just olim

α + 0 = α, α + (β + 1) = (α + β) + 1

oadd: Ord -> Ord -> Ord


    let oadd = λα β. β α osucc olim;

C combinator, swap arguments to function

    let C = λf x y. f y x;

α * 0 = 0, α * (β + 1) = (α * β) + α

omul: Ord -> Ord -> Ord

    let omul = λα β. β o0 (C oadd α) olim;

α^0 = 1, α^{β + 1} = α^β * α

opow: Ord -> Ord -> Ord

    let opow = λα β. β o1 (C omul α) olim;

First fixed point of f >= α where f strictly increasing, continuous
fixedp: (Ord -> Ord) -> Ord -> Ord

    let fixedp = λf α. olim λn. n f α;

epsilon0: Ord

    let epsilon0 = fixedp (opow ω) o0;

stepfix (fixedp f) α = α'th fixed point of f
stepfix: (Ord -> Ord) -> Ord -> Ord
stepfix f o0 = f o0
stepfix f (osucc α) = f (osucc (stepfix f α))

    let stepfix = λf α. α (f o0) (λp. f (osucc p)) olim;

Derivative of f, enumerates solutions of x = f x
deriv: (Ord -> Ord) -> (Ord -> Ord)

    let deriv = λf. stepfix (fixedp f);

Two-argument Veblen function
veblen2: Ord -> Ord -> Ord

    let veblen2 = λα. α
        (opow ω)
        deriv
        (λlf. stepfix (λostart. olim λn. fixedp (lf n) ostart)); # lf: N -> Ord -> Ord

fast-growing hierarchy
fgh: Ord -> N -> N

    let fgh = λ α. α csucc (λ f n. n f n) (λlf n. lf n n);

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

Enumerate solutions of x = veblen2 x o0

    let feferman_schuette = deriv (C veblen2 o0);

Finally, make a really big number out of all this :)

    let f_FS = fgh (osucc (feferman_schuette ω)) c3;
    draw f_FS;

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