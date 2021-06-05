# Planning as SAT + PDDL 


## Introduzione
L'obiettivo del progetto è quello di risolvere un problema in logica proposizionale usando SAT. 
In particolare ho ideato un problema di planning -- l'area dell'intelligenza artificiale che ha come scopo quello di pianificare una sequenza di azioni per permettere ad un agente di raggiungere uno stato finale dato -- in cui un robot giardiniere deve prendersi cura di un giardino. L’ambiente considerato, riportato in Figura, è un grid-world di dimensioni 3×3 rappresentante il giardino. 

![](./images/progetto_12.png)

Nello  specifico,  ogni casella può essere: i) vuota, ii) sana (i.e., contenente piante sane), o iii) infestata (i.e.,contenente piante infestanti). Il robot giardiniere, può muoversi tra tali celle, e compiere le seguenti azioni:
1. quando si trova in una cella sana può innaffiare le piante presenti;
2. quando si trova in una cella infestata può estirpare le piante presenti.

L’obiettivo dell’agente è dunque quello di trovare un percorso che gli permetta di i) estirpare tutte le piante infestanti e, ii) innaffiare tutte quelle sane.

## SAT
- SAT (il codice sta nella cartella X e puo essere eseguito usando il solver Y, con link al solver)


## PDDL
- PDDL (il codice sta nella cartella Z e puo essere eseguito usando l'editor online W, copiando problem e domain nei rispettivi spazi, con link al solver + spiegazione di come ottenere i grafici ;) )


<br><br>

#### **Autore**: Borghini Alessia
#### **Relatore**: Prof. Maurizio Lenzerini.
