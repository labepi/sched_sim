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
extern int QUANTUM;

struct proc * scheduler(struct proc * current)
{
    struct proc * selected = NULL;

    if (current != NULL) {
        if (current->state == BLOCKED) {
            current->queue = 0;
            enqueue(ready, current);
        } else if (current->state == READY) {
            // Simula quantum usado (substitua se tiver o campo correto)
            int quantum_usado = rand() % QUANTUM;

            if (quantum_usado >= QUANTUM / 2) {
                current->queue = 0;
                enqueue(ready, current);
            } else {
                current->queue = 1;
                enqueue(ready2, current);
            }
        } else if (current->state == FINISHED) {
            enqueue(finished, current);
        }
    }

    int prob = rand() % 100;
    if ((prob < 80 && !isempty(ready)) || isempty(ready2)) {
        selected = dequeue(ready);
        if (selected)
            selected->queue = 0;
    } else if (!isempty(ready2)) {
        selected = dequeue(ready2);
        if (selected)
            selected->queue = 1;
    }

    return selected;
}
