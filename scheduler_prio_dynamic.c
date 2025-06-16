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

    // Realimentação: se o processo atual terminou ou foi bloqueado/preemptado
    if (current != NULL) {
        if (current->state == BLOCKED) {
            // Processo foi bloqueado (E/S), volta para fila 1 (ready)
            current->queue = 0;
            queue_push(ready, current);
        } else if (current->state == READY) {
            // Processo foi preemptado, volta para fila 2 (ready2)
            current->queue = 1;
            queue_push(ready2, current);
        } else if (current->state == FINISHED) {
            // Processo terminou, vai para fila de finalizados
            queue_push(finished, current);
        }
        // Se estiver rodando, não faz nada (continua)
    }

    // Seleção de fila com probabilidade: 80% ready, 20% ready2
    int prob = rand() % 100;
    if ((prob < 80 && !queue_empty(ready)) || queue_empty(ready2)) {
        // Seleciona da fila 1 (ready) se não estiver vazia
        selected = queue_pop(ready);
        if (selected)
            selected->queue = 0;
    } else if (!queue_empty(ready2)) {
        // Seleciona da fila 2 (ready2)
        selected = queue_pop(ready2);
        if (selected)
            selected->queue = 1;
    }

    return selected;
}

