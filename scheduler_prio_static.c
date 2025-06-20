#include <stdio.h>
#include <stdlib.h>  // necessário para rand()

#include "queue.h"
#include "proc.h"
#include "stats.h"
#include "utils.h"

// Variáveis globais
extern struct queue * ready;
extern struct queue * ready2;
extern struct queue * blocked;
extern struct queue * finished;
extern int MAX_TIME;

struct proc * scheduler(struct proc * current)
{
    struct proc * selected = NULL;

    if (current != NULL) {
        switch (current->state) {
            case READY:
            case BLOCKED: {
                int limiar = (int)(0.2 * MAX_TIME);
                if (current->remaining_time <= limiar) {
                    enqueue(ready, current);
                    current->queue = 0;
                    if (current->state == READY)
                        count_ready_in(current);
                    else
                        count_blocked_in(current);
                } else {
                    enqueue(ready2, current);
                    current->queue = 1;
                    if (current->state == READY)
                        count_ready_in(current);
                    else
                        count_blocked_in(current);
                }
                break;
            }
            case FINISHED:
                enqueue(finished, current);
                count_finished_in(current);
                break;
            default:
                printf("@@ ERRO no estado de saída do processo %d\n", current->pid);
        }
    }

    // Escolha da fila de forma probabilística
    int fila_escolhida = 0;
    int r = rand() % 100;
    if (isempty(ready) && isempty(ready2)) {
        return NULL;
    }
    if (isempty(ready)) {
        fila_escolhida = 1;
    } else if (isempty(ready2)) {
        fila_escolhida = 0;
    } else {
        fila_escolhida = (r < 80) ? 0 : 1;
    }

    if (fila_escolhida == 0) {
        selected = dequeue(ready);
    } else {
        selected = dequeue(ready2);
    }

    if (selected) {
        count_ready_out(selected);  // usar a mesma função
        selected->state = RUNNING;
    }

    return selected;
}
