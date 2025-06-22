#include <stdio.h>
#include "queue.h"
#include "proc.h"
#include "stats.h"
#include "utils.h"

extern struct queue * ready;
extern struct queue * blocked;
extern struct queue * finished;

struct proc * scheduler(struct proc * current) {
    struct proc * selected = NULL;

    if (current != NULL) {
        // Se o processo já terminou, não o insere novamente
        if (current->remaining_time <= 0) {
            current->state = FINISHED;
        }

        switch (current->state) {
            case READY:
                if (current->remaining_time > 0) {
                    enqueue(ready, current);
                    count_ready_in(current);
                } else {
                    enqueue(finished, current);
                    count_finished_in(current);
                }
                break;

            case BLOCKED:
                enqueue(blocked, current);
                count_blocked_in(current);
                break;

            case FINISHED:
                enqueue(finished, current);
                count_finished_in(current);
                break;

            default:
                printf("@@ ERRO no estado de saída do processo %d\n", current->pid);
        }
    }

    if (isempty(ready)) return NULL;

    int min_index = -1;
    int min_time = -1;
    int len = length(ready);

    for (int i = 0; i < len; i++) {
        struct proc * p = get(ready, i);

        // Garante que só pega processo com tempo restante positivo
        if (p && p->remaining_time > 0 && (min_index == -1 || p->remaining_time < min_time)) {
            min_index = i;
            min_time = p->remaining_time;
        }
    }

    // Fallback: se não achar nenhum válido (caso raro), tenta tirar o primeiro
    if (min_index == -1) {
        for (int i = 0; i < len; i++) {
            struct proc * p = get(ready, i);
            if (p != NULL) {
                selected = remove_at(ready, i);
                break;
            }
        }
    } else {
        selected = remove_at(ready, min_index);
    }

    if (selected) {
        selected->state = RUNNING;
        count_ready_out(selected);
    }

    return selected;
}
