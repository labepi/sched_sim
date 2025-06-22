#include <stdio.h>
#include <stdlib.h>
#include "queue.h"
#include "proc.h"
#include "stats.h"
#include "utils.h"

extern struct queue * ready;
extern struct queue * ready2;
extern struct queue * blocked;
extern struct queue * finished;
extern int MAX_TIME;

struct proc * scheduler(struct proc * current) {
    struct proc * selected = NULL;

    if (current != NULL) {
        int limiar = (int)(0.2 * MAX_TIME);
        if (current->remaining_time <= limiar) {
            enqueue(ready, current);
            current->queue = 0;
        } else {
            enqueue(ready2, current);
            current->queue = 1;
        }

        if (current->state == READY)
            count_ready_in(current);
        else if (current->state == BLOCKED)
            count_blocked_in(current);
        else if (current->state == FINISHED)
            count_finished_in(current);
    }

    if (isempty(ready) && isempty(ready2)) return NULL;

    int r = rand() % 100;
    int fila = (isempty(ready)) ? 1 : (isempty(ready2)) ? 0 : (r < 80 ? 0 : 1);

    selected = (fila == 0) ? dequeue(ready) : dequeue(ready2);
    if (selected) {
        count_ready_out(selected);
        selected->state = RUNNING;
    }
    return selected;
}
