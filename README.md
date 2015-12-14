Generátor poslechových statistik pro Bandzone.cz
============

(No english, as this is intended to be used by czechs for czech website)

Jednoduchý generátor statistik, respektive grafů návštěvnosti a poslechovosti jednotlivých písní na bandzone.cz profilech. 

Závislosti:
---
- python3
- BeautifulSoup
- gnuplot
- schopný uživatel, který to rozchodí

Použití:
---
1. vytvořit složku pro data (například ~/bzstat)
1. upravit zdrojáky a nastavit proměnné **bandurl**, **sofile** a **datfile**:
    - **bandurl** = "adresa profilu" *(například http://bandzone.cz/vetryslecnypetry)*
    - **sofile** = "složka pro data/sofile" *(například ~/bzstat/sofile)
    - **datfile** = "složka pro data/datfile" *(například ~/bzstat/datfile)
2. Nastavit každodenní (0:00) spouštění následujícího příkazu: **./bzstats.py | gnuplot > /kam/vrazit/vysledek.svg**

    
    Například cronem: 

        0 0 * * * ./bzstats.py | gnuplot > /var/www/vspstats.svg

    
4. Kochat se, jak ty sračky nikdo neposlouchá
5. Divit se, že je to poněkud nehotové
