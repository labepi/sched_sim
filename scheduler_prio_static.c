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

struct proc * scheduler(struct proc * current)
{
    struct proc * selected = NULL;

    // Tratamento do processo que estava executando
    if (current != NULL) {
        switch (current->state) {
            case READY:
            case BLOCKED: {
                // Decide a fila de acordo com o remaining_time
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

    // Seleção do próximo processo
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
        if (selected->queue == 0)
            count_ready_out(selected);
        else
            count_ready_out(selected); // pode usar a mesma função para estatística
        selected->state = RUNNING;
    }

    return selected;
}
// NOTE: essa fila de finalizados é utilizada apenas para
// as estatisticas finais

// variavel global que indica o tempo maximo que um processo pode executar ao todo
extern int MAX_TIME;

struct proc * scheduler(struct proc * current)
{
    struct proc * selected; 

    return NULL;
}

