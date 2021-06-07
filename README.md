# Planning as SAT + PDDL 


## Introduzione
L'obiettivo del progetto è quello di risolvere un problema in logica proposizionale usando SAT. 
In particolare ho ideato un problema di planning – l'area dell'intelligenza artificiale che ha come scopo quello di pianificare una sequenza di azioni per permettere ad un agente di raggiungere uno stato finale dato – in cui un robot giardiniere deve prendersi cura di un giardino. L’ambiente considerato, riportato in Figura, è un grid-world di dimensioni 3×3 rappresentante il giardino. 

![](./images/progetto_12.png)

Nello  specifico,  ogni casella può essere: i) vuota, ii) sana (i.e., contenente piante sane), o iii) infestata (i.e.,contenente piante infestanti). Il robot giardiniere, può muoversi tra tali celle, e compiere le seguenti azioni:
1. quando si trova in una cella sana può innaffiare le piante presenti;
2. quando si trova in una cella infestata può estirpare le piante presenti.

L’obiettivo dell’agente è dunque quello di trovare un percorso che gli permetta di i) estirpare tutte le piante infestanti e, ii) innaffiare tutte quelle sane.
Per ulteriori dettagli vedere il file "Planning_as_SAT.pdf".

## SAT
Nella cartella SAT sono presenti i file necessari per risolvere il problema come SAT.
Per poter eseguire il file "solve.py", che trova il piano risolutivo, è necessario installare il Solver PySAT, che è disponibile al link https://github.com/pysathq/pysat.
Il piano risultante viene salvato nel file "report.txt".


## PDDL
Gli script PDDL sono presenti nella cartella PDDL. Per provare i file è sufficiente importare i file "domain.pddl" e "problem.pddl" nelle apposite sezioni del solver online al link https://web-planner.herokuapp.com/, che risolverà il problema restituendo il percorso trovato.

<br><br>

#### **Autore**: Alessia Borghini
#### **Relatore**: Prof. Maurizio Lenzerini.
