lint main() {
    lint nums = [1, 2, 3, 4, 5];
    lint nums2 = [6, 7, 8];

    nums = nums + nums2;

    lint res = [n*n for n in nums];
    return !res;
}
