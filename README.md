# RS-AF - RangeSearch - Antifraude
Herramienta que permite escanear un rango determinado de IP /24 - Devolviendo y capturando aquellos que estén activos en un listado, permitiendo posteriormente, buscar patrones de búsqueda dentro de estas URL´s

<h1>Instalación:</h1>

git clone https://github.com/MisterWh1t3/RS-AF

<h1>Pasos previos:</h1>

pip install -r requirements.txt

Nota: Es fundamental también tener (json, os , platform) // Pero no está añadido en el requirements ya que da conflicto si están ya activos.

-------------------------------------------------------------------------------------------------------------------------------------------

<H2> Extracción URL´s del Archivo .JSON </H2>

cat test-210927.json | grep -o '"http://[^"]*"' 

