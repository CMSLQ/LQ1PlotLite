
python plot_enujj_preselection.py
cp sT_preselection_enujj.pdf  /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/enu/preselection_noRatio/sT_PAS_enujj.pdf 
cp Mej_preselection_enujj.pdf /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/enu/preselection_noRatio/Mej_PAS_enujj.pdf 

python plot_eejj_preselection.py
cp sT_preselection_eejj.pdf               /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/ee/preselection_noRatio/sT_PAS_eejj.pdf
cp Mej_selected_min_preselection_eejj.pdf /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/ee/preselection_noRatio/Mej_selected_min_PAS_eejj.pdf

python plot_enujj_finalSelection.py
cp ST_450_enujj.pdf  /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/enu/finalSelection/ST_LQ450_enujj.pdf
cp Mej_450_enujj.pdf /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/enu/finalSelection/Mej_LQ450_enujj.pdf
cp ST_650_enujj.pdf  /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/enu/finalSelection/ST_LQ650_enujj.pdf
cp Mej_650_enujj.pdf /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/enu/finalSelection/Mej_LQ650_enujj.pdf

python plot_eejj_finalSelection.py
cp sT_450_eejj.pdf               /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/ee/finalSelection/sT_eejj_LQ450_eejj.pdf
cp Mej_selected_min_450_eejj.pdf /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/ee/finalSelection/Mej_selected_min_LQ450_eejj.pdf
cp sT_650_eejj.pdf               /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/ee/finalSelection/sT_eejj_LQ650_eejj.pdf
cp Mej_selected_min_650_eejj.pdf /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/ee/finalSelection/Mej_selected_min_LQ650_eejj.pdf

python plot_enujj_finalSelection_nMinus1.py
cp Mej_stAndMtAndMetLQ_650_enujj.pdf /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/enu/nMinus1_PAS/Mej_stAndMtAndMetLQ650_enujj.pdf

python plot_eejj_finalSelection_nMinus1.py
cp Mej_selected_min_StAndMeeLQ_650_eejj.pdf /Users/eberry/Code/LQPaper/papers/EXO-12-041/trunk/fig/ee/nMinus1_PAS/Mej_selected_min_StAndMeeLQ650_eejj.pdf

rm *.pdf
