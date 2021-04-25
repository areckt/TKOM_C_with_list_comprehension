int[] lengthList() {
    string[] a = ["this", "is"];
    string[] b = ["example", "text"];
    string[] c = a + b;
    int[] result = [_word for word in c];
    return result;
}