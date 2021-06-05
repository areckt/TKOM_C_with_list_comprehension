int main(){
    int n = 8;
    if (n <= 2){
        return 1;
    }

    int prev = 1;
    int result = 1;
    int i = 0;

    while (i < n-2) {
        result = result + prev;
        prev = result - prev;
        i = i + 1;
    }
    return result;
}