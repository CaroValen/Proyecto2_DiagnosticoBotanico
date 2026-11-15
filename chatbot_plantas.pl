% Motor de diagnostico botanico basado en reglas del proyecto original.
:- dynamic hecho_usuario/2.

sintoma(hojas_amarillas).
sintoma(tierra_humeda).
sintoma(hojas_secas).
sintoma(tierra_seca).
sintoma(tallos_estirados).
sintoma(hojas_palidas).
sintoma(puntos_blancos).
sintoma(manchas_cafes).

diagnosticar(Presentes) :-
    retractall(hecho_usuario(_, _)),
    cargar_hechos(Presentes),
    writeln('==================================================='),
    writeln('   BIENVENIDO AL DIAGNOSTICO DE PLANTAS'),
    writeln('==================================================='),
    findall(Diag-Rec, evaluar_diagnostico(Diag, Rec), Resultados),
    mostrar_resultados(Resultados).

% Usa los nombres de sintomas, no una secuencia de respuestas si/no.
cargar_hechos(Presentes) :-
    forall(sintoma(S),
        ( memberchk(S, Presentes)
        -> asserta(hecho_usuario(S, si))
        ;  asserta(hecho_usuario(S, no))
        )).

evaluar_diagnostico(exceso_de_agua,
        'suspender el riego de inmediato, verificar el drenaje y dejar secar el sustrato.') :-
    verificar(hojas_amarillas, 'Las hojas estan amarillas'),
    verificar(tierra_humeda, 'La tierra esta humeda').

evaluar_diagnostico(falta_de_agua,
        'regar de forma abundante hasta que el agua salga por los orificios de drenaje.') :-
    verificar(hojas_secas, 'Las hojas estan secas'),
    verificar(tierra_seca, 'El sustrato esta seco').

evaluar_diagnostico(falta_de_luz,
        'mover la planta a un lugar con luz indirecta brillante.') :-
    verificar(tallos_estirados, 'Los tallos estan estirados'),
    verificar(hojas_palidas, 'Las hojas nuevas estan palidas').

evaluar_diagnostico(plaga_cochinilla,
        'limpiar las hojas con algodon impregnado en alcohol, probando primero en una zona pequena.') :-
    verificar(puntos_blancos, 'Hay puntos blancos algodonosos').

evaluar_diagnostico(quema_por_sol,
        'alejar la planta del sol directo o colocar una cortina traslucida.') :-
    verificar(manchas_cafes, 'Hay manchas cafes').

verificar(Sintoma, _) :-
    hecho_usuario(Sintoma, si).

mostrar_resultados([]) :-
    writeln('No se pudo determinar un diagnostico certero con los sintomas entregados.').
mostrar_resultados(Resultados) :-
    Resultados = [_|_],
    writeln('[RESULTADO DEL DIAGNOSTICO]'),
    forall(member(Diag-Rec, Resultados),
        format('Diagnostico: ~w~nRecomendacion: ~w~n~n', [Diag, Rec])).
