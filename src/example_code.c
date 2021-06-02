int main(){
    int fun(int a, int b, int c){
        return a+b+c;
    }

    int i = 1;
    while (i < 15)
    {
        if (i < 10)
        {
            i = i+10;
            string str = "example";
        }
        else
        {
            return fun(1, 2, 3);
        }
    }
    return 0;
}