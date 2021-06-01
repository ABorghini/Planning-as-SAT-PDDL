(define (problem 3x3)
    (:domain robot_giardiniere)
    
    (:objects 
        robot_giardiniere - agente
        p1 p2 p3 p4 - pianta
        c00 c01 c02 c10 c11 c12 c20 c21 c22 - cella
    )
    
    (:init
        (at robot_giardiniere c00)
        (pianta-in p1 c10)
        (pianta-in p2 c11)
        (pianta-in p3 c02) (sana p3)
        (pianta-in p4 c22) (sana p4)

        (adj c00 c01) (adj c00 c10) (adj c01 c11) (adj c01 c02) (adj c02 c12)
        (adj c10 c11) (adj c10 c20) (adj c11 c12) (adj c11 c21) (adj c12 c22)
        (adj c20 c21) (adj c21 c22)
        (adj c01 c00) (adj c10 c00) (adj c11 c01) (adj c02 c01) (adj c12 c02)
        (adj c11 c10) (adj c20 c10) (adj c12 c11) (adj c21 c11) (adj c22 c12)
        (adj c21 c20) (adj c22 c21)
    )
    
    (:goal
        (and 
            (not (pianta-in p1 c10)) 
            (not (pianta-in p2 c11)) 
            (innaffiata p3) 
            (innaffiata p4) 
        )
    )
)
