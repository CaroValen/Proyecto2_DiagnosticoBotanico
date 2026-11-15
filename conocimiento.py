"""Conocimiento compartido por la interfaz y el modelo de lenguaje."""

SINTOMAS = {
    "hojas_amarillas": "Las hojas están amarillas",
    "tierra_humeda": "La tierra está muy húmeda o encharcada",
    "hojas_secas": "Las hojas están marrones, crujientes o secas",
    "tierra_seca": "El sustrato está completamente seco",
    "tallos_estirados": "Los tallos están muy largos buscando luz",
    "hojas_palidas": "Las hojas nuevas nacen pequeñas o pálidas",
    "puntos_blancos": "Hay puntos blancos algodonosos en hojas o tallos",
    "manchas_cafes": "Hay manchas cafés similares a quemaduras solares",
}

REGLAS = {
    "exceso_de_agua": (("hojas_amarillas", "tierra_humeda"), "Suspender el riego, verificar el drenaje y dejar secar el sustrato."),
    "falta_de_agua": (("hojas_secas", "tierra_seca"), "Regar hasta que el agua salga por los orificios de drenaje."),
    "falta_de_luz": (("tallos_estirados", "hojas_palidas"), "Mover la planta a un lugar con luz indirecta brillante."),
    "plaga_cochinilla": (("puntos_blancos",), "Limpiar las hojas con algodón impregnado en alcohol, probando primero en una zona pequeña."),
    "quema_por_sol": (("manchas_cafes",), "Alejar la planta del sol directo o colocar una cortina traslúcida."),
}
