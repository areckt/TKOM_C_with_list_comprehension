int main() {

    # PONIZSZY KOD NIE ROBI NIC SZCZEGÓLNEGO
    # TEN PRZYKLAD MA TYLKO POKAZAC SKLADNIE JEZYKA

    int a = 5;                              # int declaration
    a = 3*(a + 2 * (1 - a));                # int assignment

    float b = 4.5;                          # float declaration
    b = b / (b * 0.1 + 2.4);                # float assignment

    string c = "Hello";                     # string declaration
    c = c + ", World";                      # string assignment

    lint d = [1, 2, 3];                     # lint declaration
    d = [a, d[0], 2*4];                     # lint assignment

    lint e = [num * num for num in d];      # lint list comprehension declaration
    e = [-2 * num for num in e];            # lint list comprehension assignment

    lfloat f = [1.1, -4.2, 2.4];            # lfloat declaration
    f = [f[a+10], 0.4, 5.5];                # lfloat assignment

    lfloat g = [b * fnum for fnum in f];    # lfloat list comprehension declaration
    g = [9.9 * fnum for fnum in g];         # lfloat list comprehension assignment

    lstring h = ["Hello", ",", " "];        # lstring declaration
    h = [h[0], h[1], h[2], "World"];        # lstring assignment

    lstring i = ["Hey"+s for s in h];       # lstring list comprehension declaration
    i = [word + "!" for word in i];         # lstring list comprehension assignment

    if (a < 10) {                           # if statement
        return a;
    }
    else {                                  # else statement
        a = a + a;
    }

    while (a > 5) {                         # while statement
        a = a - 1;
    }

    return a;                               # return variable with matching type (int main => return int)
}