# SoftwareDeSistemas_UASLP

Este repositorio contiene las practicas de laboratiorio de la materia de Software de Sistemas, culla finalidad es tener un compilador para la arquitectura de proposito academico SIC/XE. 
El plan de la materia esta disponible aquí:---> [Software de Sistemas](https://infocomp.ingenieria.uaslp.mx/cominf/public/docs/temarios/2263.pdf)

## Practica 1(Calculadora de expresiones):

## Practica 2:

Estas instrucciones especifican como empezar desde cero para tener una copia de este juego y que puedas jugarlo e incluso editarlo.

### Prerequisitos

Si tu intencion es solo jugar el juego no necesitas mas que entrar a cuelquiera de los siguientes links:

* [GigameshII](https://www.greenfoot.org/scenarios/23940?js=false/) - El primer lanzamiento (version) de las aventuras de Gigamesh II.
* [GigameshII-SR](https://github.com/Pedejeca135/Gigamesh2D) - Aqui habra un segundo lanzamiento de las aventuras de Gigamesh II.

Cabe mencionar que muchas veces el sitio web de Greenfoot no funciona correctamente y no deja jugar esta y otras joyas, por lo que si ese es el caso, recomiendo descargar el editor de Greenfoot para lo cual se necesita un sistema operaivo de 64 bits. Si no es asi puedes buscar [versiones anteriores](https://www.greenfoot.org/download_old). Tambien necesitaras una copia comprmida de este repositorio del juego. Si no sabes como hacerlo. No te preocupes, a continuación explico como.

* [Greenfoot](https://www.greenfoot.org/download) - Descarga de greenfoot para diferentes sistemas operativos.

#### Necesitaras JDK8
![java-8_Banner](https://github.com/Pedejeca135/Gigamesh2D/blob/master/ReadmeImages/java-8_Banner.png)
 

 Si no sabes si tienes instalado Java o que version de este tienes dejo este [Link a tutorial para saber que version de java tienes en tu pc](https://www.java.com/es/download/help/version_manual.xml)


#### Windows

##### Instalacion de JDK
Esta parte se tiene que hacer si no tienes java en la version 8, como se menciono antes.
Primero descarga el ejecutable de instalacion desde la [pagina de descarga del jdk8](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html). quiza necesites crear una cuenta en Oracle por sus ultimas políticas.
![pagina de descarga jdk8](https://github.com/Pedejeca135/Gigamesh2D/blob/master/ReadmeImages/sdk1.PNG)


Despues de esto, en el archivo descargado hacemos click derecho y luego en el menu contextual clickear donde dice ejecutar como administrador.


![intalacion jdk](https://github.com/Pedejeca135/Gigamesh2D/blob/master/ReadmeImages/sdk2.PNG)


##### Instalacion Greefoot
Lo primero que tienes que hacer es ir al [Link de descarga](https://www.greenfoot.org/download) y descargar el instalador .msi para Windows.  


![descarga greenfoot windows](https://github.com/Pedejeca135/Gigamesh2D/blob/master/ReadmeImages/windows1.PNG)

Lo segundo es dar click derecho en el archivo descargado y en el menú contextual dar click en instalar.


![instalacion greenfoot windows](https://github.com/Pedejeca135/Gigamesh2D/blob/master/ReadmeImages/installing_greenfoot1.PNG)

Emergera una ventana que te ira guiando. clickeamos next.


![instalacion greenfoot windows](https://github.com/Pedejeca135/Gigamesh2D/blob/master/ReadmeImages/installing_greenfoot2.PNG)

Lo siguiente es elegir los usuarios en los que se istalara greenfoot. Depende de ti.


![instalacion greenfoot windows](https://github.com/Pedejeca135/Gigamesh2D/blob/master/ReadmeImages/installing_greenfoot3.PNG)

Despues hay que decidir si se quiere asociar los tipos de archivo ".gfar" y ".greenfoot" a el programa en instalacion, que es lo mas recomendable. Tambien hay que elegir los accesos directos que queremos tener.


![instalacion greenfoot windows](https://github.com/Pedejeca135/Gigamesh2D/blob/master/ReadmeImages/installing_greenfoot4.PNG)

Elegiremos el folder de destino, el que esta por default es el recomendado.


![instalacion greenfoot windows](https://github.com/Pedejeca135/Gigamesh2D/blob/master/ReadmeImages/installing_greenfoot5.PNG)

Finalmente pushamos en instalar y finalizar.


![instalacion greenfoot windows](https://github.com/Pedejeca135/Gigamesh2D/blob/master/ReadmeImages/installing_greenfoot6.PNG)

##### Probando el videojuego
Para tener el videojuego en tu computadora basta con  hacer click en  el boton verde de arriba que dice "Clone or download" y descargar el comprimido .zip del projecto, ubicarlo y descomprimirlo.
Si tienes [git](https://git-scm.com/download) puedes clonar el repositorio desde la terminal usandocomandos git.

Para pobar que todo funciona bien, teniendo ya instalado correctamente Greenfoot. En la carpeta del repositorio descargado hay que buscar el archivo project.greenfoot y dar doble click.

Listo ahora puedes jugar las aventuras de GigameshII solo o con un amigo e incluso editar el codigo.

#### Ubuntu-Debian
Antes de hacer cualquier instalación siempre es recomendable actualizar el sistema.
```
$ sudo apt update
```
```
$ sudo apt upgrade
```
##### Instalacion de JDK
Para saber si ya tienes java instalado y la version del mismo.
```
$ java -version
```
Si java no esta instalado aparecera algo como:
```
Output:
Command 'java' not found, but can be installed with:

apt install default-jre
apt install openjdk-11-jre-headless
apt install openjdk-9-jre-headless
apt install openjdk-8-jre-headless
```
Ejecuta el siguiente comando para instalar el Java Runtime enviroment(JRE). que permite ejecutar el software de java.
```
$ sudo apt install default-jre
```

puedes volver a verificar la instalacion con:
```
$ java -version
```
Ahora necesitaremos instalar el kit de desarrollo de Java (JDK) además de JRE para compilar y ejecutar programas basados en Java. 
```
$ sudo apt install default-jdk
```
La instalacion de JDK se puede verificar con la vercion del compilador de java o javac.
```
$ javac -version
```

Hasta ahora hemos instalado la version por default que para la fecha de este commit es la 11(java11).Lo proximo por hacer consiste en instalar la version de java que greenfoot utiliza(java8). Para ello ejecute el siguiente comando:
```
$ sudo apt install openjdk-8-jdk
```
listo, ahora hay que instalar el software de greenfoot.

##### Instalacion Greefoot

Lo primero que tienes que hacer es ir al [Link de descarga](https://www.greenfoot.org/download) , y descargar el archivo .deb para Ubuntu-Debian. 

Ubicamos el archivo abrimos una terminal y ponemos el siguiente comando:

```
$ sudo dpkg -i Greenfoot-linux-361.deb
```
##### Probando el videojuego
Para tener el projecto en tu computadora puedes descargar el comprimido .zip pero yo recomiendo que si no tienes git lo instales con el comando:
```
$ sudo apt install git
```
A continuacion clonar el repositorio con el comando:
```
$ git clone https://github.com/Pedejeca135/Gigamesh2D.git
```
Finalmente, para pobar que todo funciona bien, teniendo ya instalado correctamente Greenfoot, y teniendo la carpeta de trabajo del videojuego, tenemos que dar permisos de ejecucion a todos los archivos dentro, por lo que tiene que ser recursivo(-R).
Se tiene que ubicar la carpeta del projecto y en su folder padre hacer el siguiente comando:
```
$ sudo chmod -R 777 Gigamesh2D/
```
Ahora puedes abrir el Escenario de Gigamesh2D desde la aplicacion de greenfoot.

Listo ahora puedes jugar las aventuras de GigameshII solo o con un amigo e incluso editar el codigo.

#### Mac OS X
##### Instalacion de JDK
##### Instalacion Greefoot
##### Probando el videojuego
No hay presupuesto. 

[Hacer tutorial](https://github.com/Pedejeca135/Gigamesh2D/pulls).

### Mas informacion sobre la instalacion

[Installing Greenfoot](https://www.greenfoot.org/download/installation)


[Greenfoot FAQ](https://www.greenfoot.org/doc/faq)



## Hecho con

* [Greenfoot](https://www.greenfoot.org/door) - El framework usado.

* [JAVA8](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) - Greenfoot necesita java en su version 8.


## Versiones

Cuenta con varias versiones. Para mas informacion revisar los [tags](https://github.com/Pedejeca135/Gigamesh2D) en la seccion de Branchs.

## Autoría

* **Pedro Cantú** [Pedejeca135](https://github.com/Pedejeca135)

* **Fernando Mendoza** - *Primera fase* - [FerMendoza123](https://github.com/FerMendoza123)

## Colaboracion
Este projecto esta abierto a pull-request y aportes por parte de la comunidad, tanto diseño gráfico como codigo. No olvides poner tu nombre y fecha de edicion en el codigo, para que los que vean en un futuro el codigo sepan tu aporte.

## Contacto
Si quieres ser parte del proximo lanzamiento, en el que puede que se utilizen los nombres reales de los Heroes de esta fantastica Epopeya, tienes ideas, quieres felicitarme o simplemente tienes problemas con algo referente a este pequeño projecto puedes mandarme un correo a la direccion [pjco90@hotmail.com].

## Licencia
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

Puedes usar parcial o totalmente el codigo en otros projectos y repositorios, asi como las imagenes dando el respectivo credito.
No puedes usar los nombres Gigamesh ni Enkibit.

## Reconocimientos

* [Eloy Hernández](https://github.com/eloyhz) (Profesor).
