#include <stdio.h>

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

    if (current != NULL)
    {
        switch (current->state) 
        {
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

    if (isempty(ready))
        return NULL;

    int max_idx = -1;
    int max_time = -1;
    int qsize = length(ready);
    for (int i = 0; i < qsize; i++) {
        struct proc *p = get(ready, i);
        if (p->remaining_time > max_time) {
            max_time = p->remaining_time;
            max_idx = i;
        }
    }

    selected = remove_at(ready, max_idx);
    count_ready_out(selected);
    selected->state = RUNNING;

    return selected;
}
