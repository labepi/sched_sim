#include <stdio.h>

#include "queue.h" // contem funções uteis para filas
#include "proc.h"  // possui as funções dos processos
#include "stats.h" // possui as funções de estatisticas 
#include "utils.h" // possui funções uteis 

// Utilizando as variáveis globais definidas no 'main'
extern struct queue * ready;    // fila de aptos
extern struct queue * ready2;   // segunda fila de aptos
extern struct queue * blocked;  // fila de bloqueados
extern struct queue * finished; // fila de finalizados
// NOTE: essa fila de finalizados é utilizada apenas para
// as estatisticas finais

// variavel global que indica o tempo maximo que um processo pode executar ao todo
extern int MAX_TIME;

struct proc * scheduler(struct proc * current)
{
    struct proc * selected = NULL;

    /*
     *   Tratando o processo que está atualmente executando
     */
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

    /*
     *   Estratégia de seleção de um novo processo para executar (LJF)
     */
    if (isempty(ready))
    {
        return NULL;
    }

    // Procurar o processo com maior remaining_time na fila ready
    int max_idx = -1;
    int max_time = -1;
    int qsize = queue_size(ready);
    for (int i = 0; i < qsize; i++) {
        struct proc *p = queue_get(ready, i);
        if (p->remaining_time > max_time) {
            max_time = p->remaining_time;
            max_idx = i;
        }
    }

    // Remover o processo selecionado da fila
    selected = remove_at(ready, max_idx);

    // Estatísticas e alteração de estado
    count_ready_out(selected);
    selected->state = RUNNING;

    return selected;
}

