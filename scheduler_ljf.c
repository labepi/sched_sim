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
        switch (current->state) {
            case READY:
                enqueue(ready, current);
                count_ready_in(current);
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

    int max_index = -1, max_time = -1, len = length(ready);
    for (int i = 0; i < len; i++) {
        struct proc * p = get(ready, i);
        if (max_index == -1 || p->remaining_time > max_time) {
            max_index = i;
            max_time = p->remaining_time;
        }
    }

    selected = remove_at(ready, max_index);
    count_ready_out(selected);
    selected->state = RUNNING;
    return selected;
}
