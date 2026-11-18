import { describe, it, expect } from 'vitest';
import { countByStatus, completionRate, filterByStatus } from './tasks';

/**
 * Tests des fonctions utilitaires (tasks.ts)
 *
 * Ces tests sont écrits en JavaScript : même structure qu'en Python avec pytest :
 *
 *   Python (pytest)                       JavaScript (Vitest)
 *   from tasks import completionRate      import { completionRate } from './tasks';
 *   class TestCompletionRate:             describe('completionRate', () => { ... });
 *   def test_xxx():                       it('xxx', () => { ... });
 *   tasks = [...]                         const tasks = [...];
 *   assert resultat == 3                  expect(resultat).toBe(3);
 *   assert resultat == {"a": 1}           expect(resultat).toEqual({ a: 1 });
 *
 * () => { ... } est une fonction sans nom : l'équivalent d'un def.
 *
 * toBe    → compare une valeur simple (nombre, texte, booléen)
 * toEqual → compare le contenu d'un objet ou d'un tableau
 */

// =============================================================================
// PARTIE 1 : TESTS EXEMPLES (lisez-les !)
// =============================================================================

describe('countByStatus', () => {
  it('compte les tâches de chaque statut', () => {
    // ARRANGE : préparer une liste de tâches
    const tasks = [
      { status: 'todo' },
      { status: 'todo' },
      { status: 'done' },
    ];

    // ACT : appeler la fonction à tester
    const counts = countByStatus(tasks);

    // ASSERT : vérifier le résultat
    expect(counts).toEqual({ todo: 2, in_progress: 0, done: 1 });
  });

  it('renvoie des zéros pour une liste vide', () => {
    const counts = countByStatus([]);

    expect(counts).toEqual({ todo: 0, in_progress: 0, done: 0 });
  });
});

// =============================================================================
// PARTIE 2 : À VOUS ! (TP 1 - Exercice 4)
// =============================================================================
//
// Écrivez les 3 tests de completionRate().
// Pour chaque test : supprimez la ligne `throw new Error(...)`,
// puis écrivez ARRANGE / ACT / ASSERT comme dans les exemples ci-dessus.
//
// Lancer les tests : npm test

describe('completionRate', () => {
  it('calcule le pourcentage de tâches terminées', () => {
    // ARRANGE : 4 tâches, dont 2 avec le statut 'done'
    const tasks = [
      { status: 'todo' },
      { status: 'in_progress' },
      { status: 'done' },
      { status: 'done' },
    ];

    // ACT
    const rate = completionRate(tasks);

    // ASSERT
    expect(rate).toBe(50);
  });

  it('renvoie 100 quand toutes les tâches sont terminées', () => {
    // ARRANGE
    const tasks = [
      { status: 'done' },
      { status: 'done' },
    ];

    // ACT : appeler completionRate(tasks)
    const rate = completionRate(tasks);

    // ASSERT : le résultat doit valoir 100
    expect(rate).toBe(100);
  });

  it('renvoie 0 pour une liste vide', () => {
    // ARRANGE
    const tasks = [];

    // ACT
    const rate = completionRate(tasks);

    // ASSERT
    expect(rate).toBe(0);
  });
});

// =============================================================================
// BONUS (TDD) : filterByStatus()
// =============================================================================

describe('filterByStatus', () => {
  it('renvoie seulement les tâches terminées', () => {
    // ARRANGE
    const tasks = [
      { id: 1, status: 'todo' },
      { id: 2, status: 'done' },
      { id: 3, status: 'in_progress' },
      { id: 4, status: 'done' },
    ];

    // ACT
    const doneTasks = filterByStatus(tasks, 'done');

    // ASSERT : un tableau → toEqual
    expect(doneTasks).toEqual([
      { id: 2, status: 'done' },
      { id: 4, status: 'done' },
    ]);
  });
});
