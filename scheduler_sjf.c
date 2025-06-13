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

    // Tratamento do processo que acabou de sair da execução
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

    // Se a fila de aptos está vazia, retorna NULL
    if (isempty(ready))
        return NULL;

    // SJF: Seleciona o processo com menor remaining_time
    int min_index = -1;
    int min_time = -1;
    int ready_len = length(ready);
    for (int i = 0; i < ready_len; i++) {
        struct proc * p = get(ready, i);
        if (min_index == -1 || p->remaining_time < min_time) {
            min_index = i;
            min_time = p->remaining_time;
        }
    }

    // Remove o processo selecionado da fila
    selected = remove_at(ready, min_index);

    // Estatísticas e alteração de estado
    count_ready_out(selected);
    selected->state = RUNNING;

    return selected;
}
