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

        switch (current->state) {
            case READY:
            case BLOCKED:
                if (current->remaining_time <= limiar) {
                    enqueue(ready, current);
                    current->queue = 0;
                    (current->state == READY) ? count_ready_in(current) : count_blocked_in(current);
                } else {
                    enqueue(ready2, current);
                    current->queue = 1;
                    (current->state == READY) ? count_ready_in(current) : count_blocked_in(current);
                }
                break;
            case FINISHED:
                enqueue(finished, current);
                count_finished_in(current);
                break;
            default:
                printf("@@ ERRO no estado de saída do processo %d\n", current->pid);
        }
    }

    if (isempty(ready) && isempty(ready2))
        return NULL;

    int fila_escolhida;
    int r = rand() % 100;

    if (isempty(ready))
        fila_escolhida = 1;
    else if (isempty(ready2))
        fila_escolhida = 0;
    else
        fila_escolhida = (r < 80) ? 0 : 1;

    selected = (fila_escolhida == 0) ? dequeue(ready) : dequeue(ready2);

    if (selected) {
        count_ready_out(selected);
        selected->state = RUNNING;
    }

    return selected;
}
