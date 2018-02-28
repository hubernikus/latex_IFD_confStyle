(TeX-add-style-hook
 "results"
 (lambda ()
   (TeX-run-style-hooks
    "input/multipleStaticEllipses"
    "input/fastMovingEllipse"
    "input/leftMovingCircle"
    "input/rotatingObstacle"
    "input/quantitativeComparison")
   (LaTeX-add-labels
    "sec:comparison"))
 :latex)

