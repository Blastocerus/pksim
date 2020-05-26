[![Run on Repl.it](https://repl.it/badge/github/Blastocerus/pksim)](https://repl.it/github/Blastocerus/pksim)

# pksim

[Finite
difference](https://en.wikipedia.org/wiki/Finite_difference_method)
implementation of pharmacokinetical modelling.

These programs are aimed at a digital laboratory course in
pharmaceutics. The basic requirement is that they are easlily
accessible with any computational device regardless of its operation
system.

This goal could be achieved with a static website powered by HTML5 and
Javascript. However, in case that a student might show some interst in
the implementation of pharmacokinetical simulations,
[Python](https://python.org) code would me much more amenable.

The numerical solution approch to the underlying system of
differential equations is valid for linear and non-linear models.


# general model



## compartments

In order to keep the model simple and general, we will in this
application extend the definition of compartments to fictious dosage
and waste compartments.

Compartments are modeled by 
- *name*,
- *volume of distribution*,
- *dosing scheme*

## dosing schemes

A **dosis scheme** is an array of *time points* and *doses*. A **dose**
is generally defined as a *liberation function* of *mass API* over
*time*. Given the numeric means of integration in minute steps, the
liberation function may also be expressed discontinually,by an array of *masses* in
minute steps.

Special and common *doses* are

- bolus input (defined by *dose* $`D`$ and an optional *lag time*
  $`t_l`$, $`l`$ for *liberation*),
  ```math
  d(t) = D\cdot\delta_{t t_l}
  ```
- zero order input (defined by *dose* $`D`$ and *velocity constant* $`k`$),
- first order input (defined by *dose* $`D`$ and *velocity constant* $`k`$),




## transitions

A **transition** describes the kinetics with which the API flows from
one *compartment* to another. Common *transition types* are

- *first order*
- *zero order*
- *immediate*


### first order transition

The *transition* of linear pharmacokinetics. 

```math
\frac{dA}{dt} = - k \cdot A
```

### transition matrix

# special situations

## one compartment with extravasal 

