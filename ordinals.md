# Representation of ordinals in lambda calculus

The file `demofiles/f_fs.olc` contains a function which represents the fast-growing-function applied to an ordinal related to the Feferman-Schütte ordinal. As far as I know, the way that ordinals are represented in lambda calculus in that file is original.

In what follows we use *Ord* to refer only to the set of ordinals we can represent using the notation we define here. All ordinals will have limit sequences.

My first cut at representing ordinals in lambda calculus involved representing the three types of ordinals with standard lambda calculus constructions for structures and discriminated unions. However there's a cleaner way, that more neatly captures the things I want to compute here.

Supposing we want to define a function from *Ord* to some type *T* ie *F: Ord -> T*. We'll typically do that by specifying three things, *z*, *s*, and *l*:

* *F(0)*, the value of the function at zero; we'll call this *z*, and it's of type *T* ie *z: T*
* the value of *F(α + 1)*, given *F(α)*; we'll call this *s: T -> T*
* the value of *F(α)* where *α* is a limit ordinal,
given the values of *F* on the limit sequence ie *F(α[0])*, *F(α[1])*, *F(α[2])*. We'll call this *l*, and say that it's passed a function which returns *F(α[i])* for any *i*, where *i* is an integer in Church representation, ie *l: (N -> T) -> T*.

In this representation, given an ordinal *α* and a function on ordinals *F* represented as the three values *z*, *s*, and *l*, we can find *F(α)* by passing the three functions to the ordinal, ie *α z s l*. This means that the type of an ordinal is *T -> (T -> T) -> ((N -> T) -> T) -> T*.

Much like Church notation, the representation of ordinal zero is therefore just `λz s l. z`, while one is `λz s l. s z` and two is `λz s l. s (s z)`; in general the successor of `α` is `λz s l. s (α z s l)`. For ω as for any limit ordinal, we pass in a function that calculates *F* for any entry in its limit sequence: `λz s l. l (λi. i s z)`. More generally, we define a representation of ordinal zero `o0`, a function `osucc` that finds the successor of an ordinal of type *Ord -> Ord* which finds the successor of an ordinal, and a function `olim` which returns a limit ordinal given a limit sequence: *(N -> Ord) -> Ord*.

    let o0 = λz s l. z;
    let osucc = λo z s l. s (o z s l);
    let olim = λf z s l. l (λi. f i z s l);

This representation makes common functions on ordinals very clean and concise.
