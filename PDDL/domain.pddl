(define (domain robot_giardiniere)
    (:requirements :strips :negative-preconditions :equality :typing)
    
    (:types agente pianta cella)
    
    (:predicates
        (adj ?from ?to) (innaffiata ?p) (sana ?p)
        (pianta-in ?p ?c) (at ?robot ?c)
    )
    
    (:action move
        :parameters (?robot - agente ?from - cella ?to - cella)
        :precondition (and (at ?robot ?from) (adj ?from ?to) (not (= ?from ?to)))
        :effect (and (at ?robot ?to) (not (at ?robot ?from)))
    )
    
    (:action innaffia
        :parameters (?robot - agente ?c - cella ?p - pianta)
        :precondition (and (at ?robot ?c) (pianta-in ?p ?c) (sana ?p) (not (innaffiata ?p)))
        :effect (and (innaffiata ?p))
    )
    
    (:action estirpa
        :parameters (?robot - agente ?c - cella ?p - pianta)
        :precondition (and (at ?robot ?c) (pianta-in ?p ?c) (not (sana ?p)))
        :effect (and (not (pianta-in ?p ?c)))
    )
)
