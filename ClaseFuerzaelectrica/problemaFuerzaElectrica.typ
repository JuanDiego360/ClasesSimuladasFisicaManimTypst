// mostrar la ecuación con solo el número
#show ref: it => {
  let eq = math.equation
  if it.element != none and it.element.func() == eq {
    // Genera el número limpio (paréntesis con contador automático)
    let cnt = counter(eq).at(it.element.location()).first()
    link(it.element.location(), "(" + numbering("1", cnt) + ")")
  } else {
    it
  }
}


= Problema de Electrostática

4 cargas están en el plano XY, la primera carga de $8 mu C$ está en el origén, la segunda carga de $-2 mu C$ está en las coordenadas $[0,3] m$, la tercera carga de $4 mu C$ está en las coordenadas $[3,0] m$ y la cuarta carga de $2 mu C$ está ubicada en las coordenadas $[3,3] m$, Calcular la fuerza Electrica de la carga 4 debido a la presencia de las otras 3 cargas.

*Solución:*

Calculamos la Fuerza Electrostática de la carga 4 debido a la carga 1 *$arrow(F)_41$*, con la ley de Coulomb se tiene:

#math.equation(
  block: true,
  numbering: "1",
  $arrow(F)_41 = K_e (q_4q_1)/ r_41^2 hat(r)_41$,
) <fuerzaF41>

Calculamos el vector $hat(r)_41$, sabiendo que: $arrow(r)_4=3 hat(i)+ 3 hat(j)$, $arrow(r)_1=0 hat(i)+ 0 hat(j)$, $q_4=2 times 10^(-6) C$ y $q_1=8 times 10^(-6) C$

$
  arrow(r)_4 - arrow(r)_1 = (3 hat(i)+ 3 hat(j))m - (0 hat(i) + 0 hat(j))m = (3-0) hat(i)m + (3-0) hat(j)m = (3 hat(i) + 3 hat(j)) m
$

$
  |arrow(r)_4-arrow(r)_1| = sqrt((arrow(r)_4-arrow(r)_1) dot (arrow(r)_4-arrow(r)_1)) = sqrt((3 hat(i) + 3 hat(j)) dot (3 hat(i) + 3 hat(j)))
$

$
  |arrow(r)_4-arrow(r)_1| = sqrt(9+9) = sqrt(2 times 9) = 3 sqrt(2) m
$

$
  r_41^2 = |arrow(r)_4-arrow(r)_1|^2 = (3 sqrt(2) m)^2 = 18 m^2
$

$
  hat(r)_41=(arrow(r_4)-arrow(r_1))/(|arrow(r_4)-arrow(r_1)|) = (3 hat(i)+ 3 hat(j))/(3sqrt(2)) = (hat(i)+ hat(j))/(sqrt(2)) = 1/sqrt(2) hat(i) + 1/sqrt(2) hat(j)
$

una vez calculado $hat(r)_41$ utilizamos la ecuación @fuerzaF41

$
  arrow(F)_41 = 9 times 10^(9) (N m^2)/(C^2)((2 times 10^(-6) C)(8 times 10^(-6)C))/(18 m^2) (1/sqrt(2) hat(i) + 1/sqrt(2) hat(j))
$

$
  arrow(F)_41 = 8 times 10^(-3) N (1/sqrt(2) hat(i) + 1/sqrt(2) hat(j))
$

$
  arrow(F)_41 = 5.6568 times 10^(-3) hat(i) + 5.6568 times 10^(-3) hat(j) N
$

#v(1em)

Calculamos ahora la Fuerza Electrostática de la carga 4 debido a la carga 2 *$arrow(F)_42$*:
#math.equation(
  block: true,
  numbering: "1",
  $arrow(F)_42 = K_e (q_4q_2)/ r_42^2 hat(r)_42$,
) <fuerzaF42>

La carga 2 está en $arrow(r)_2=0 hat(i)+ 3 hat(j)$, con $q_2=-2 times 10^(-6) C$. El vector que va de la carga 2 a la carga 4 es:

$
  arrow(r)_4 - arrow(r)_2 = (3 hat(i)+ 3 hat(j))m - (0 hat(i) + 3 hat(j))m = 3 hat(i) m
$

$
  |arrow(r)_4-arrow(r)_2| = 3 m quad r_42^2 = 9 m^2
$

$
  hat(r)_42=(arrow(r_4)-arrow(r_2))/(|arrow(r_4)-arrow(r_2)|) = (3 hat(i))/(3) = hat(i)
$

Como $q_2$ es negativa y $q_4$ positiva la fuerza es de *atracción*, por lo que $arrow(F)_42$ se dirige hacia la carga 2 (sentido $-hat(i)$). Usando la ecuación @fuerzaF42:

$
  arrow(F)_42 = 9 times 10^(9) (N m^2)/(C^2)((2 times 10^(-6) C)(-2 times 10^(-6)C))/(9 m^2) hat(i)
$

$
  arrow(F)_42 = -4 times 10^(-3) hat(i) N
$

#v(1em)

Calculamos la Fuerza Electrostática de la carga 4 debido a la carga 3 *$arrow(F)_43$*:
#math.equation(
  block: true,
  numbering: "1",
  $arrow(F)_43 = K_e (q_4q_3)/ r_43^2 hat(r)_43$,
) <fuerzaF43>

La carga 3 está en $arrow(r)_3=3 hat(i)+ 0 hat(j)$, con $q_3=4 times 10^(-6) C$. El vector que va de la carga 3 a la carga 4 es:

$
  arrow(r)_4 - arrow(r)_3 = (3 hat(i)+ 3 hat(j))m - (3 hat(i) + 0 hat(j))m = 3 hat(j) m
$

$
  |arrow(r)_4-arrow(r)_3| = 3 m quad r_43^2 = 9 m^2
$

$
  hat(r)_43=(arrow(r_4)-arrow(r_3))/(|arrow(r_4)-arrow(r_3)|) = (3 hat(j))/(3) = hat(j)
$

Como $q_3$ y $q_4$ son positivas la fuerza es de *repulsión*, dirigida en sentido $+hat(j)$. Usando la ecuación @fuerzaF43:

$
  arrow(F)_43 = 9 times 10^(9) (N m^2)/(C^2)((2 times 10^(-6) C)(4 times 10^(-6)C))/(9 m^2) hat(j)
$

$
  arrow(F)_43 = 8 times 10^(-3) hat(j) N
$

#v(1em)

== Superposición de Fuerzas

Por el principio de superposición, la fuerza total sobre la carga 4 es la suma vectorial de las tres fuerzas:

#math.equation(
  block: true,
  numbering: "1",
  $arrow(F)_4 = arrow(F)_41 + arrow(F)_42 + arrow(F)_43$,
) <fuerzaTotal>

Sumamos componente a componente:

$
  arrow(F)_4 = (5.6568 times 10^(-3) hat(i) N + 5.6568 times 10^(-3) hat(j) N) + (-4 times 10^(-3) hat(i) N) + (8 times 10^(-3) hat(j) N)
$

$
  arrow(F)_4 = (5.6568 times 10^(-3) - 4 times 10^(-3)) hat(i) N + (5.6568 times 10^(-3) + 8 times 10^(-3)) hat(j) N
$

$
  arrow(F)_4 = 1.6568 times 10^(-3) hat(i) N + 13.6568 times 10^(-3) hat(j) N
$

Su magnitud, usando la ecuación @fuerzaTotal:

$
  |arrow(F)_4| = sqrt((1.6568 times 10^(-3))^2 + (13.6568 times 10^(-3))^2) N
$

$
  |arrow(F)_4| = sqrt(2.7450 times 10^(-6) + 186.5082 times 10^(-6)) N = sqrt(189.2532 times 10^(-6)) N
$

$
  |arrow(F)_4| = 13.757 times 10^(-3) N approx 13.76 times 10^(-3) N
$

Su dirección se obtiene con:

$
  theta = arctan(F_(4y)/F_(4x)) = arctan((13.6568 times 10^(-3))/(1.6568 times 10^(-3))) = arctan(8.2427) approx 83.08 deg
$

*Resultado:* la fuerza total sobre la carga 4 es

$
  arrow(F)_4 = 1.6568 times 10^(-3) hat(i) N + 13.6568 times 10^(-3) hat(j) N
$

con magnitud $|arrow(F)_4| approx 13.76 times 10^(-3) N$ y dirección $theta approx 83.08 deg$ respecto al eje $+x$.
