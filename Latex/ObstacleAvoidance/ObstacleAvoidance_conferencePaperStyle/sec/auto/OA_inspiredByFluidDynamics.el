(TeX-add-style-hook
 "OA_inspiredByFluidDynamics"
 (lambda ()
   (LaTeX-add-labels
    "sec:IFD"
    "sec:basicCircle"
    "fig:staticELlipse_IFD")
   (LaTeX-add-environments
    '("biography" LaTeX-env-args ["argument"] 1)))
 :latex)

