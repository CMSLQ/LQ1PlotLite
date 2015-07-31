#eejj
python plot_eejj_finalSelection.py
#python plot_eejj_finalSelection_bestFit.py
python plot_eejj_finalSelection_nMinus1.py
#python plot_eejj_finalSelection_nMinus1_bestFit.py
python plot_eejj_preselection.py

#enujj
python plot_enujj_finalSelection.py
#python plot_enujj_finalSelection_bestFit.py
python plot_enujj_finalSelection_nMinus1.py
#python plot_enujj_finalSelection_nMinus1_bestFit.py
python plot_enujj_preselection.py

# limits
root -q BR_Sigma_EE_vsMass.C
root -q BR_Sigma_ENu_vsMass.C
root -q ComboPlotLQ1.C
