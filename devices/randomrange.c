#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "randomrange.h"

int randomrange(int lower, int upper)
{
    int num = (rand() % (upper - lower + 1)) + lower;
    return num;
}
