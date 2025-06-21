#include <stdio.h>
#include <stdlib.h>  // necessário para rand()

#include "queue.h"
#include "proc.h"
#include "stats.h"
#include "utils.h"

extern struct queue * ready;
extern struct queue * ready2;
extern struct queue * blocked;
extern struct queue * finished;
extern int MAX_TIME;

struct proc * scheduler(struct proc * current)
{
    struct proc * selected = NULL;

    if (current != NULL) {
        if (current->state == BLOCKED) {
            current->queue = 0;
            enqueue(ready, current);
            count_ready_in(current);
        } else if (current->state == READY) {
            current->queue = 1;
            enqueue(ready2, current);
            count_ready_in(current);
        } else if (current->state == FINISHED) {
            enqueue(finished, current);
            count_finished_in(current);
        }
    }

    int prob = rand() % 100;
    if ((prob < 80 && !isempty(ready)) || isempty(ready2)) {
        selected = dequeue(ready);
        if (selected) {
            selected->queue = 0;
            count_ready_out(selected);
            selected->state = RUNNING;
        }
    } else if (!isempty(ready2)) {
        selected = dequeue(ready2);
        if (selected) {
            selected->queue = 1;
            count_ready_out(selected);
            selected->state = RUNNING;
        }
    }

    return selected;
}
