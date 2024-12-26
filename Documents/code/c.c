#include <stdio.h>
int main() {
    struct book {
        char name[25];
        char author[25];
        int callno;
    };
    struct book b1 = { "Let us C", "ABC", 101 };
    struct book *ptr;
    ptr = &b1;
    printf("Address of b1: %p\n", &b1);
    return 0;
}