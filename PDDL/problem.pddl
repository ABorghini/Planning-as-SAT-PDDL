(define (problem 3x3)
    (:domain robot_giardiniere)
    
    (:objects 
        robot_giardiniere - agente
        p1 p2 p3 p4 - pianta
        c00 c01 c02 c10 c11 c12 c20 c21 c22 - cella
    )
    
    (:init
        (at robot_giardiniere c02)
        (pianta-in p1 c00) 
        (pianta-in p2 c11) (infestante p2)
        (pianta-in p3 c22) (infestante p3)
        (pianta-in p4 c20) 

        (adj c00 c01) (adj c00 c10) (adj c01 c00) (adj c01 c11) (adj c01 c02) 
        (adj c02 c01) (adj c02 c12) (adj c10 c00) (adj c10 c11) (adj c10 c20) 
        (adj c11 c01) (adj c11 c10) (adj c11 c12) (adj c11 c21) (adj c12 c02)
        (adj c12 c11) (adj c12 c22) (adj c20 c10) (adj c20 c21) (adj c21 c11) 
        (adj c21 c20) (adj c21 c22) (adj c22 c12) (adj c22 c21)
    )
    
    (:goal
        (and 
            (not (pianta-in p2 c11)) 
            (not (pianta-in p3 c22)) 
            (innaffiata p1) 
            (innaffiata p4) 
        )
    )
)
